from typing_extensions import TypedDict , NotRequired
from typing import Optional , List
from .objects import Analyst
class GenerateAnalystsState(TypedDict):
    """
    Represents the state required for generating analysts.
    """
    topic: str
    max_analysts: int
    human_analysts_feedback: NotRequired[Optional[str]]
    analysts: NotRequired[List[Analyst]]
    #research_question: str
    
