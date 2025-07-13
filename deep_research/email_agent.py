from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from dotenv import load_dotenv
import asyncio
import os
import brevo_python
from brevo_python.rest import ApiException

@function_tool
def send_email_via_brevo_sdk(
    subject:str ="No Subject",
    html_content:str ="",
    text_content:str ="No content provided."
):
    """
    Send an email using Brevo's official Python SDK (Transactional Emails).
    Send out an email with the given subject and HTML body.
    Never use attachement as a method to send the content - always use email body.

    Parameters:
    - subject (str): Email subject.
    - html_content (str): HTML body.

    Returns:
    - API response (dict) or error message.
    """
    api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_name = "Shailesh"
    receiver_email = os.getenv("RECEIVER_EMAIL")
    receiver_name = "Friend"

    # Configure API client with API key
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = api_key

    # Create an API client
    api_instance = brevo_python.TransactionalEmailsApi(
        brevo_python.ApiClient(configuration)
    )

    # Prepare the email payload
    send_smtp_email = brevo_python.SendSmtpEmail(
        sender={
            "name": sender_name,
            "email": sender_email
        },
        to=[
            {
                "email": receiver_email,
                "name": receiver_name
            }
        ],
        subject=subject,
        html_content=html_content,
        text_content=text_content
    )

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email sent! Response:")
        print(api_response)
        return api_response.to_dict()
    except ApiException as e:
        print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)
        return {"error": str(e)}
    
INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email_via_brevo_sdk],
    model="gpt-4o-mini",    
    model_settings=ModelSettings(tool_choice="required"),
)

async def main(report: str):
    load_dotenv()

    with trace("Email"):
        result = await Runner.run(email_agent, report)
        print(result.final_output)
        return result.final_output

if __name__ == "__main__":
    # Example usage:
    # In a real scenario, the 'message' would come from the writer agent's output
    example_report = """
    # Research Report on Renewable Energy

    ## Introduction
    Renewable energy sources are crucial for mitigating climate change...

    ## Key Findings
    - Solar power: ...
    - Wind power: ...

    ## Policy Implementations
    - Germany's Energiewende...
    - China's massive investments...

    ## Challenges
    - Grid integration...
    - Storage solutions...

    ## Conclusion
    Renewable energy plays a pivotal role...
    """
    asyncio.run(main(example_report))
