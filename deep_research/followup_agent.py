from pydantic import BaseModel, Field
from typing import List
from agents import Agent, trace, Runner, gen_trace_id
from agents.model_settings import ModelSettings
import asyncio
from dotenv import load_dotenv

QUESTION_COUNT=5

# Pydantic output types
class FollowUpQuestion(BaseModel):
    question: str = Field(description="The text of the follow-up question.")

class FollowUpQuestions(BaseModel):
    questions: List[FollowUpQuestion] = Field(
        description="A list of three follow-up research questions"
    )

# Revised instructions
INSTRUCTIONS = (
    """You are an expert research assistant. 
    Given a user's research topic, generate up to {QUESTION_COUNT} follow-up questions.
    Ask follow-up questions when the initial query has:
        Ambiguous scope - "research AI" could mean technical implementation, business impact, ethics, etc.
        Multiple interpretations - "climate change effects" could focus on economics, ecology, human health, etc.
        Missing context - academic level, intended audience, specific use case
        Vague parameters - timeframe, geographic focus, depth of analysis needed
        Unclear deliverable format - summary, detailed report, specific data points
    Focus on the most critical disambiguation needs rather than trying to capture everything.
    Question Categories to Prioritize:
        Scope & Focus - "What specific aspect interests you most?"
        Context & Purpose - "How will you use this research?"
        Depth & Format - "Do you need a brief overview or detailed analysis?"
        Constraints - "Any specific timeframe, sources, or limitations?"
    """
)

# Define the agent
followup_agent = Agent(
    name="FollowupQuestionsAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=FollowUpQuestions,
    model_settings=ModelSettings(tool_choice="auto"),
)

async def main(topic: str):
    """
    Example standalone test run of the followup agent.
    """
    load_dotenv()

    with trace("FollowupQuestions"):
        result = await Runner.run(followup_agent, topic)
        print(result.final_output)
        return result.final_output

if __name__ == "__main__":
    example_topic = "What is the future of renewable energy technologies in Europe?"
    asyncio.run(main(example_topic))
