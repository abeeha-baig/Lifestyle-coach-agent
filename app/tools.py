from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class LifestyleTip(BaseModel):
    text: str
    category: Optional[str] = None  # e.g., "Morning Routine", "Sleep", "Productivity"
    difficulty: Optional[str] = None  # "Easy", "Moderate", "Hard"
    audience: Optional[str] = None  # "Students", "Remote Workers", etc.
    source_url: Optional[str] = None


class ArticleAnalysis(BaseModel):
    type_of_tips: List[str]
    audience: str
    difficulty: str
    tone: str
    sample_tip: str


class WellnessArticle(BaseModel):
    title: str
    url: str
    content: str
    tips: List[LifestyleTip] = []
    analysis: Optional[ArticleAnalysis] = None


class LifestyleCoachState(BaseModel):
    query: str
    search_results: List[Dict[str, Any]] = []
    articles: List[WellnessArticle] = []
    recommendation: Optional[str] = None
    tips: List[LifestyleTip] = []                     
    analysis: Optional[List[Dict[str, Any]]] = None   
