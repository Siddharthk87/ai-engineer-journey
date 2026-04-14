name = input("What's your name? ")
age = int(input("What's your age? "))
hours_per_day = float(input("How many hours per day can you study? "))

if hours_per_day >= 2:
    pace = "excellent"
elif hours_per_day >= 1:
    pace = "solid"
else:
    pace = "challenging but possible"

if age < 30:
    advantage = "You have youth on your side."
elif age < 40:
    advantage = "You have professional experience that will make this more meaningful."
else:
    advantage = "Your industry expertise gives you a head start on real-world applications."

print(f"\nHi {name}!")
print(f"Studying {hours_per_day} is a {pace} pace for this roadmap.")
print(f"{advantage}")
print(f"At this rate, you'll be writing AI automation tool within 6 months.")