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
# TOP LEVEL: Coordinator Agent
# -------------------------------------------------
travel_coordinator = Agent(
    role="Travel Coordinator",
    goal=(
        "Orchestrate the travel planning process by delegating to specialized "
        "teams and synthesizing their outputs into a comprehensive travel plan."
    ),
    backstory=(
        "You are an experienced travel coordinator who manages multiple "
        "specialized teams to create perfect travel experiences."
    ),
    llm=llm,
    verbose=True
)

# -------------------------------------------------
# LEVEL 2A: Research Team Agents
# -------------------------------------------------
attraction_specialist = Agent(
    role="Attraction Specialist",
    goal="Research and identify the best attractions for the destination",
    backstory="Expert in identifying must-see attractions and hidden gems.",
    llm=llm,
    verbose=True
)

food_specialist = Agent(
    role="Food & Cuisine Specialist",
    goal="Find the best local food experiences and restaurants",
    backstory="Culinary expert specializing in local and international cuisines.",
    llm=llm,
    verbose=True
)

accommodation_specialist = Agent(
    role="Accommodation Specialist",
    goal="Recommend the best hotels and areas to stay",
    backstory="Accommodation expert with knowledge of different lodging options.",
    llm=llm,
    verbose=True
)

# -------------------------------------------------
# LEVEL 2B: Planning Team Agents
# -------------------------------------------------
itinerary_planner = Agent(
    role="Itinerary Planner",
    goal="Create a well-organized day-by-day travel itinerary",
    backstory="Expert travel planner with experience in diverse destinations.",
    llm=llm,
    verbose=True
)

logistics_manager = Agent(
    role="Logistics Manager",
    goal="Handle transportation and logistical aspects of the trip",
    backstory="Logistics expert in travel planning and transportation.",
    llm=llm,
    verbose=True
)

# -------------------------------------------------
# LEVEL 2C: Financial Team Agent
# -------------------------------------------------
budget_analyst = Agent(
    role="Budget Analyst",
    goal="Analyze and optimize the travel budget",
    backstory="Financial expert specializing in travel cost analysis.",
    llm=llm,
    verbose=True
)

# -------------------------------------------------
# COORDINATOR TASK (Collects information for delegation)
# -------------------------------------------------
coordination_task = Task(
    description="""
    You are the Travel Coordinator. Your role is to guide the planning process
    and ensure all teams work together effectively.
    
    Travel Details:
    - Destination: {destination}
    - Duration: {duration}
    - Budget: {budget}
    - Preferences: {preferences}
    
    Overview the planning process and prepare to delegate to:
    1. Research Team (Attractions, Food, Accommodation)
    2. Planning Team (Itinerary, Logistics)
    3. Financial Team (Budget Analysis)
    
    Acknowledge these inputs and confirm readiness for delegation.
    """,
    expected_output="""
    Confirmation of travel requirements and readiness for delegation to teams.
    """,
    agent=travel_coordinator
)

# -------------------------------------------------
# RESEARCH TEAM TASKS (Parallel Execution)
# -------------------------------------------------
attraction_task = Task(
    description="""
    Research the top attractions in {destination}.
    
    Include:
    - Must-visit landmarks
    - Hidden gems
    - Cultural sites
    - Natural attractions
    - Best time to visit each attraction
    
    Duration: {duration}
    Preferences: {preferences}
    """,
    expected_output="Detailed list of attractions with descriptions and recommendations",
    agent=attraction_specialist,
    async_execution=True
)

food_task = Task(
    description="""
    Research the food scene in {destination}.
    
    Include:
    - Famous restaurants
    - Local traditional dishes
    - Street food experiences
    - Vegetarian/vegan options
    - Price ranges
    
    Preferences: {preferences}
    """,
    expected_output="Comprehensive guide to dining in the destination",
    agent=food_specialist,
    async_execution=True
)

