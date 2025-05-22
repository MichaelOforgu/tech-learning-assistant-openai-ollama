import os
from openai import OpenAI
import ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# System prompt for consistent responses
SYSTEM_PROMPT = """You are an assistant answering technical questions for beginners. Use simple language,
avoid jargon, and explain concepts step-by-step. Use analogies and examples to clarify ideas.
Summarize key points at the end and invite follow-up questions. Format all responses in Markdown.
Make learning clear, accessible, and engaging."""

def get_openai_response(question):
    """Get response from OpenAI's GPT model"""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=MODEL_GPT,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error with OpenAI: {str(e)}"

def get_ollama_response(question):
    """Get response from Ollama's Llama model"""
    try:
        response = ollama.chat(
            model=MODEL_LLAMA,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error with Ollama: {str(e)}" 