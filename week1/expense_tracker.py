import json
import os

def load_expenses(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_expenses(filename, expenses):
    with open(filename, "w") as f:
        json.dump(expenses, f, indent=2)

def add_expense(expenses):
    category = input("Category (food/transport/bills/other): ").lower()
    amount = float(input("Amount (AED): "))
    description = input("Description: ")

    expense = {
        "category": category,
        "amount": amount,
        "description": description
    }

    expenses.append(expense)
    print(f"✓ Added {description} - AED {amount}\n")
    return expenses

def show_summary(expenses):
    if not expenses:
        print("No expenses recorded yet. \n")
        return
    
    totals = {}
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        if category in totals:
            totals[category] += amount
        else:
            totals[category] = amount

    print("\n--- Expense Summary ---")
    for category, total in totals.items():
        print(f"{category.capitalize()}: AED {total:.2f}")

    grand_total = sum(totals.values())
    print(f"\nTotal: AED {grand_total:.2f}\n")

def main():
    filename = "expenses.json"
    expenses = load_expenses(filename)
    print(f"Loaded {len(expenses)} existing expenses. \n")

    while True:
        print("What would you like to do?")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Quit")

        choice = input("\nChoice (1/2/3): ")

        if choice == "1":
            expenses = add_expense(expenses)
            save_expenses(filename, expenses)
        elif choice == "2":
            show_summary(expenses)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.\n")
main()  