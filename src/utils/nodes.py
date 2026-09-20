from dotenv import load_dotenv
from .states import GenerateAnalystsState
from .models import get_llm 
from .objects import Analyst , Perspectives
from .prompts import analyst_instructions
from langchain.messages import SystemMessage , HumanMessage
from langgraph.types import interrupt
load_dotenv()  # Load environment variables from .env file

def create_analysts(state: GenerateAnalystsState):
    """Create analysts"""
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analysts_feedback = state.get("human_analysts_feedback","")
    #research_question = state["research_question"]
    
    #Enforce structured output
    structured_llm = get_llm().with_structured_output(Perspectives)
    
    #system_massage
    system_message = analyst_instructions.format(topic=topic, human_analysts_feedback=human_analysts_feedback, max_analysts=max_analysts)
    
    # generate analysts
    analysts = structured_llm.invoke([SystemMessage(content=system_message)] + [HumanMessage(content="Please Generate the set of analysts.")])
    return {"analysts": analysts.analysts}

def human_feedback(state: GenerateAnalystsState):
    """
    this is where the human givens feedback about the analysts given.
    """
    feedback= interrupt({
        "question":"Are these analysts okey for you?",
        "analysts":[
            analyst.model_dump() if hasattr(analyst, 'model_dump') else analyst
            for analyst in state.get("analysts", [])
        ],
        "instructions": (
            "Return feedback to regenerate analysts, "
            "or return empty/perfect/continue/okay to approve and continue the graph."
        )
    })
    if feedback is None:
        return {"human_analyst_feedback": None }
    if isinstance(feedback, str):
        feedback= feedback.strip()
        if feedback =="":
            return {"human_analyst_feedback": None }
        if feedback.lower() in{"perfect" , "okey" , "continue" ,"yes"}:
            return {"human_analyst_feedback": None }
        return {"human_analyst_feedback": feedback}