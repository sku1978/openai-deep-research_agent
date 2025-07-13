from dotenv import load_dotenv
from agents import trace, Runner
from followup_agent import followup_agent
from writer_agent import ReportData
from research_manager import research_manager_agent
import asyncio
import gradio as gr

load_dotenv()

STATE_IDLE = "idle"
STATE_AWAITING_FOLLOWUPS = "awaiting_followups"

def run_async(fn, *args, **kwargs):
    return asyncio.run(fn(*args, **kwargs))

async def get_formatted_followup_questions(topic: str) -> str:
    with trace("Deep Research Followup Questions"):
        result = await Runner.run(followup_agent, topic)
    
    # final_output is a list of FollowUpQuestion objects
    list_of_questions = [q.question for q in result.final_output.questions]

    formatted = "\n".join(f"- {q}" for q in list_of_questions)

    return formatted

# sync wrapper for Gradio
def get_formatted_followup_questions_sync(topic: str) -> str:
    return run_async(get_formatted_followup_questions, topic)

def format_final_output(final_output: ReportData) -> str:
    """
    Formats the final ReportData into a human-readable string.
    """
    summary = final_output.short_summary
    markdown_report = final_output.markdown_report
    follow_ups = final_output.follow_up_questions

    formatted_followups = ""
    if follow_ups:
        formatted_followups = "\n".join(f"- {q}" for q in follow_ups)

    formatted = (
        f"✅ **Short Summary**\n{summary}\n\n"
        f"✅ **Report**\n{markdown_report}\n\n"
    )

    if formatted_followups:
        formatted += f"✅ **Follow-Up Questions**\n{formatted_followups}\n"

    return formatted

async def run_full_research(topic: str):
    with trace("Deep Research Full Run"):
        return await Runner.run(research_manager_agent, topic)

def chatbot(user_input, chat_history, state):
    
    if state["status"] == STATE_IDLE:
        topic = user_input

        formatted_questions = get_formatted_followup_questions_sync(topic)

        chat_history.append({"role": "user", "content": topic})
        formatted_questions = get_formatted_followup_questions_sync(topic)

        chat_history.append({
            "role": "assistant",
            "content": f"Here are some follow-up questions:\n{formatted_questions}"
        })

        state["status"] = STATE_AWAITING_FOLLOWUPS
        state["topic"] = topic

        return "", chat_history, state

    elif state["status"] == STATE_AWAITING_FOLLOWUPS:
        user_followup_answers = user_input
        topic = state["topic"]

        revised_topic = topic + "\n\nAdditional Context:\n" + user_followup_answers

        final_result = run_async(
            run_full_research,
            revised_topic
        )

        formatted_output = format_final_output(final_result.final_output)

        chat_history.append({"role": "user", "content": user_followup_answers})
        chat_history.append({
            "role": "assistant",
            "content": f"Here’s the result of further research:\n{formatted_output}"
        })

        state["status"] = STATE_IDLE
        state["topic"] = None

        return "", chat_history, state

    else:
        chat_history.append({"role": "assistant", "content": "I’m not sure what to do."})
        return "", chat_history, state

with gr.Blocks() as demo:
    chatbot_ui = gr.Chatbot(type="messages")
    state = gr.State({"status": STATE_IDLE, "topic": None})
    txt = gr.Textbox(placeholder="Enter your research topic or answer follow-up questions")

    def respond(message, history, state):
        return chatbot(message, history, state)

    txt.submit(respond, [txt, chatbot_ui, state], [txt, chatbot_ui, state])

demo.launch()
