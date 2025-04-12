import gradio as gr


def greet(name):
    return f"Welcome, {name}!"


iface = gr.Interface(fn=greet, inputs="text", outputs="text", title="Greeting Bot")
iface.launch(inbrowser=True, share=True)
