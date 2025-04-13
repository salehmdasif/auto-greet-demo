import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import io

# Global variable to store filtered dataframe
df_global = None


# Function: Clean data
def clean_data(file, method):
    global df_global
    filepath = file.name if hasattr(file, 'name') else file
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        return "Unsupported file format."

    if method == "Drop missing values":
        df = df.dropna()
    elif method == "Fill numeric with median":
        for col in df.select_dtypes(include='number'):
            df[col] = df[col].fillna(df[col].median())
    elif method == "Fill categorical with mode":
        for col in df.select_dtypes(include='object'):
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode[0])

    df = df.drop_duplicates()
    df_global = df.copy()
    return df


# Function: Filter data with query
def filter_data(query):
    global df_global
    if df_global is None:
        return pd.DataFrame()
    try:
        df_filtered = df_global.query(query)
        return df_filtered
    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])


# Function: Download filtered data
def download_data():
    global df_global
    if df_global is None:
        return None
    df_global.to_csv("filtered_output.csv", index=False)
    return "filtered_output.csv"


# Function: Generate chart
def generate_chart(x_col, y_col, chart_type):
    global df_global
    if df_global is None or x_col not in df_global:
        return None

    plt.figure(figsize=(8, 4))

    try:
        if chart_type == "Bar":
            if y_col not in df_global:
                return None
            df_global.groupby(x_col)[y_col].mean().plot(kind='bar')
            plt.ylabel(f"Average of {y_col}")

        elif chart_type == "Line":
            if y_col not in df_global:
                return None
            df_global.groupby(x_col)[y_col].mean().plot(kind='line')
            plt.ylabel(f"Average of {y_col}")

        elif chart_type == "Pie":
            df_global[x_col].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.ylabel("")

        plt.title(f"{chart_type} Chart of {y_col if chart_type != 'Pie' else x_col}")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    except Exception as e:
        print("Chart Error:", str(e))
        return None


# Gradio UI
def build_dashboard():
    with gr.Blocks() as demo:
        gr.Markdown("# 📊 Mini Pro-Level Data Dashboard")

        with gr.Row():
            file_input = gr.File(label="📂 Upload CSV or Excel", type="filepath")
            clean_method = gr.Radio(["Drop missing values", "Fill numeric with median", "Fill categorical with mode"],
                                    label="🧹 Cleaning Method")
            clean_btn = gr.Button("🧼 Clean Data")

        cleaned_table = gr.Dataframe(label="🧾 Cleaned Data Preview", interactive=False)

        with gr.Row():
            filter_input = gr.Textbox(label="🔍 Filter Query (e.g., Price > 500 and Rating >= 4)")
            filter_btn = gr.Button("Apply Filter")

        filtered_table = gr.Dataframe(label="📊 Filtered Data Preview", interactive=False)

        download_btn = gr.Button("⬇️ Download CSV")
        download_file = gr.File(label="📁 Your CSV File")

        with gr.Row():
            x_axis = gr.Textbox(label="X-axis Column")
            y_axis = gr.Textbox(label="Y-axis Column (leave blank for Pie)")
            chart_type = gr.Radio(["Bar", "Line", "Pie"], label="📈 Chart Type")
            chart_btn = gr.Button("📊 Generate Chart")

        chart_output = gr.Image(label="📊 Chart Preview")

        clean_btn.click(fn=clean_data, inputs=[file_input, clean_method], outputs=cleaned_table)
        filter_btn.click(fn=filter_data, inputs=filter_input, outputs=filtered_table)
        download_btn.click(fn=download_data, inputs=None, outputs=download_file)
        chart_btn.click(fn=generate_chart, inputs=[x_axis, y_axis, chart_type], outputs=chart_output)

    return demo


build_dashboard().launch()
