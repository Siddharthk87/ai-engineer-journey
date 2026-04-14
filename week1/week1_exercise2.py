# A for loop runs once for each item in sequence
skills = ["Python", "APIs", "LLMs", "RAG", "Agents", "Deployment", "Specialisation"]

print("\nYour 6-month learning journey:\n")

for i, skill in enumerate(skills, 1):
    print(f"Month {i}: {skill}")

for skill in enumerate(skills, 1):
    print(f"{skill}")

print("\n--- Now with a condition inside the loop ---\n")

for i, skill in enumerate(skills, 1):
    if i <= 2:
        status = "Foundation"
    elif i <= 4:
        status = "Core AI Engineering"
    else:
        status = "Advanced"
    print(f"Month {i}: {skill} [{status}]")

# Try this: loop only over the first three items
for skill in skills[:3]:
    print(f"Focus this month: {skill}")