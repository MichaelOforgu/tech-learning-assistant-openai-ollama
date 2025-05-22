import gradio as gr
from technical_assistant import get_openai_response, get_ollama_response
import socket

def find_available_port(start_port=7860, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def process_question(question, model_choice):
    """Process the question using the selected model"""
    if model_choice == "OpenAI (GPT-4o-mini)":
        return get_openai_response(question)
    else:
        return get_ollama_response(question)

# Create Gradio interface
with gr.Blocks(title="Technical Learning Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Technical Learning Assistant 🤖")
    gr.Markdown("""
    Welcome to the Technical Learning Assistant! This tool helps you understand technical concepts through clear, 
    beginner-friendly explanations. Choose your preferred AI model and ask any technical question.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            question = gr.Textbox(
                label="Your Technical Question",
                placeholder="Enter your question here...",
                lines=5
            )
            model_choice = gr.Radio(
                choices=["OpenAI (GPT-4o-mini)", "Ollama (Llama 3.2)"],
                label="Choose Model",
                value="OpenAI (GPT-4o-mini)",
                info="OpenAI requires an API key, while Ollama runs locally"
            )
            submit_btn = gr.Button("Get Answer", variant="primary")
        
        with gr.Column(scale=2):
            answer = gr.Markdown(
                label="Answer",
                show_label=False,
                elem_classes=["answer-box"]
            )
    
    # Add some example questions
    gr.Examples(
        examples=[
            "What is the difference between a list and a tuple in Python?",
            "Explain how HTTP requests work in simple terms",
            "What is the purpose of a virtual environment in Python?",
            "How does a database index work?"
        ],
        inputs=question
    )
    
    submit_btn.click(
        fn=process_question,
        inputs=[question, model_choice],
        outputs=answer
    )

if __name__ == "__main__":
    # Find an available port
    port = find_available_port()
    if port is None:
        print("Error: Could not find an available port. Please try again later.")
        exit(1)
    
    print(f"Starting server on port {port}...")
    demo.launch(
        share=False,  # Set to True if you want to create a public link
        server_name="0.0.0.0",  # Makes the server accessible from other devices
        server_port=port  # Use the found available port
    ) 