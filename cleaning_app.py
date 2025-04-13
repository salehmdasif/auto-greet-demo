import gradio as gr
import pandas as pd

def clean_data(file, clean_method):
    try:
        filepath = file.name if hasattr(file, "name") else file
        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        elif filepath.endswith(".xlsx"):
            df = pd.read_excel(filepath)
        else:
            return pd.DataFrame()

        if clean_method == "Drop missing values":
            df = df.dropna()
        elif clean_method == "Fill numeric with median":
            for col in df.select_dtypes(include='number'):
                df[col] = df[col].fillna(df[col].median())
        elif clean_method == "Fill categorical with mode":
            for col in df.select_dtypes(include='object'):
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "")

        df = df.drop_duplicates()

        return df.head(10).to_markdown()  # ✅ Scrollable, Clean, Aligned

    except Exception as e:
        print("Error:", str(e))
        return pd.DataFrame()


gr.Interface(
    fn=clean_data,
    inputs=[
        gr.File(label="📂 Upload CSV or Excel", type="filepath"),
        gr.Radio(["Drop missing values", "Fill numeric with median", "Fill categorical with mode"],
                 label="Choose Cleaning Method")
    ],
    outputs=gr.Textbox(label="🧹 Cleaning Summary", lines=25),
    title="Step 3.1 – Data Cleaning Agent"
).launch()
