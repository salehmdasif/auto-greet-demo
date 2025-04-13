from flask import Flask
import gradio as gr
import threading
import pandas as pd
import io

app = Flask(__name__)


def analyze_dataset(file):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file.name)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file.name)
        else:
            return "❌ Unsupported file format."

        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()

        describe_str = df.describe(include='all').to_string()
        sample_str = df.sample(5).to_string()

        result = (
            f"🧠 Dataset Info:\n{info_str}\n\n"
            f"📊 Describe:\n{describe_str}\n\n"
            f"🔍 Sample Rows:\n{sample_str}"
        )
        return result

    except Exception as e:
        return f"❌ Error: {str(e)}"


def launch_gradio():
    gr.Interface(
        fn=analyze_dataset,
        inputs=gr.File(label="📂 Upload CSV/Excel", type="filepath"),
        outputs=gr.Textbox(label="📊 EDA Summary", lines=30),
        title="EDA Agent",
        description="Upload a dataset and view df.info(), describe(), and sample rows."
    ).launch(server_name="127.0.0.1", server_port=7865, inbrowser=True)


@app.route("/")
def home():
    return "✅ Flask is running. Visit http://127.0.0.1:7865 to use the EDA interface."


if __name__ == "__main__":
    threading.Thread(target=launch_gradio, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, threaded=True)
