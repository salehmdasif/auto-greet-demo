import gradio as gr
import pandas as pd


def process_data(file, selected_cols, filter_condition):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file.name)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file.name)
        else:
            return "❌ Unsupported file format."

        msg = f"Original Shape: {df.shape}\n"

        # Column Selection
        if selected_cols:
            df = df[selected_cols]
            msg += f"Selected Columns: {selected_cols}\n"

        # Filter
        if filter_condition:
            try:
                df = df.query(filter_condition)
                msg += f"Filter Applied: {filter_condition}\n"
            except Exception as e:
                return f"❌ Filter Error: {str(e)}"
        return df



    except Exception as e:
        return f"❌ Error: {str(e)}"


# Helper to extract columns
def get_columns(file):
    try:
        if file is None:
            return gr.CheckboxGroup.update(choices=[], value=[])

        filepath = file.name if hasattr(file, "name") else file

        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        elif filepath.endswith(".xlsx"):
            df = pd.read_excel(filepath)
        else:
            return gr.CheckboxGroup.update(choices=[], value=[])

        return gr.CheckboxGroup.update(choices=list(df.columns), value=list(df.columns))

    except Exception as e:
        print("❌ Error loading columns:", str(e))
        return gr.CheckboxGroup.update(choices=[], value=[])


# Build UI
with gr.Blocks() as demo:
    gr.Markdown("### 🧪 Step 3.2 – Column Selection & Filtering")

    file_input = gr.File(label="📂 Upload CSV/Excel", type="filepath")
    column_selector = gr.CheckboxGroup(label="📌 Select Columns (optional)", interactive=True)
    filter_input = gr.Textbox(label="🔍 Filter (e.g. Price > 500 and Rating >= 4)")
    output_box = gr.Dataframe(label="📊 Filtered Data Preview", interactive=False)

    file_input.change(fn=get_columns, inputs=file_input, outputs=column_selector)
    run_btn = gr.Button("✅ Run Filter")
    run_btn.click(fn=process_data, inputs=[file_input, column_selector, filter_input], outputs=output_box)

demo.launch()
