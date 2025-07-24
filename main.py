from dotenv import load_dotenv
from app.workflow import Workflow
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

def main():
    workflow = Workflow()
    print("💡 Lifestyle Coach Agent")

    while True:
        query = input("\n🏃‍♀️ Lifestyle Goal or Challenge: ").strip()
        if query.lower() in {"quit", "exit"}:
            break

        if query:
            result = workflow.run(query)
            print(f"\n📋 Personalized Recommendations for: {query}")
            print("=" * 60)

            if result.tips:
                print("\n🌿 Lifestyle Tips:")
                for i, tip in enumerate(result.tips, 1):
                    print(f"{i}. {tip.text}")
                    if tip.source_url:
                        print(f"   🔗 Source: {tip.source_url}")

            if result.analysis:
                print("\n🧠 Article Insights:")
                print("-" * 40)
                for i, article in enumerate(result.analysis, 1):
                    print(f"\nArticle {i}: {article.title}")
                    print(f"📝 Summary: {article.summary}")
                    print(f"💡 Key Insights: {article.key_insights}")
                    print(f"🔗 Source: {article.url}")

            if result.recommendation:
                print("\n🎯 Lifestyle Coach Recommendation:")
                print("-" * 40)
                print(result.recommendation)

if __name__ == "__main__":
    main()
