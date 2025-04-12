from flask import Flask
import gradio as gr
import threading

app = Flask(__name__)


def greet(name):
    return f"Welcome, {name}!"


def launch_gradio():
    iface = gr.Interface(fn=greet, inputs="text", outputs="text", title="Greeting Bot")
    iface.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)


@app.route("/")
def home():
    return "✅ Flask is running. Gradio UI runs at port 7860"


if __name__ == "__main__":
    threading.Thread(target=launch_gradio, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, threaded=True)
