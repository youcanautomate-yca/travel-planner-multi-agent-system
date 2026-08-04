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

attraction_agent = Agent(
    role="Attraction Researcher",
    goal="Find the best tourist attractions",
    backstory="Expert in famous tourist attractions around the world.",
    llm=llm,
    verbose=True
)

hotel_agent = Agent(
    role="Hotel Researcher",
    goal="Recommend the best hotels and areas to stay",
    backstory="Travel accommodation expert.",
    llm=llm,
    verbose=True
)

food_agent = Agent(
    role="Food Researcher",
    goal="Find famous restaurants and local cuisine",
    backstory="Expert in food and culinary experiences.",
    llm=llm,
    verbose=True
)

itinerary_agent = Agent(
    role="Travel Planner",
    goal="Create the best itinerary",
    backstory="Experienced travel planner.",
    llm=llm,
    verbose=True
)

budget_agent = Agent(
    role="Budget Analyst",
    goal="Estimate total travel cost",
    backstory="Financial expert for travel planning.",
    llm=llm,
    verbose=True
)

# -------------------------------------------------
# Parallel Tasks
# -------------------------------------------------

attraction_task = Task(
    description="""
Research the top attractions in {destination}.

Include:
- Must visit places
- Hidden gems
- Best time to visit
""",
    expected_output="List of attractions",
    agent=attraction_agent,
    async_execution=True
)

hotel_task = Task(
    description="""
Find the best hotels and areas to stay in {destination}.

Include:
- Luxury
- Mid-range
- Budget hotels
""",
    expected_output="Hotel recommendations",
    agent=hotel_agent,
    async_execution=True
)

food_task = Task(
    description="""
Research local food in {destination}.

Include:
- Famous restaurants
- Local dishes
- Street food
""",
    expected_output="Food recommendations",
    agent=food_agent,
    async_execution=True
)

# -------------------------------------------------
# Dependent Task
# -------------------------------------------------

itinerary_task = Task(
    description="""
Using all previous research, create a detailed
day-by-day itinerary.

Duration : {duration}
Preferences : {preferences}
""",
    expected_output="Complete itinerary",
    agent=itinerary_agent,
    context=[
        attraction_task,
        hotel_task,
        food_task
    ]
)

budget_task = Task(
    description="""
Estimate total travel cost.

Budget : {budget}

Include:

- Flights
- Hotels
- Food
- Local transport
- Activities

Compare estimated cost with available budget.
""",
    expected_output="Detailed budget report",
    agent=budget_agent,
    context=[itinerary_task]
)

# -------------------------------------------------
# Crew
# -------------------------------------------------

travel_crew_parallel = Crew(
    agents=[
        attraction_agent,
        hotel_agent,
        food_agent,
        itinerary_agent,
        budget_agent
    ],
    tasks=[
        attraction_task,
        hotel_task,
        food_task,
        itinerary_task,
        budget_task
    ],
    process=Process.sequential,
    verbose=True
)
