# Regular loop approach
expenses = [45.0, 12.0, 90.0, 30.0, 70.0]

# Filter only expensive items the old way
expensive_old = []
for e in expenses:
    if e > 40:
     expensive_old.append(e)

print("Old way:", expensive_old)

# List comprehension - Same result, one line
expensive_new = [e for e in expenses if e > 40]
print("New way:", expensive_new)

#Transform values - convert AED to USD (1 AED = 0.27 USD)
in_usd = [round(e * 0.27, 2) for e in expenses]
print("In USD:", in_usd)

# Combine filter and transform in one line
expensive_in_usd = [round(e * 0.27, 2) for e in expenses if e > 40]
print("Expensive in USD:", expensive_in_usd)

# Works on strings too
skills = ["python", "apis", "llms", "rag", "agents"]
capitalised = [s.upper() for s in skills]
print("Capitalised:", capitalised)