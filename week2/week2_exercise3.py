# Without error handling - this crashes
# int("'hello") # uncomment this to see the crash

# Wtih error handing
def safe_convert(value, target_type):
    try:
        return target_type(value)
    except ValueError as e:
        print(f"Conversion failed: {e}")
        return None
    
# Test it
print(safe_convert("38", int)) # works
print(safe_convert("2.5", float)) # works
print(safe_convert("hello", int)) # fails gracefully
print(safe_convert("abc", float)) # fails gracefully

# Multiple exception types
def read_expense_file(filename):
    try:
        with open(filename, "r") as f:
            import json
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"File '{filename}' doesn't exist yet. Starting fresh.")
        return []
    except json.JSONDecodeError:
        print(f"File '{filename}' is corrupter. Starting fresh.")
        return []

# Test with a file that doesn't exist
expenses = read_expense_file("fake_file.json")
print(f"Loaded {len(expenses)} expenses")

# Test with your real file
expenses = read_expense_file("../week1/expenses.json")
print(f"Loaded {len(expenses)} expenses from week 1")

# Finally block - runs no matter what
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannont divide by zero")
        return None
    finally:
        print(f"divide ({a}, {b}) was called")

print (divide(10,2 ))
print(divide(10,0))