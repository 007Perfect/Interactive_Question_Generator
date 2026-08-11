import os
import gradio as gr
from google import genai

# Get API key from Render Environment Variables
API_KEY = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"


def generate_questions(topic, difficulty, number):

    if not topic.strip():
        return "Please enter a topic."

    prompt = f"""
You are a question generator.

Generate exactly {number} questions about:
Topic: {topic}

Difficulty: {difficulty}

Rules:
- Number each question.
- Keep questions clear and simple.
- Give only the questions.
- Do not provide answers.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks() as app:

    gr.Markdown("# Interactive Question Generator")
    gr.Markdown("Generate questions using Gemini AI.")

    topic = gr.Textbox(
        label="Enter Topic",
        placeholder="Example: Artificial Intelligence"
    )

    difficulty = gr.Dropdown(
        choices=["Easy", "Medium", "Hard"],
        value="Easy",
        label="Difficulty"
    )

    number = gr.Slider(
        minimum=1,
        maximum=10,
        value=5,
        step=1,
        label="Number of Questions"
    )

    generate_button = gr.Button("Generate Questions")

    output = gr.Textbox(
        label="Generated Questions",
        lines=10
    )

    generate_button.click(
        fn=generate_questions,
        inputs=[topic, difficulty, number],
        outputs=output
    )


# Render requires the app to listen on the provided port.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
