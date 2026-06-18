import anthropic

client = anthropic.Anthropic()

system_prompt = "You are a senior valuation analyst at Deloitte Dubai. You specialise in Middle East markets. Always structure your response with: 1) Key Metrics, 2) Valuation Range using EV/EBITDA multiples appropriate for the sector, 3) Key Risks, 4) Bottom Line recommendation. Be concise and professional."

conversation_history = []

print("Valuation Assistant ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        print("Exiting Valuation Assistant. Goodbye!")
        break

    conversation_history.append({
        
        "role": "user", 
        "content": user_input
        
        })
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=conversation_history
    )
    
    response = message.content[0].text

    conversation_history.append({
        
        "role": "assistant",
        "content": response

    })
    print(f"Claude: {response}\n")