accommodation_task = Task(
    description="""
    Find the best accommodation options in {destination}.
    
    Include:
    - Luxury hotels
    - Mid-range hotels
    - Budget accommodations
    - Recommended neighborhoods
    - Amenities and proximity to attractions
    
    Duration: {duration}
    Budget: {budget}
    """,
    expected_output="Detailed accommodation recommendations by category",
    agent=accommodation_specialist,
    async_execution=True
)

# -------------------------------------------------
# PLANNING TEAM TASKS (Sequential: depends on research)
# -------------------------------------------------
itinerary_task = Task(
    description="""
    Create a comprehensive day-by-day itinerary for {destination}.
    
    Details:
    - Duration: {duration}
    - Preferences: {preferences}
    
    The itinerary should:
    - Distribute attractions evenly across days
    - Include meal times and dining recommendations
    - Allow for rest and exploration time
    - Group nearby attractions
    - Suggest best routes between locations
    
    Use the research team's findings on attractions, food, and accommodations.
    """,
    expected_output="""
    Detailed day-by-day itinerary with timing, activities, meals, and logistics.
    """,
    agent=itinerary_planner
)

logistics_task = Task(
    description="""
    Plan the logistics for the {destination} trip.
    
    Trip Details:
    - Duration: {duration}
    - Destination: {destination}
    
    Cover:
    - Getting from airport to accommodation
    - Local transportation options
    - Transportation between attractions
    - Best transportation modes
    - Estimated travel times
    
    Base this on the created itinerary and accommodation choices.
    """,
    expected_output="""
    Complete logistics plan including transportation, timing, and recommendations.
    """,
    agent=logistics_manager
)

# -------------------------------------------------
# FINANCIAL TEAM TASK
# -------------------------------------------------
budget_task = Task(
    description="""
    Analyze and optimize the travel budget for {destination}.
    
    Trip Details:
    - Duration: {duration}
    - Available Budget: {budget}
    - Preferences: {preferences}
    
    Provide cost estimates for:
    - Flights
    - Accommodation
    - Food and dining
    - Transportation
    - Activities and attractions
    - Miscellaneous expenses
    
    Compare total estimate with available budget.
    If over budget, suggest cost-saving alternatives.
    """,
    expected_output="""
    Detailed budget breakdown with:
    - Cost estimates by category
    - Total estimated cost
    - Comparison with available budget
    - Cost-saving suggestions if needed
    """,
    agent=budget_analyst
)

# -------------------------------------------------
# RESEARCH TEAM CREW (Parallel)
# -------------------------------------------------
research_team = Crew(
    agents=[
        attraction_specialist,
        food_specialist,
        accommodation_specialist
    ],
    tasks=[
        attraction_task,
        food_task,
        accommodation_task
    ],
    process=Process.parallel,
    verbose=True
)

# -------------------------------------------------
# PLANNING TEAM CREW (Sequential)
# -------------------------------------------------
planning_team = Crew(
    agents=[
        itinerary_planner,
        logistics_manager
    ],
    tasks=[
        itinerary_task,
        logistics_task
    ],
    process=Process.sequential,
    verbose=True
)

# -------------------------------------------------
# FINANCIAL TEAM CREW (Solo)
# -------------------------------------------------
financial_team = Crew(
    agents=[
        budget_analyst
    ],
    tasks=[
        budget_task
    ],
    verbose=True
)

# -------------------------------------------------
# MAIN HIERARCHICAL CREW
# -------------------------------------------------
travel_crew_hierarchical = Crew(
    agents=[
        travel_coordinator,
        attraction_specialist,
        food_specialist,
        accommodation_specialist,
        itinerary_planner,
        logistics_manager,
        budget_analyst
    ],
    tasks=[
        coordination_task,
        attraction_task,
        food_task,
        accommodation_task,
        itinerary_task,
        logistics_task,
        budget_task
    ],
    process=Process.sequential,
    verbose=True
)
