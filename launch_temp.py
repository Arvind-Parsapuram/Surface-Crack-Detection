import app; app.app.launch(server_port=8501, server_name='0.0.0.0', css=app.CUSTOM_CSS, theme=__import__('gradio').themes.Soft(), prevent_thread_lock=True, quiet=True)
