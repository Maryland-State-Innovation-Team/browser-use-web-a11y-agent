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

async def run_accessibility_audit(url: str):
    """
    Spins up a Browser Agent to audit the specific URL for WCAG 2.1 AA / ADA Title II compliance.
    """
    print(f"Starting Accessibility Audit for: {url}")
    print("Agent is initializing as a keyboard-only screen reader user...")

    # Initialize the LLM
    llm = ChatGoogle(model=MODEL_NAME)

    # Define the Audit Task based on the provided DoIT Report examples
    task = f"""
    You are an expert Accessibility Auditor and QA Tester.
    Your goal is to audit the website {url} for WCAG 2.1 AA and ADA Title II violations.
    
    You must simulate the behavior of a **Keyboard-Only User** using a **Screen Reader**.
    
    ### EXECUTION STEPS:
    1. **Navigate to the URL.**
    2. **Keyboard Navigation Test:** - Do NOT use the mouse to click links initially. Use the 'Tab' key to move focus.
       - Verify if a "Skip to Main Content" link appears.
       - Verify if the visual focus indicator is visible on all interactive elements.
       - Check if the tab order is logical.
    3. **Screen Reader Simulation:**
       - Inspect images. Do they have 'alt' text? Is the alt text descriptive or just "image"?.
       - Check buttons. Do buttons like "X" or "Menu" have aria-labels (e.g., "Close Menu")?.
       - Check form fields. Do inputs have associated <label> tags or aria-labels?.
    4. **Dynamic Content Check:**
       - If there are modals, check if focus is trapped inside them when open.
       - If search results load dynamically, check if an 'aria-live' region announces the result count.
    
    ### REPORTING:
    Once you have explored the page and tested these elements, compile a **Final Audit Report**.
    Output a readable text report with the following sections:
    
    - **Executive Summary**: A brief overview of the site's accessibility.
    - **Critical Issues (High Severity)**: Issues that block access (e.g., Keyboard traps, missing form labels, no skip link).
    - **Major Issues (Medium Severity)**: Issues that hinder experience (e.g., Poor alt text, confusing tab order, low contrast text).
    - **Minor Issues (Low Severity)**: Best practice violations (e.g., Skipped heading levels).
    
    Be specific. If you find a button missing a label, describe *which* button it is.
    """

    # Initialize the Agent
    agent = Agent(
        task=task,
        llm=llm,
        controller=Controller(),
        use_vision=True  # Crucial for detecting visual focus indicators and contrast issues
    )

    try:
        # Run the agent 
        history = await agent.run(max_steps=200)
        
        # Get the final result from the agent's history
        result = history.final_result()
        
        print("\n" + "="*60)
        print("ACCESSIBILITY AUDIT REPORT")
        print("="*60 + "\n")
        print(result)
        print("\n" + "="*60)

    except Exception as e:
        print(f"An error occurred during the audit: {e}")

if __name__ == "__main__":
    target_url = get_target_url()
    asyncio.run(run_accessibility_audit(target_url))
