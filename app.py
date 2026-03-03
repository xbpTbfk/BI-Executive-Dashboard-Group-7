import gradio as gr
import asyncio
import os
import pandas as pd
import altair as alt
import json
import re
from dotenv import load_dotenv
from google.genai import types
from bi_agent import bi_runner

load_dotenv(dotenv_path='bi_agent/.env')

async def run_bi_pipeline_async(user_question: str):
    session = await bi_runner.session_service.create_session(
        user_id='user', app_name='agents'
    )
    content = types.Content(role='user', parts=[types.Part(text=user_question)])
    events_async = bi_runner.run_async(
        user_id='user', session_id=session.id, new_message=content
    )
    results = {}
    async for event in events_async:
        if event.actions and event.actions.state_delta:
            for key, value in event.actions.state_delta.items():
                results[key] = value
                if "---RESULT_START---" in str(value):
                    print("✅ Final Response Captured!")
    return results

def process_request(message: str):
    sql_query = "-- No SQL"
    df = None
    chart = None
    explanation = "Processing..."
    error_msg = ""
    error_visible = gr.update(visible=False)

    try:
        results = asyncio.run(run_bi_pipeline_async(message))
        raw_response = results.get('final_response', '')
        
        if not raw_response:
            return "No response", None, None, "The agent returned nothing.", "Agent Error: Empty Response", gr.update(visible=True)

        json_pattern = r"---RESULT_START---(.*?)---RESULT_END---"
        match = re.search(json_pattern, raw_response, re.DOTALL)
        
        if not match:
            return raw_response, None, None, "-- No SQL", "Format Error: Could not find JSON markers", gr.update(visible=True)

        data_json = json.loads(match.group(1).strip())
        
        sql_query = data_json.get('sql_used', '-- No SQL provided')
        explanation = data_json.get('text_response', 'No insights generated.')
        chart_code = data_json.get('chart_code', '')
        raw_data = data_json.get('raw_data', [])
        df = pd.DataFrame(raw_data) if raw_data else None
        
        if chart_code and df is not None:
            try:
                clean_code = re.sub(r"```python|```", "", chart_code).strip()
                namespace = {'alt': alt, 'pd': pd, 'df': df}
                exec(clean_code, namespace)
                chart = namespace.get('chart')
            except Exception as e:
                error_msg = f"Visualization Error: {str(e)}"
                error_visible = gr.update(visible=True)

        return explanation, chart, df, sql_query, error_msg, error_visible

    except Exception as e:
        return "An error occurred.", None, None, "-- Error", f"System Error: {str(e)}", gr.update(visible=True)

# --- CSS ---
custom_css = """
.main-title { text-align: center; font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #2563eb, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; }
.sub-title { text-align: center; color: #666; font-size: 1rem; margin-bottom: 20px; }
.insight-box { border: 1px solid #e2e8f0; background: #fdfdfd; padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.error-box { background-color: #fff1f2; border: 1px solid #fda4af; border-radius: 8px; padding: 15px; color: #9f1239; }
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("# 💎 BI Executive Dashboard", elem_classes="main-title")
    gr.Markdown("Text-to-SQL Intelligence | Group 7 | Made with 💧", elem_classes="sub-title")

    # 1. Error Row (Hidden by default)
    with gr.Column(visible=False, elem_classes="error-box") as error_container:
        gr.Markdown("### 🛠 Technical Problem / Bug")
        error_display = gr.Markdown("")

    # 2. Input Row
    with gr.Row():
        user_input = gr.Textbox(label="Your Question", placeholder="Ask anything about the data...", scale=4)
        submit_btn = gr.Button("Analyze", variant="primary", scale=1)

    # 3. Insights
    with gr.Column(elem_classes="insight-box"):
        gr.Markdown("### 💡 Key Insights")
        explanation_output = gr.Markdown("Waiting for input...")

    # 4. Visualization & Table
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("### 📊 Visualization")
            chart_output = gr.Plot()
        with gr.Column(scale=2):
            gr.Markdown("### 📋 Raw Data")
            data_output = gr.DataFrame(max_height=400)

    # 5. SQL
    with gr.Group():
        gr.Markdown("### 🔍 SQL Query Trace")
        sql_output = gr.Code(language="sql")

    submit_btn.click(
        fn=process_request,
        inputs=[user_input],
        outputs=[explanation_output, chart_output, data_output, sql_output, error_display, error_container]
    )

if __name__ == "__main__":
    demo.launch()