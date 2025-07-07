from pydantic import BaseModel, Field
from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
import asyncio
from dotenv import load_dotenv


INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)

async def main(message: str):
    """Loads environment, runs the writer agent, and prints the result."""
    load_dotenv()

    with trace("Search"):
        result = await Runner.run(writer_agent, message)
        #print(result.final_output)
        print(result.final_output.markdown_report)
        return result.final_output

if __name__ == "__main__":
    query = (
    "Original Query:\n"
    "What is the role of renewable energy in mitigating climate change, and how have different "
    "countries implemented policies to accelerate renewable adoption?\n\n"
    "Initial Research Notes:\n"
    "- Renewable energy includes solar, wind, hydro, geothermal.\n"
    "- IPCC reports suggest renewables are crucial to stay below 1.5°C.\n"
    "- Countries like Germany, China, USA have significant renewable capacity but differ in policy approaches.\n"
    "- Challenges include grid integration, storage, costs, and political factors.\n"
)
    asyncio.run(main(query))

