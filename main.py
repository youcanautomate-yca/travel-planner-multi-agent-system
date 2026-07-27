"""
Travel Planner Multi-Agent System
==================================

This script runs a multi-agent travel planning system using CrewAI.

Setup:
1. Add your OpenAI API key to the .env file:
   OPENAI_API_KEY=sk-your_api_key_here

2. Install dependencies:
   pip install -r requirements.txt

3. Run this script:
   python main.py
"""

from agents.travel_agents import travel_crew


def main():
    """Run the travel planning crew"""
    print("🧳 Travel Planner Multi-Agent System")
    print("=" * 60)
    print()
    
    # Run the crew with sample inputs
    result = travel_crew.kickoff(
        inputs={
            "destination": "Paris",
            "duration": "7 days",
            "budget": "₹1,50,000",
            "preferences": (
                "History, culture, food, photography, and popular landmarks"
            )
        }
    )
    
    print("\n")
    print("=" * 60)
    print("✈️  FINAL TRAVEL PLAN")
    print("=" * 60)
    print(result)


if __name__ == '__main__':
    main()
