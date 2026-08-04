import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Validate that the API key is set
if not openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please add your OpenAI API key to the .env file."
    )

# Set the OpenAI API key in environment for CrewAI to use
os.environ["OPENAI_API_KEY"] = openai_api_key


# -----------------------------
# OpenAI LLM
# -----------------------------
llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.7
)


# -----------------------------
# Agent 1: Destination Researcher
# -----------------------------
destination_researcher = Agent(
    role="Destination Researcher",

    goal=(
        "Research the destination and identify the best attractions, "
        "activities, food experiences, and travel recommendations."
    ),

    backstory=(
        "You are an experienced travel researcher who knows how to "
        "identify the best places and experiences for travelers."
    ),

    llm=llm,
    verbose=True
)


# -----------------------------
# Agent 2: Itinerary Planner
# -----------------------------
itinerary_planner = Agent(
    role="Travel Itinerary Planner",

    goal=(
        "Create a practical day-by-day travel itinerary based on "
        "the destination research."
    ),

    backstory=(
        "You are an expert travel planner who creates realistic "
        "and enjoyable travel itineraries."
    ),

    llm=llm,
    verbose=True
)


# -----------------------------
# Agent 3: Budget Analyst
# -----------------------------
budget_analyst = Agent(
    role="Travel Budget Analyst",

    goal=(
        "Analyze the travel plan and estimate the cost of flights, "
        "hotels, food, transportation, and activities."
    ),

    backstory=(
        "You are a financial travel expert who helps travelers "
        "stay within their budget."
    ),

    llm=llm,
    verbose=True
)


# -----------------------------
# Task 1
# -----------------------------
research_task = Task(
    description="""
    Research the following travel request:

    Destination: {destination}
    Duration: {duration}
    Budget: {budget}
    Traveler Preferences: {preferences}

    Identify:
    - Top attractions
    - Popular activities
    - Local experiences
    - Recommended areas to stay
    - Important travel considerations
    """,

    expected_output="""
    A detailed destination research report containing:
    - Top attractions
    - Activities
    - Recommended areas
    - Local experiences
    - Travel recommendations
    """,

    agent=destination_researcher
)


# -----------------------------
# Task 2
# -----------------------------
itinerary_task = Task(
    description="""
    Using the destination research from the previous task, create
    a day-by-day travel itinerary.

    Destination: {destination}
    Duration: {duration}
    Traveler Preferences: {preferences}

    The itinerary should:
    - Organize activities by day
    - Group nearby attractions together
    - Include reasonable travel time
    - Include food and relaxation time
    - Avoid an unrealistic schedule
    """,

    expected_output="""
    A complete day-by-day travel itinerary with:
    - Morning activities
    - Afternoon activities
    - Evening activities
    - Food recommendations
    - Travel considerations
    """,

    agent=itinerary_planner
)


# -----------------------------
# Task 3
# -----------------------------
budget_task = Task(
    description="""
    Analyze the proposed itinerary and estimate the total travel cost.

    Budget: {budget}

    Include estimated costs for:
    - Flights
    - Accommodation
    - Food
    - Local transportation
    - Activities
    - Miscellaneous expenses

    Compare the estimated cost with the available budget.
    If the plan exceeds the budget, suggest cost-saving alternatives.
    """,

    expected_output="""
    A detailed budget breakdown in Indian Rupees (₹), including:
    - Estimated cost by category
    - Total estimated cost
    - Comparison with the available budget
    - Suggestions to reduce costs if necessary
    """,

    agent=budget_analyst
)


# -----------------------------
# Create Crew
# -----------------------------
travel_crew_sequential = Crew(
    agents=[
        destination_researcher,
        itinerary_planner,
        budget_analyst
    ],

    tasks=[
        research_task,
        itinerary_task,
        budget_task
    ],

    process=Process.sequential,

    verbose=True
)
