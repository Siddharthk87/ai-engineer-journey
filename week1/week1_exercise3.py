def greet(name, role):
    message = f"Hi {name}, welcome to your AI engineering journey!"
    print(message)
    print(f"Current role: {role}")
    print(f"Target role: AI Automation engineer\n")

def calculate_study_hours(hours_per_day, days_per_week):
    weekly = hours_per_day * days_per_week
    monthly = weekly * 4
    total = monthly * 8
    return total

def assess_progress(weeks_completed, total_weeks=35):
    percentage = (weeks_completed / total_weeks) * 100
    return round(percentage, 1)

#Now USE the functions

greet("Siddharth", "Valuation speacialist at Deloitte")

total_hours = calculate_study_hours(2.5, 6)
print(f"Total study hours over 8 months: {total_hours}")

progress = assess_progress(18)
print(f"Progress after Week 1: {progress}%")