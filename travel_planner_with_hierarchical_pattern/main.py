"""
Travel Planner Multi-Agent System - Hierarchical Pattern
=========================================================

This script demonstrates a hierarchical multi-agent travel planning system using CrewAI.

Architecture:
- Level 1: Travel Coordinator (orchestrates the process)
- Level 2: Specialized Teams
  - Research Team (Attractions, Food, Accommodation) - runs in parallel
  - Planning Team (Itinerary, Logistics) - runs sequentially
  - Financial Team (Budget Analysis)

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
    print("📊 Organizational Structure:")
    print("  L1: Travel Coordinator")
    print("  ├── L2A: Research Team (Parallel)")
    print("  │   ├── Attraction Specialist")
    print("  │   ├── Food Specialist")
    print("  │   └── Accommodation Specialist")
    print("  ├── L2B: Planning Team (Sequential)")
    print("  │   ├── Itinerary Planner")
    print("  │   └── Logistics Manager")
    print("  └── L2C: Financial Team")
    print("      └── Budget Analyst")
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
