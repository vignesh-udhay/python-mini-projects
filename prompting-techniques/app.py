import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def determine_technique_and_transform(prompt):
    """Use LLM to determine the best technique and generate a transformed prompt."""
    system_prompt = """You are an expert in prompt engineering. Your task is to:
1. Analyze the given prompt
2. Choose the most appropriate prompting technique from: Zero-Shot, Few-Shot, Chain-of-Thought, Self-Consistency, Tree of Thoughts, or Meta Prompting
3. Transform the prompt using the chosen technique

Return your response in this exact format:
TECHNIQUE: [chosen technique]
TRANSFORMED_PROMPT: [your transformed prompt]"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        response = completion.choices[0].message.content
        
        # Parse the response to extract technique and transformed prompt
        lines = response.split('\n')
        technique = None
        transformed_prompt = None
        
        for line in lines:
            if line.startswith('TECHNIQUE:'):
                technique = line.replace('TECHNIQUE:', '').strip()
            elif line.startswith('TRANSFORMED_PROMPT:'):
                transformed_prompt = line.replace('TRANSFORMED_PROMPT:', '').strip()
        
        if not technique or not transformed_prompt:
            raise ValueError("LLM response format was incorrect")
            
        return technique, transformed_prompt
        
    except Exception as e:
        return "Zero-Shot", f"Error in technique selection: {str(e)}"

def get_llm_response(prompt):
    """Get response from Groq LLM using the best technique determined by another LLM call."""
    # First, determine the best technique and get transformed prompt
    technique, transformed_prompt = determine_technique_and_transform(prompt)
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Provide a clear and detailed response."},
                {"role": "user", "content": transformed_prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content, technique, transformed_prompt
    except Exception as e:
        return f"Error: {str(e)}", technique, transformed_prompt

# Define the Gradio interface
with gr.Blocks(title="Prompting Playground") as demo:
    gr.Markdown("# 🎮 Prompting Playground")
    gr.Markdown("Enter your prompt and let the AI choose the best prompting technique!")
    
    with gr.Row():
        with gr.Column():
            prompt_input = gr.Textbox(
                label="Enter your prompt",
                placeholder="e.g., 'Solve the equation: 2x + 5 = 15' or 'Explain how photosynthesis works'",
                lines=3
            )
            submit_btn = gr.Button("Generate Response", variant="primary")
        
        with gr.Column():
            technique_output = gr.Textbox(
                label="Selected Technique",
                lines=1,
                interactive=False
            )
            transformed_prompt_output = gr.Textbox(
                label="Transformed Prompt",
                lines=3,
                interactive=False
            )
            response_output = gr.Textbox(
                label="AI Response",
                lines=8,
                interactive=False
            )
    
    def generate_response(prompt):
        if not prompt:
            return "Please enter a prompt", "No technique selected", "No transformed prompt"
        
        response, technique, transformed_prompt = get_llm_response(prompt)
        return response, f"Using technique: {technique}", transformed_prompt
    
    submit_btn.click(
        fn=generate_response,
        inputs=[prompt_input],
        outputs=[response_output, technique_output, transformed_prompt_output]
    )

if __name__ == "__main__":
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY environment variable is not set")
    
    # Run the Gradio app
    demo.launch() 