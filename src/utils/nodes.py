from dotenv import load_dotenv
from .states import GenerateAnalystsState , InterviewState
from .models import get_llm 
from .objects import Analyst , Perspectives , SearchQuery
from .prompts import (
    analyst_instructions,
    question_instructions,
    search_instructions,
    answer_instructions,
    section_writer_instructions
)
from langchain.messages import SystemMessage , HumanMessage
from langgraph.types import interrupt
from langchain_tavily import TavilySearch
from langchain_core.messages import get_buffer_string
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
    
def generate_question(state:InterviewState):
    """Node to generate the question"""   
    analyst = state["analyst"]
    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst) 
    messages = state["messages"]  
    #generate question
    system_massage = question_instructions.format(goals=analyst.persona)
    question = get_llm().invoke([SystemMessage(content=system_massage)]+messages) 
    
    return {"messages":[question]}
    
def search_web(state:InterviewState):
    """Return docs from the web""" 
    #seaarch query
    structred_llm = get_llm().with_structured_output(SearchQuery)
    #search intersection
    search_insrtuction_system_message = SystemMessage(content=search_insrtuctions)
    tavily_search = TavilySearch(max_results=3)
    search_query = structred_llm.invoke([search_insrtuction_system_message]+state["messages"])
    #search
    data = tavily_search.invoke({"query": search_query.search_query})    
    search_docs = data.get("results",data)
    
    #format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context":[formatted_search_docs]}

def search_web2(state:InterviewState):
    """Return docs from the web""" 
    #seaarch query9
    structred_llm = get_llm().with_structured_output(SearchQuery)
    #search intersection
    search_insrtuction_system_message = SystemMessage(content=search_insrtuctions)
    tavily_search = TavilySearch(max_results=3)
    search_query = structred_llm.invoke([search_insrtuction_system_message]+state["messages"])
    #search
    data = tavily_search.invoke({"query": search_query.search_query})
    search_docs = data.get("results",data)
    
    #format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context":[formatted_search_docs]}

def generate_answer(state:InterviewState):
    """Node to answer a question"""
    #get state
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]
    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)
    system_message = answer_instructions.format(goals=analyst.persona,context=context) 
    answer = get_llm.invoke([SystemMessage(content=system_message)]+messages)
    #name the message as coming from the expert
    answer.name = "expert"
    # append to the state
    return {"messages":[answer]}

def save_interview(state:InterviewState):
    """save interviews"""
    messages = state["messages"]
    interview = get_buffer_string(messages)
    return{"interview":interview}

def write_section(state: InterviewState):
    """
    Node to answer a question
    """
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]
    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)
    system_message = section_writer_instructions.format(focus= analyst.description)
    section= get_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Use this source to write your section:{context}")])
    
    return {"sections":[section.content]}    

    

        
