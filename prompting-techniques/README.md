# 🎮 Prompting Playground

A web application that intelligently selects and applies the best prompting technique for your input using the Groq LLM API.

## Features

- Input any prompt and let the AI choose the optimal prompting technique
- Automatic technique selection from:
  - Zero-Shot Prompting: Direct instruction without examples
  - Few-Shot Prompting: Guided by example patterns
  - Chain-of-Thought (CoT): Step-by-step reasoning
  - Self-Consistency: Multiple reasoning paths with consistency check
  - Tree of Thoughts (ToT): Multiple reasoning paths in a tree structure
  - Meta Prompting: Focus on structural and syntactical aspects
- Clean and intuitive Gradio interface
- Powered by Groq's Llama 3.3 70B model for high-quality responses

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
   You can get your API key from [Groq Cloud](https://console.groq.com/)

## Usage

1. Run the application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (usually http://127.0.0.1:7860)
3. Enter your prompt in the text box
4. Click "Generate Response" to see:
   - The selected prompting technique
   - The transformed prompt
   - The AI's response

## Example Prompts

- "Solve the equation: 2x + 5 = 15"
- "Explain how photosynthesis works"
- "Write a short poem about artificial intelligence"
- "Analyze the pros and cons of remote work"

## Prompting Techniques Explained

1. **Zero-Shot Prompting**

   - Direct instruction without examples
   - Relies on model's pre-trained knowledge
   - Best for straightforward tasks

2. **Few-Shot Prompting**

   - Includes example patterns
   - Enables in-context learning
   - Useful for consistent formatting

3. **Chain-of-Thought (CoT)**

   - Step-by-step reasoning
   - Breaks down complex problems
   - Shows intermediate thinking

4. **Self-Consistency**

   - Multiple reasoning paths
   - Selects most consistent answer
   - Improves reliability

5. **Tree of Thoughts (ToT)**

   - Multiple reasoning branches
   - Strategic lookahead
   - Explores different approaches

6. **Meta Prompting**
   - Focuses on task structure
   - Analyzes input/output types
   - Provides structured solutions

## Technical Details

- Built with Python and Gradio
- Uses Groq's Llama 3.3 70B model for both technique selection and response generation
- Implements a two-step process:
  1. First LLM call determines the best prompting technique
  2. Second LLM call generates the final response using the selected technique

## Note

Make sure you have a valid Groq API key and sufficient credits in your account to use the application.
