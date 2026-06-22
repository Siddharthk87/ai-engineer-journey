import anthropic
import json

client = anthropic.Anthropic()

def get_company_financials(company_name: str) -> dict:
    financials_database = {
        "gems": {
            "company": "GEMS Education",
            "revenue_prev": 50,
            "revenue_curr": 75,
            "ebitda": 15,
            "debt": 30,
            "cash": 20,
            "sector": "Education"
        },
        "emaar": {
            "company": "Emaar Properties",
            "revenue_prev": 24,
            "revenue_curr": 31,
            "ebitda": 12,
            "debt": 45,
            "cash": 15,
            "sector": "Real Estate"
        }
    }
    key = company_name.lower()
    if key in financials_database:
        return financials_database[key]
    return {"error": f"Company '{company_name}' not found"}

tools = [
    {
        "name": "get_company_financials",
        "description": "Retrieves financial data for a company including revenue, EBITDA, debt and cash",
        "input_schema": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "The name of the company to look up"
                }
            },
            "required": ["company_name"]
        }
    }
]

print("Valuation Assistant ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system="You are a senior valuation analyst at Deloitte Dubai. When asked about a company, use the get_company_financials tool to fetch their data, then provide a valuation assessment.",
            tools=tools,
            messages=[{"role": "user", "content": user_input}]
        )
 
        if response.stop_reason == "tool_use":
            tool_use = response.content[0]
            tool_result = get_company_financials(tool_use.input["company_name"])

            final_response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=1024,
                system="You are a senior valuation analyst at Deloitte Dubai. When asked about a company, use the get_company_financials tool to fetch their data, then provide a valuation assessment.",
                tools=tools,
                messages=[
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": response.content},
                    {"role": "user", "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": json.dumps(tool_result)
                        }
                    ]}
                ]
            )
            print(f"\nClaude: {final_response.content[0].text}\n")
        else:
            print(f"\nClaude: {response.content[0].text}\n")

    except Exception as e:
        print(f"Error: {e}")