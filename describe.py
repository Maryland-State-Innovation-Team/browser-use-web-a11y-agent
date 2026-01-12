import asyncio
import sys
import os
from dotenv import load_dotenv
from browser_use import Agent, Controller, ChatGoogle

# Load environment variables (Expects GOOGLE_API_KEY)
load_dotenv()

# --- Configuration ---
MODEL_NAME = "gemini-3-flash-preview"

def get_target_url():
    """Parses command line arguments to get the target URL."""
    if len(sys.argv) < 2:
        print("Usage: python audit.py <URL>")
        sys.exit(1)
    return sys.argv[1]

async def run_enhanced_description(url: str):
    """
    Spins up a Browser Agent to provide a rich, synthesized visual description of the URL,
    focusing on information unavailable to standard screen readers.
    """
    print(f"Starting Enhanced Visual Description for: {url}")
    print("Agent is initializing as a Visual Interpreter...")

    # Initialize the LLM
    llm = ChatGoogle(model=MODEL_NAME)

    # Define the Description Task
    task = f"""
    You are an expert Visual Interpreter and AI Describer for the visually impaired.
    Your goal is to explore the website {url} and provide a rich, high-level description of visual elements, context, and data synthesis that a standard screen reader cannot provide.
    
    ### CORE OBJECTIVES:
    Do NOT simply read the text on the page. A screen reader already does that.
    Instead, focus on the "Visual Story" and "Synthesis."
    
    1. **Data Visualization & Infographics (High Priority):**
       - If you encounter charts, graphs, or infographics, do not just read the data points.
       - **Trends:** Describe the overall movement (e.g., "A steady upward trend over the last 5 years").
       - **Relationships:** Explain how variables interact (e.g., "As price increases, demand drops sharply").
       - **Comparisons:** Highlight the winners/losers or biggest slices of the pie.
       - **Outliers:** Note anything that breaks the pattern.
    
    2. **Visual Hierarchy & Layout:**
       - What draws the eye first? (e.g., "A massive hero image dominates the top half").
       - How is information grouped? (e.g., "A three-column card layout suggesting equal importance among features").
       - Describe the usage of white space and density.
    
    3. **Atmosphere & Branding:**
       - Describe the color palette and what emotion it conveys (e.g., "Clinical and clean blue/white" vs. "Energetic and dark").
       - Describe the style of imagery (e.g., "Abstract vector art" vs. "Candid photography").
    
    4. **Complex UI Elements:**
       - If there is a progress stepper, dashboard, or map, describe its state and complexity visually, not just its labels.
    
    ### EXECUTION STEPS:
    1. Navigate to the URL.
    2. Scroll through the page to capture the full visual context.
    3. Analyze any specific charts or hero sections in detail.
    
    ### REPORTING:
    Compile a **Descriptive Summary** using the following structure:
    
    - **Visual Overview**: A quick summary of the page's look, feel, and purpose.
    - **Key Visual Insights**:
        - **Data Stories**: (Synthesis of charts/graphs found).
        - **Imagery Analysis**: (Description of photos/icons and their context).
    - **Layout & Navigation Flow**: How the page guides the user's eye visually.
    - **Hidden Context**: Details a blind user would miss (e.g., "The 'Sign Up' button is highlighted in bright red, indicating urgency").
    """

    # Initialize the Agent
    agent = Agent(
        task=task,
        llm=llm,
        controller=Controller(),
        use_vision=True  # Essential for interpreting charts and layout
    )

    try:
        # Run the agent 
        history = await agent.run(max_steps=200)
        
        # Get the final result from the agent's history
        result = history.final_result()
        
        print("\n" + "="*60)
        print("VISUAL DESCRIPTION REPORT")
        print("="*60 + "\n")
        print(result)
        print("\n" + "="*60)

    except Exception as e:
        print(f"An error occurred during the description generation: {e}")

if __name__ == "__main__":
    target_url = get_target_url()
    asyncio.run(run_enhanced_description(target_url))
