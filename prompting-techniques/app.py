import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv
from system_prompt import system_prompt;

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def determine_technique_and_transform(prompt):
    """Use LLM to determine the best technique and generate a transformed prompt."""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        response = completion.choices[0].message.content
        
        # Parse the response to extract technique and transformed prompt
        lines = response.split('\n')
        technique = None
        transformed_prompt = None
        
        # First pass: Look for exact matches
        for line in lines:
            if line.startswith('TECHNIQUE:'):
                technique = line.replace('TECHNIQUE:', '').strip()
            elif line.startswith('TRANSFORMED_PROMPT:'):
                transformed_prompt = line.replace('TRANSFORMED_PROMPT:', '').strip()
        
        # Second pass: If not found, look for case-insensitive matches
        if not technique or not transformed_prompt:
            for line in lines:
                if 'technique:' in line.lower():
                    technique = line.split(':', 1)[1].strip()
                elif 'transformed_prompt:' in line.lower():
                    transformed_prompt = line.split(':', 1)[1].strip()
        
        # If still not found, try to infer from the response
        if not technique:
            # Default to Zero-Shot if we can't determine the technique
            technique = "Zero-Shot"
            
        if not transformed_prompt:
            # Use the original prompt if we can't find a transformed version
            transformed_prompt = prompt
            
        return technique, transformed_prompt
        
    except Exception as e:
        print(f"Error in determine_technique_and_transform: {str(e)}")
        return "Zero-Shot", prompt

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
            
            # Add example prompts section
            gr.Markdown("### Example Prompts to Try")
            gr.Markdown("""
            **Zero-Shot Examples:**
            - Translate 'Hello, how are you?' into French
            - Summarize the process of photosynthesis
            - Convert 25°C to Fahrenheit
            
            **Few-Shot Examples:**
            - Fix the grammar: 'They is going to the store'
            - Complete the pattern: 2, 4, 8, 16, __
            - Convert these sentences to past tense: 'She walks to school'
            
            **Chain-of-Thought Examples:**
            - If a train travels 120 km in 2 hours, what's its speed in m/s?
            - Calculate 15% of 200
            - Solve: If x + 5 = 12, what is 2x + 3?
            
            **Tree of Thoughts Examples:**
            - How can we reduce plastic waste in cities?
            - What are the pros and cons of remote work?
            - How can we improve public transportation?
            
            **Meta Prompting Examples:**
            - Make this more creative: 'Write a story about a robot'
            - Rewrite this to be more engaging: 'Explain how a car works'
            - Transform this into a riddle: 'The sun rises in the east'
            """)
        
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