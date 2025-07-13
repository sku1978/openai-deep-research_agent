from dotenv import load_dotenv
from agents import Agent, 
from planner_agent import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent

load_dotenv()

planner_tool = planner_agent.as_tool(tool_name="planner_tool", tool_description="Plans for deep research by deciding the search terms")
search_tool = search_agent.as_tool(tool_name="search_tool", tool_description="Does a Websearch and returns result")

tools = [planner_tool, search_tool]
handoffs = [writer_agent]

instructions = """
Role: You are an expert research coordinator, responsible for efficiently gathering comprehensive information on a given topic and preparing it for a writer agent. You prioritize thoroughness, accuracy, and the effective use of designated tools.
Goal: To provide a comprehensive set of search results related to a given topic, enabling a separate writer agent to produce a high-quality research summary.
Constraints:
You must use the planner_tool tool to generate search terms.
You must use the search_tool for all searches.
You are not responsible for writing the summary; your job ends with the handoff of search results to the writer_tool.
"""

research_manager_agent = Agent(
    name="test_driver",
    instructions=instructions,
    model="gpt-4o-mini",
    tools=tools,
    handoffs=handoffs
)