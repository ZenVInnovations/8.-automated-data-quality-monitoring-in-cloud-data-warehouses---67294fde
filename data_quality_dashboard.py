import gradio as gr
import pandas as pd
import great_expectations as ge
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import io
import socket
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def find_free_port(start_port=7860, max_port=7960):
    """Find a free port in the given range."""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    raise OSError(f"No free ports found in range {start_port}-{max_port}")

def analyze_data_quality(file):
    """
    Analyze data quality of uploaded CSV file using Great Expectations
    """
    try:
        # Read the uploaded file
        df = pd.read_csv(file.name)
        
        # Basic data validation
        if df.empty:
            return (
                {"Error": "The uploaded file is empty"},
                "Error: Empty file",
                None
            )
        
        # Convert to Great Expectations DataFrame
        ge_df = ge.from_pandas(df)
        
        # Add basic expectations
        expectations = [
            ge_df.expect_column_values_to_not_be_null(column) 
            for column in df.columns
        ]
        expectations.extend([
            ge_df.expect_column_values_to_be_unique(df.columns[0]),  # Assume first column is ID
            ge_df.expect_table_row_count_to_be_between(1, 1000000)
        ])
        
        # Validate expectations
        results = ge_df.validate()
        
        # Generate missing values visualization
        plt.figure(figsize=(10, 6))
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            sns.barplot(x=missing.values, y=missing.index)
            plt.title("Missing Values per Column")
            plt.xlabel("Count")
            plt.ylabel("Column")
        else:
            plt.text(0.5, 0.5, "No Missing Values Found!", ha='center', va='center')
        
        # Save plot to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        # Generate summary
        summary = {
            "Total Rows": len(df),
            "Total Columns": len(df.columns),
            "Missing Values": df.isnull().sum().sum(),
            "Duplicate Rows": df.duplicated().sum(),
            "Validation Success": results["success"],
            "Analysis Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Format validation results
        validation_details = []
        for result in results["results"]:
            validation_details.append(
                f"- {result['expectation_config']['expectation_type']}: "
                f"{'✅ Passed' if result['success'] else '❌ Failed'}"
            )
        
        return (
            summary,
            "\n".join(validation_details),
            buf
        )
        
    except Exception as e:
        logging.error(f"Error in analyze_data_quality: {str(e)}")
        return (
            {"Error": str(e)},
            f"Error occurred during analysis: {str(e)}",
            None
        )

def create_interface():
    """Create and configure the Gradio interface"""
    with gr.Blocks(title="Data Quality Monitor") as demo:
        gr.Markdown("# Data Quality Monitoring Dashboard")
        gr.Markdown("Upload a CSV file to analyze its data quality")
        
        with gr.Row():
            file_input = gr.File(label="Upload CSV File", file_types=[".csv"])
        
        with gr.Row():
            analyze_btn = gr.Button("Analyze Data Quality", variant="primary")
        
        with gr.Row():
            with gr.Column():
                summary_output = gr.JSON(label="Summary Statistics")
                validation_output = gr.Textbox(label="Validation Results", lines=10)
            with gr.Column():
                plot_output = gr.Image(label="Missing Values Visualization")
        
        analyze_btn.click(
            analyze_data_quality,
            inputs=[file_input],
            outputs=[summary_output, validation_output, plot_output]
        )
        
        return demo

if __name__ == "__main__":
    try:
        # Find an available port
        port = find_free_port()
        logging.info(f"Starting server on port {port}")
        
        # Create and launch the interface
        demo = create_interface()
        demo.launch(
            server_name="0.0.0.0",
            server_port=port,
            share=False,
            show_error=True,
            favicon_path=None,
            quiet=True
        )
    except Exception as e:
        logging.error(f"Failed to start server: {str(e)}")
        print(f"Error: {str(e)}") 