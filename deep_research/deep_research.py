# deep_research.py

import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

mgr = ResearchManager()

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research Agent")

    # STEP 1 — Initial user topic
    topic_input = gr.Textbox(
        label="What topic would you like to research?",
        placeholder="E.g. The future of renewable energy technologies in Europe"
    )
    next_button = gr.Button("Next: Suggest Follow-up Questions", variant="primary")

    # STEP 2 — Display follow-up questions and extra info box
    followup_md = gr.Markdown(visible=False)
    extra_info_input = gr.Textbox(
        label="Add any extra details or clarifications based on the follow-up questions above.",
        placeholder="Write anything you’d like the research to focus on...",
        visible=False,
        lines=4,
    )
    run_button = gr.Button("Run Research", variant="primary", visible=False)

    # STEP 3 — Show report
    report_output = gr.Markdown(visible=False)

    # Step 1 → Step 2
    async def generate_followups(query):
        followups = await mgr.ask_followup_questions(query)

        # Build markdown string
        markdown_text = "## Suggested Follow-up Questions\n"
        markdown_text += "These are some questions you might answer to help refine your research:\n\n"
        for i, q in enumerate(followups.questions, 1):
            markdown_text += f"**{i}. {q.question}**\n\n"

        # Return new markdown value, make visible=True, also show extra input box and run button
        return (
            gr.update(value=markdown_text, visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=False)
        )

    next_button.click(
        generate_followups,
        inputs=topic_input,
        outputs=[
            followup_md,
            extra_info_input,
            run_button,
            report_output
        ]
    )


    # Step 2 → Step 3
    async def run_full_research(query, extra_text):
        combined_query = mgr.combine_query_with_followups(query, extra_text)
        chunks = []
        async for chunk in mgr.run(combined_query):
            chunks.append(chunk)

        final_report = chunks[-1] if chunks else "No report generated."
        return gr.update(value=final_report, visible=True)

    run_button.click(
        run_full_research,
        inputs=[topic_input, extra_info_input],
        outputs=[report_output]
    )

ui.launch(inbrowser=True)
