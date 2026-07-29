# Travel Planner Multi-Agent System

# Watch the complete implementation session here [https://youtu.be/JhmqzNl8y_w]

A multi-agent travel planning system built with CrewAI that helps you create comprehensive travel itineraries with budget analysis.

## Features

- 🔍 **Destination Research**: Explore attractions, activities, and local experiences
- 📅 **Itinerary Planning**: Create day-by-day travel plans
- 💰 **Budget Analysis**: Estimate costs and optimize spending

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- OpenAI API key (get it from [platform.openai.com](https://platform.openai.com/api-keys))

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure OpenAI API Key

#### Option A: Using `.env` file (Recommended)

1. Open the `.env` file in the root directory:
   ```
   .env
   ```

2. Add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your_actual_api_key_here
   ```

3. Replace `sk-your_actual_api_key_here` with your actual OpenAI API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

#### Option B: Using Environment Variable

Alternatively, set the environment variable directly:

```bash
export OPENAI_API_KEY=sk-your_actual_api_key_here
```

**Important**: Never commit your `.env` file to version control. The `.gitignore` file already protects it.

### 4. Run the Application

```bash
python main.py
```

## Project Structure

```
travel-planner-multi-agent-system/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (keep secret!)
├── .env.example            # Example configuration template
├── .gitignore              # Git ignore rules
└── agents/
    └── travel_agents.py   # CrewAI agents and tasks
```

## How It Works

1. **Destination Researcher Agent**: Researches the destination for attractions and activities
2. **Itinerary Planner Agent**: Creates a day-by-day travel plan
3. **Budget Analyst Agent**: Estimates costs and provides budget analysis

## Customization

Edit the inputs in `main.py` to customize:

```python
result = travel_crew.kickoff(
    inputs={
        "destination": "Paris",
        "duration": "7 days",
        "budget": "₹1,50,000",
        "preferences": "History, culture, food, photography, and popular landmarks"
    }
)
```

## Troubleshooting

### "OPENAI_API_KEY environment variable is not set"

This error means your API key is missing. Follow Step 3 above to add it.

### API Key Errors

- Ensure your OpenAI API key is valid and active
- Check that you have sufficient credits in your OpenAI account
- Verify the key format starts with `sk-`

## License

Your License Here

