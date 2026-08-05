import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.7
)

# -------------------------------------------------
# Agents
# -------------------------------------------------

manager = Agent(
    role="Senior Travel Manager",
    goal="""
    Analyze travel requests, decide which specialists should work,
    coordinate their work, validate the results,
    and deliver the best travel plan.
    """,
    backstory="""
    You are the team leader of an AI travel agency.

    You never perform specialist work yourself.

    Instead, you:
    - Understand the customer's request
    - Decide which expert should handle each task
    - Review the quality of every response
    - Request additional work when necessary
    - Combine everything into one final travel plan
    """,
    llm=llm,
    verbose=True,
    allow_delegation=True
)

attraction_agent = Agent(
    role="Attraction Researcher",
    goal="Find the best tourist attractions",
    backstory="Expert in famous tourist attractions around the world.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

hotel_agent = Agent(
    role="Hotel Researcher",
    goal="Recommend the best hotels and areas to stay",
    backstory="Travel accommodation expert.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

food_agent = Agent(
    role="Food Researcher",
    goal="Find famous restaurants and local cuisine",
    backstory="Expert in food and culinary experiences.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

itinerary_agent = Agent(
    role="Travel Planner",
    goal="Create the best itinerary",
    backstory="Experienced travel planner.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

budget_agent = Agent(
    role="Budget Analyst",
    goal="Estimate total travel cost",
    backstory="Financial expert for travel planning.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# -------------------------------------------------
# Manager Task
# -------------------------------------------------

travel_task = Task(
    description="""
    Plan a complete trip to {destination}.

    Duration: {duration}
    Budget: {budget}
    Preferences: {preferences}
    """,
    expected_output="A complete travel plan including itinerary, accommodation, food recommendations and budget analysis."
)


# -------------------------------------------------
# Crew
# -------------------------------------------------

travel_crew_hierarchical = Crew(
    agents=[
        attraction_agent,
        hotel_agent,
        food_agent,
        itinerary_agent,
        budget_agent

    ],
    manager_agent= manager,
    tasks=[
        travel_task
    ],
    process=Process.hierarchical,
    verbose=True
)
