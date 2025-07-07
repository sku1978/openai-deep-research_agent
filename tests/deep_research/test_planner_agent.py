import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from agents import Agent
from deep_research.planner_agent import (
    planner_agent,
    main,
    WebSearchPlan,
    WebSearchItem,
    INSTRUCTIONS,
)


def test_planner_agent_configuration():
    """
    Tests that the planner_agent is configured correctly.
    """
    assert isinstance(planner_agent, Agent)
    assert planner_agent.name == "PlannerAgent"
    assert planner_agent.instructions == INSTRUCTIONS
    assert planner_agent.model == "gpt-4o-mini"
    assert planner_agent.output_type == WebSearchPlan


@pytest.mark.asyncio
async def test_main_execution_flow(capsys):
    """
    Tests the main execution flow, mocking the Runner.run call to avoid
    making a real API call.
    """
    # 1. Prepare mock data that mimics the expected output from the runner
    mock_search_plan = WebSearchPlan(
        searches=[
            WebSearchItem(reason="To get a comprehensive list.", query="list of all countries"),
            WebSearchItem(reason="To check for recent changes.", query="new countries 2025"),
        ]
    )
    mock_runner_result = MagicMock()
    mock_runner_result.final_output = mock_search_plan

    # 2. Patch dependencies in the module where they are used
    with patch("deep_research.planner_agent.Runner.run", new_callable=AsyncMock, return_value=mock_runner_result) as mock_run, \
         patch("deep_research.planner_agent.load_dotenv") as mock_load_dotenv:

        # 3. Prepare the test message
        expected_message = "What are all the countries in whole wide world in 2025?"

        # 4. Run the function to test
        await main(expected_message)

        # 5. Assert that the mocked functions were called as expected
        mock_load_dotenv.assert_called_once()
        mock_run.assert_awaited_once_with(planner_agent, expected_message)

        # 6. Assert that the final output was printed to the console
        captured = capsys.readouterr()
        assert str(mock_search_plan) in captured.out