import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings
from deep_research.search_agent import (
    search_agent,
    main,
    INSTRUCTIONS,
)


def test_search_agent_configuration():
    """
    Tests that the search_agent is configured correctly.
    """
    assert isinstance(search_agent, Agent)
    assert search_agent.name == "Search agent"
    assert search_agent.instructions == INSTRUCTIONS
    assert search_agent.model == "gpt-4o-mini"
    assert isinstance(search_agent.model_settings, ModelSettings)
    assert search_agent.model_settings.tool_choice == "required"

    assert len(search_agent.tools) == 1
    tool = search_agent.tools[0]
    assert isinstance(tool, WebSearchTool)
    assert tool.search_context_size == "low"


@pytest.mark.asyncio
async def test_main_execution_flow(capsys):
    """
    Tests the main execution flow, mocking the Runner.run call to avoid
    making a real API call.
    """
    # 1. Prepare mock data
    mock_summary = "This is a mock summary of the search results about all the countries in the world."
    mock_runner_result = MagicMock()
    mock_runner_result.final_output = mock_summary
    test_message = "What are all the countries in whole wide world in 2025?"

    # 2. Patch dependencies in the module where they are used
    with patch("deep_research.search_agent.Runner.run", new_callable=AsyncMock, return_value=mock_runner_result) as mock_run, \
         patch("deep_research.search_agent.load_dotenv") as mock_load_dotenv:

        # 3. Run the function to test
        result = await main(test_message)

        # 4. Assert that the mocked functions were called as expected
        mock_load_dotenv.assert_called_once()
        mock_run.assert_awaited_once_with(search_agent, test_message)

        # 5. Assert that the final output was printed to the console
        captured = capsys.readouterr()
        assert mock_summary in captured.out

        # 6. Assert the return value
        assert result == mock_summary