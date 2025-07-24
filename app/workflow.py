from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .tools import LifestyleCoachState, LifestyleTip, WellnessArticle, ArticleAnalysis
from .firecrawl import FirecrawlService
from .prompt import LifestyleCoachPrompts


class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.prompts = LifestyleCoachPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(LifestyleCoachState)
        graph.add_node("extract_tips", self._extract_tips_step)
        graph.add_node("analyze_articles", self._analyze_articles_step)
        graph.add_node("generate_recommendation", self._recommendation_step)
        graph.set_entry_point("extract_tips")
        graph.add_edge("extract_tips", "analyze_articles")
        graph.add_edge("analyze_articles", "generate_recommendation")
        graph.add_edge("generate_recommendation", END)
        return graph.compile()

    def _extract_tips_step(self, state: LifestyleCoachState) -> Dict[str, Any]:
        print(f"🔍 Searching wellness articles for: {state.query}")
        search_results = self.firecrawl.search_articles(state.query, num_results=3)

        articles: List[WellnessArticle] = []
        for result in search_results.data:
            url = result.get("url", "")
            title = result.get("metadata", {}).get("title", "Untitled")
            scraped = self.firecrawl.scrape_article(url)
            if not scraped:
                continue

            content = scraped.markdown[:3000]  # trim to fit token limit
            messages = [
                SystemMessage(content=self.prompts.TIP_EXTRACTION_SYSTEM),
                HumanMessage(content=self.prompts.tip_extraction_user(state.query, content))
            ]
            response = self.llm.invoke(messages)

            tips = []
            for line in response.content.strip().split("\n"):
                if line.strip() and line.strip()[0].isdigit():
                    tips.append(LifestyleTip(text=line.strip()[2:], source_url=url))

            articles.append(WellnessArticle(
                title=title,
                url=url,
                content=content,
                tips=tips
            ))

        return {"articles": articles}

    def _analyze_articles_step(self, state: LifestyleCoachState) -> Dict[str, Any]:
        print("🔎 Analyzing article content...")

        for article in state.articles:
            try:
                structured_llm = self.llm.with_structured_output(ArticleAnalysis)
                messages = [
                    SystemMessage(content=self.prompts.ARTICLE_ANALYSIS_SYSTEM),
                    HumanMessage(content=self.prompts.article_analysis_user(state.query, article.content))
                ]
                analysis = structured_llm.invoke(messages)
                article.analysis = analysis
            except Exception as e:
                print(f"❌ Failed to analyze article: {article.title} – {e}")
                article.analysis = None

        return {"articles": state.articles}

    def _recommendation_step(self, state: LifestyleCoachState) -> Dict[str, Any]:
        print("💡 Generating lifestyle recommendation...")

        all_tips = [tip.text for article in state.articles for tip in article.tips]
        if not all_tips:
            return {"recommendation": "Sorry, I couldn't find any solid tips for your query."}

        formatted_tips = "\n".join([f"- {t}" for t in all_tips[:5]])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, formatted_tips))
        ]

        try:
            response = self.llm.invoke(messages)
            return {"recommendation": response.content}
        except Exception as e:
            print(f"❌ Recommendation error: {e}")
            return {"recommendation": "There was a problem generating your recommendation."}

    def run(self, query: str) -> LifestyleCoachState:
        initial_state = LifestyleCoachState(query=query)
        final_state = self.workflow.invoke(initial_state)

        # Reconstruct objects to avoid attribute errors
        hydrated_articles = []
        for a in final_state["articles"]:
            tips = [LifestyleTip(**t.dict()) if isinstance(t, LifestyleTip) else LifestyleTip(**t) for t in a.tips]
            analysis = None
            if a.analysis:
                analysis = ArticleAnalysis(**a.analysis.dict()) if isinstance(a.analysis, ArticleAnalysis) else ArticleAnalysis(**a.analysis)
            hydrated_articles.append(WellnessArticle(
                title=a.title,
                url=a.url,
                content=a.content,
                tips=tips,
                analysis=analysis
            ))

        # Flatten tips
        all_tips = [tip for article in hydrated_articles for tip in article.tips]

        return LifestyleCoachState(
            query=query,
            articles=hydrated_articles,
            tips=all_tips,
            recommendation=final_state.get("recommendation"),
        )
