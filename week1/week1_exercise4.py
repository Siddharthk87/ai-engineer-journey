# A dictionary stores key-value pairs
person = {
    "name": "Siddharth",
    "age": 38,
    "role": "Valuation Specialist",
    "company": "Deloitte",
    "location": "Dubai",
    "study_hours_per_day": 2.5
}

# Access values by key
print(person["name"])
print(person["company"])

# Add a new key
person["target_role"] = "AI Automation Engineer"

# Update an existing key
person["study_hours_per_day"] = 3.0

#Loop through a dictionary
print("\n--- Your Profile ---")
for key, value in person.items():
    print(f"{key}: {value}")

# A more realistic example - a dictionary of dictionaries
months = {
    "Month 1": {"topic": "Python Foundations", "status": "In Progress"},
    "Month 2": {"topic": "LLM App Development", "status": "Pending"},
    "Month 3": {"topic": "RAG Systems", "status": "Pending"},
} 

print("\n--- Roadmap status ---")
for month, details in months.items():
    print(f"{month}: {details['topic']} [{details['status']}]")

print("\n--- Roadmap status ---")
for month, details in months.items():
    print(f"{month}: {details}")