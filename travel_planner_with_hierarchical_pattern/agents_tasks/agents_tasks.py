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
    Coordinate all travel specialists
    and create the best travel plan.
    """,

    backstory="""
    You are a senior travel consultant.

    You never solve everything yourself.

    Instead you decide which specialist
    should perform each task.

    You combine all specialist outputs
    into a complete travel plan.
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

    Your role:
    1. Delegate attraction research to the Attraction Researcher
    2. Delegate accommodation research to the Hotel Researcher
    3. Delegate food research to the Food Researcher
    4. Delegate itinerary creation to the Travel Planner
    5. Delegate budget analysis to the Budget Analyst
    
    After gathering all information, synthesize it into a comprehensive travel plan.
    """,

    expected_output="Complete and detailed travel itinerary",

    agent=manager
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
