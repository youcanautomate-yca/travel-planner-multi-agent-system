"""
Travel Planner Multi-Agent System - Hierarchical Pattern
=========================================================

This script demonstrates a hierarchical multi-agent travel planning system using CrewAI.

Architecture:
- Manager Agent: Senior Travel Manager who coordinates all specialists
- Specialist Agents: Attraction Researcher, Hotel Researcher, Food Researcher, 
                     Travel Planner, Budget Analyst
- Process: Hierarchical - Manager delegates to specialists and synthesizes outputs

Setup:
1. Add your OpenAI API key to the .env file:
   OPENAI_API_KEY=sk-your_api_key_here

2. Install dependencies:
   pip install -r requirements.txt

3. Run this script:
   python main.py
"""

from travel_planner_with_hierarchical_pattern.agents_tasks.agents_tasks import travel_crew_hierarchical


def main():
    """Run the hierarchical travel planning crew"""
    print("🧳 Travel Planner Multi-Agent System - Hierarchical Pattern")
    print("=" * 70)
    print()
    print("📊 Manager-based Hierarchy:")
    print("  Manager: Senior Travel Manager")
    print("  ├── Specialists (coordinated by manager):")
    print("  │   ├── Attraction Researcher")
    print("  │   ├── Hotel Researcher")
    print("  │   ├── Food Researcher")
    print("  │   ├── Travel Planner")
    print("  │   └── Budget Analyst")
    print()
    print("=" * 70)
    print()
    
    # Run the crew with sample inputs
    result = travel_crew_hierarchical.kickoff(
        inputs={
            "destination": "Paris",
            "duration": "7 days",
            "budget": "₹2,00,000",
            "preferences": (
                "History, culture, food, photography, and popular landmarks"
            )
        }
    )
    
    print("\n")
    print("=" * 70)
    print("✈️  FINAL HIERARCHICAL TRAVEL PLAN")
    print("=" * 70)
    print(result)


if __name__ == '__main__':
    main()
