import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from agents import Agent
from deep_research.writer_agent import (
    writer_agent,
    main,
    INSTRUCTIONS,
    ReportData,
)


def test_writer_agent_configuration():
    """
    Tests that the writer_agent is configured correctly.
    """
    assert isinstance(writer_agent, Agent)
    assert writer_agent.name == "WriterAgent"
    assert writer_agent.instructions == INSTRUCTIONS
    assert writer_agent.model == "gpt-4o-mini"
    assert writer_agent.output_type == ReportData


@pytest.mark.asyncio
async def test_main_execution_flow(capsys):
    """
    Tests the main execution flow, mocking the Runner.run call to avoid
    making a real API call.
    """
    # 1. Prepare mock data that mimics the expected output from the runner
    mock_report_data = ReportData(
        short_summary="This is a mock summary.",
        markdown_report="# Mock Report\n\nThis is the body of the mock report.",
        follow_up_questions=["What about topic A?", "How does topic B relate?"],
    )
    mock_runner_result = MagicMock()
    mock_runner_result.final_output = mock_report_data

    # 2. Patch dependencies in the module where they are used
    with patch("deep_research.writer_agent.Runner.run", new_callable=AsyncMock, return_value=mock_runner_result) as mock_run, \
         patch("deep_research.writer_agent.load_dotenv") as mock_load_dotenv:

        # 3. Prepare the test message
        test_message = "Original Query: ...\nInitial Research Notes: ..."

        # 4. Run the function to test
        result = await main(test_message)

        # 5. Assert that the mocked functions were called as expected
        mock_load_dotenv.assert_called_once()
        mock_run.assert_awaited_once_with(writer_agent, test_message)

        # 6. Assert that the markdown report was printed to the console
        captured = capsys.readouterr()
        assert mock_report_data.markdown_report in captured.out

        # 7. Assert the return value
        assert result == mock_report_data