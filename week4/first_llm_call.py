import anthropic

client = anthropic.Anthropic()

company = input("Enter the company name: ")
revenue_prev = input("Enter the previous year's revenue (in AED bn): ")
revenue_curr = input("Enter the current year's revenue (in AED bn): ")
ebitda = input("Enter the current year EBITDA (in AED bn): ")
debt = input("Enter the current year debt (in AED bn): ")
cash = input("Enter the current year cash (in AED bn): ")

financials = f"""
Company: {company}
Revenue 2023: AED {revenue_prev} billion
Revenue 2024: AED {revenue_curr} billion
EBITDA 2023: AED {ebitda} billion
EBITDA 2024: AED {ebitda} billion
Debt: AED {debt} billion
Cash: AED {cash} billion
"""


message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system="You are a senior valuation analyst at Deloitte Dubai. You specialise in Middle East markets. Always structure your response with: 1) Key Metrics, 2) Valuation Range using EV/EBITDA multiples appropriate for the sector, 3) Key Risks, 4) Bottom Line recommendation. Be concise and professional.",
    messages=[
        {
            "role": "user",
            "content": f"Analyze these financials and give me a brief valuation assessment:\n{financials}"
        }
    ]
)

print(message.content[0].text)