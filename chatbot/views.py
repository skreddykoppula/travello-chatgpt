from django.shortcuts import render
import openai

# Define available options
departures = ["Hyderabad", "Goa", "Mumbai", "Delhi"]
destinations = ["Hyderabad", "Goa", "Mumbai", "Delhi"]
budgets = [10000, 15000, 20000, 25000]
days = [5, 6, 7]

# Set up OpenAI API key
openai.api_key = "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"

def home(request):
    context = {
        "departures": departures,
        "destinations": destinations,
        "budgets": budgets,
        "days": days,
    }
    return render(request, "chatbot.html", context)

def generate_itinerary(request):
    # Get user preferences from the form
    departure_choice = int(request.POST.get("departure"))
    departure_city = departures[departure_choice - 1]
    destination_choice = int(request.POST.get("destination"))
    destination_city = destinations[destination_choice - 1]
    budget_choice = int(request.POST.get("budget"))
    budget = budgets[budget_choice - 1]
    days_choice = int(request.POST.get("days", 1))  # Default value is 1
    num_days = days[days_choice - 1]

    # Generate itinerary
    activities = []
    for i in range(1, num_days + 1):
        # Generate activity based on ChatGPT's response
        prompt = f"Plan an activity for day {i} of a {num_days}-day trip from {departure_city} to {destination_city} with a budget of ${budget} day wise."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )
        activity = response.choices[0].text.strip()
        activities.append(f"Day {i}: {activity}")

    # Render the itinerary page with the generated activities
    context = {"activities": activities}
    return render(request, "chatbot.html", context)
