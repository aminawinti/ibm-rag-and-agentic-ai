import gradio as gr

from config import SERVER_NAME, SERVER_PORT
from modules.query_engine import answer, summarize
from modules.transcript import get_video_id, load_transcript


def check_video(url):
    # returns an error message, or None when the video is usable
    if not url or not get_video_id(url):
        return "Please provide a valid YouTube URL."
    if not load_transcript(url):
        return "No English transcript available for this video."
    return None


def summarize_video(url):
    return check_video(url) or summarize(url)


def answer_question(url, question):
    if not question:
        return "Please enter a question."
    return check_video(url) or answer(url, question)


with gr.Blocks() as interface:
    gr.Markdown("<h2 style='text-align: center;'>YouTube Video Summarizer and Q&A</h2>")

    video_url = gr.Textbox(label="YouTube Video URL", placeholder="Enter the YouTube Video URL")

    summarize_btn = gr.Button("Summarize Video")
    summary_output = gr.Textbox(label="Video Summary", lines=5)

    question_input = gr.Textbox(label="Ask a Question About the Video", placeholder="Ask your question")
    question_btn = gr.Button("Ask a Question")
    answer_output = gr.Textbox(label="Answer to Your Question", lines=5)

    summarize_btn.click(summarize_video, inputs=video_url, outputs=summary_output)
    question_btn.click(answer_question, inputs=[video_url, question_input], outputs=answer_output)


if __name__ == "__main__":
    interface.launch(server_name=SERVER_NAME, server_port=SERVER_PORT)
