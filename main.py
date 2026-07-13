import gradio as gr

from ui import create_app

app, css, nav_js = create_app()

if __name__ == "__main__":
    app.launch(
        server_port=8501,
        server_name="0.0.0.0",
        css=css,
        theme=gr.themes.Soft(),
        head=nav_js,
    )
