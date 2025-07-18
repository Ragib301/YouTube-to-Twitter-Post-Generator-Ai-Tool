import gradio as gr
from os import path
from get_transcript import get_youtube_transcript
from generate_post import generate_posts, generate_data
from spreadsheet_schedule import create_spreadsheet, run_schedule


def main_func(video_url, post_count, progress=gr.Progress()):
    progress(0.0, desc="Starting...")
    transcript, video_id = get_youtube_transcript(video_url)
    if not transcript:
        return "Could not fetch transcript.", None, gr.update(visible=False)

    progress(0.25, desc="Transcript fetched...")
    post_list = generate_posts(transcript, post_count)
    progress(0.5, desc="Generated blog posts...")
    post_data = generate_data(post_list)
    progress(0.75, desc="Generating spreadsheet...")
    dataFrame = create_spreadsheet(post_data)

    progress(0.9, desc="Finzalizing Outputs...")

    message = f"Transcript processed and spreadsheet created!\n\n"
    if not dataFrame.empty:
        contents = dataFrame['content'].to_list()
        for i in range(len(contents)):
            message += f" - [Post {i+1}]: {contents[i]}\n\n"
        message += f"\n - [Transcript]: {transcript[:500]}..."
    else:
        message = "Processing complete but spreadsheet is empty."
    progress(1.0, desc="Done!")

    return message, dataFrame, gr.update(visible=True), gr.DownloadButton(value='output.zip', visible=True)


def clear_inputs():
    return "", 3, ""


def twitter_posting(time_input):
    gr.Info("Post Schedule running on Thread!")
    import threading
    threading.Thread(target=run_schedule, args=(time_input,)).start()


css = """
.gradio-container {
    background: url('file=background.jpg');
}
.gr-button {
    font-weight: bold;
}
"""
with gr.Blocks(theme=gr.themes.Default(text_size="lg"), css=css,
               title="Ai Blog Post Generator") as app:
    gr.Markdown(
        """
        # <center><h1>Ai Blog Post Generator from YouTube</h1></center>
        """,
        elem_id="title"
    )

    with gr.Row():
        with gr.Column(scale=1):
            youtube_input = gr.Textbox(
                label="YouTube Video Link", placeholder="https://youtube.com/...")
            blog_count = gr.Number(
                label="Number of Blog Posts", value=3, precision=0)
            time_input = gr.Textbox(label="Schedule Time to Post (HH:MM)",
                                    placeholder="14:30")

            with gr.Row():
                clear_btn = gr.Button("Clear", variant="secondary")
                submit_btn = gr.Button("Submit", variant="primary")
            twitter_btn = gr.Button("Schedule Post to Twitter", visible=False)
            download_btn = gr.DownloadButton("Download all files in ZIP",
                                             visible=False)

        with gr.Column(scale=1):
            output_box = gr.Textbox(
                label="Outputs", lines=5, max_lines=8, interactive=False)
            df_display = gr.Dataframe(label="Blog Schedule", visible=True)

    submit_btn.click(fn=main_func, inputs=[youtube_input, blog_count],
                     outputs=[output_box, df_display, twitter_btn, download_btn])
    clear_btn.click(fn=clear_inputs,
                    outputs=[youtube_input, blog_count, output_box])
    twitter_btn.click(fn=twitter_posting, inputs=time_input,
                      outputs=None)
    download_btn.click(fn=gr.Info("All contents downloaded in a ZIP File!"))


if __name__ == "__main__":
    background_image = 'background.jpg'
    absolute_path = path.abspath(background_image)
    app.launch(allowed_paths=[absolute_path], share=True)
