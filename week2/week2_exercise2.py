# String methods - tools built into every string
text = " Valuation Specialist at Deloitte "

# Cleaning
print(text.strip()) # remove whitespace from both ends
print(text.strip().lower()) # chain methods together
print(text.strip().upper())

# Splitting and joining
skills = "python,apis,llms,rag,agents"
skills_list = skills.split(",") # split string into list
print(skills_list)

rejoined = " | ".join(skills_list) # join list back into string
print(rejoined)

# Checking content
email = "siddharth@deloitte.com"
print(email.startswith("siddharth")) # True or False
print(email.endswith(".com"))
print("deloitte" in email)

# Replacing
messy = "AI   engineer  with  lots   of   spaces"
print(messy.replace("  "," "))

# Finding
sentence = "RAG systems are the more in-demand AI skills right now"
print(sentence.find("RAG")) # returns position of first match
print(sentence.count("a"))  # counts occurences 
print(sentence.upper().count("A")) # case matter - this counts all A's

# Real world example - cleaning user input before storing it
raw_input = " FOOD "
cleaned = raw_input.strip().lower()
print(f"Raw: '{raw_input}'. -> Cleaned: '{cleaned}'")