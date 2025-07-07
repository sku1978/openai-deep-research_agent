from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
import asyncio
from dotenv import load_dotenv

INSTRUCTIONS = "You are a research assistant. Given a search term, you search the web for that term and \
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 \
words. Capture the main points. Write succintly, no need to have complete sentences or good \
grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the \
essence and ignore any fluff. Do not include any additional commentary other than the summary itself."

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)


async def main(message: str):
    """Loads environment, runs the search agent, and prints the result."""
    load_dotenv()

    with trace("Search"):
        result = await Runner.run(search_agent, message)
        print(result.final_output)
        return result.final_output

if __name__ == "__main__":
    query = "What are all the countries in whole wide world in 2025?"
    asyncio.run(main(query))