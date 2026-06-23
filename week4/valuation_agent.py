import anthropic
import json

client = anthropic.Anthropic()

# ── Your tools/functions ────────────────────────────────────

def get_company_financials(company_name: str) -> dict:
    database = {
        "gems": {
            "company": "GEMS Education",
            "sector": "Education",
            "revenue_prev": 50,
            "revenue_curr": 75,
            "ebitda": 15,
            "debt": 30,
            "cash": 20
        },
        "emaar": {
            "company": "Emaar Properties",
            "sector": "Real Estate",
            "revenue_prev": 24,
            "revenue_curr": 31,
            "ebitda": 12,
            "debt": 45,
            "cash": 15
        }
    }
    key = company_name.lower()
    if key in database:
        return database[key]
    return {"error": f"Company '{company_name}' not found"}

def calculate_wacc(cost_of_equity: float, cost_of_debt: float,
                   equity_value: float, debt_value: float,
                   tax_rate: float) -> dict:
    total = equity_value + debt_value
    wacc = (equity_value/total * cost_of_equity/100) + \
           (debt_value/total * cost_of_debt/100 * (1 - tax_rate/100))
    return {
        "wacc_percentage": round(wacc * 100, 2),
        "equity_weight": round(equity_value/total * 100, 1),
        "debt_weight": round(debt_value/total * 100, 1)
    }

def get_comparable_companies(sector: str) -> dict:
    comparables = {
        "education": {
            "companies": ["Taaleem Holdings", "Aldar Education", "Inspired Education"],
            "avg_ev_ebitda": 11.5,
            "avg_ev_revenue": 2.8,
            "avg_ebitda_margin": 21.0
        },
        "real estate": {
            "companies": ["Aldar Properties", "DAMAC", "Nakheel"],
            "avg_ev_ebitda": 9.0,
            "avg_ev_revenue": 3.5,
            "avg_ebitda_margin": 35.0
        }
    }
    key = sector.lower()
    if key in comparables:
        return comparables[key]
    return {"error": f"No comparables found for sector '{sector}'"}

def run_tool(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "get_company_financials":
        return get_company_financials(tool_input["company_name"])
    elif tool_name == "calculate_wacc":
        return calculate_wacc(
            tool_input["cost_of_equity"],
            tool_input["cost_of_debt"],
            tool_input["equity_value"],
            tool_input["debt_value"],
            tool_input["tax_rate"]
        )
    elif tool_name == "get_comparable_companies":
        return get_comparable_companies(tool_input["sector"])
    return {"error": f"Unknown tool: {tool_name}"}

# ── Tools list ──────────────────────────────────────────────

tools = [
    {
        "name": "get_company_financials",
        "description": "Retrieves financial data for a company including revenue, EBITDA, debt and cash",
        "input_schema": {
            "type": "object",
            "properties": {
                "company_name": {"type": "string", "description": "The name of the company"}
            },
            "required": ["company_name"]
        }
    },
    {
        "name": "calculate_wacc",
        "description": "Calculates the Weighted Average Cost of Capital",
        "input_schema": {
            "type": "object",
            "properties": {
                "cost_of_equity": {"type": "number", "description": "Cost of equity as percentage"},
                "cost_of_debt": {"type": "number", "description": "Cost of debt as percentage"},
                "equity_value": {"type": "number", "description": "Market value of equity in AED bn"},
                "debt_value": {"type": "number", "description": "Market value of debt in AED bn"},
                "tax_rate": {"type": "number", "description": "Corporate tax rate as percentage"}
            },
            "required": ["cost_of_equity", "cost_of_debt", "equity_value", "debt_value", "tax_rate"]
        }
    },
    {
        "name": "get_comparable_companies",
        "description": "Retrieves comparable companies and their valuation multiples for a given sector",
        "input_schema": {
            "type": "object",
            "properties": {
                "sector": {"type": "string", "description": "The industry sector e.g. Education, Real Estate"}
            },
            "required": ["sector"]
        }
    }
]

# ── Agent loop ──────────────────────────────────────────────

system_prompt = """You are a senior valuation analyst at Deloitte Dubai specialising in Middle East markets.

When asked to value a company, you MUST follow these steps in order:
1. Fetch the company financials using get_company_financials
2. Get comparable companies for the sector using get_comparable_companies  
3. Calculate WACC using calculate_wacc
4. Write a full valuation report with: Key Metrics, Comparable Companies Analysis, WACC, Valuation Range, Key Risks, and Bottom Line

Do not skip any steps. Do not ask the user for information — figure it out from the data."""

print("Valuation Agent ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    messages = [{"role": "user", "content": user_input}]

    print("\n[Agent thinking...]\n")

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2048,
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "tool_use":
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            for block in response.content:
                if block.type == "tool_use":
                    print(f"[Calling: {block.name} with {block.input}]")
                    result = run_tool(block.name, block.input)
                    print(f"[Result: {result}]\n")

                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result)
                        }]
                    })
        else:
            print(f"Claude: {response.content[0].text}\n")
            break