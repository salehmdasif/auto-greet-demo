import gradio as gr
import pandas as pd
import io


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
        sample_str = df.sample(10).to_string()

        result = (
            f"🧠 Dataset Info:\n{info_str}\n\n"
            f"📊 Describe:\n{describe_str}\n\n"
            f"🔍 Sample:\n{sample_str}"
        )
        return result

    except Exception as e:
        return f"❌ Error: {str(e)}"


gr.Interface(
    fn=analyze_dataset,
    inputs=gr.File(label="Upload CSV or Excel", type="filepath"),
    outputs=gr.Textbox(label="EDA Summary", lines=30),
    title="EDA Viewer"
).launch()
