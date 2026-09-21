from typing_extensions import TypedDict , NotRequired , Annotated
from typing import Optional , List
from .objects import Analyst
from langgraph.graph import MessagesState
import operator
class GenerateAnalystsState(TypedDict):
    """
    Represents the state required for generating analysts.
    """
    topic: str
    max_analysts: int
    human_analysts_feedback: NotRequired[Optional[str]]
    analysts: NotRequired[List[Analyst]]
    #research_question: str
    
class InterviewState(MessagesState):
    max_num_turns: int #Number turns of conversation
    context: Annotated[list,operator.add] #source of docs
    analyst:Analyst #my analyst
    interview: str# interview transcript
    sections: list # final key we duplication in outer state for Send() api  
    