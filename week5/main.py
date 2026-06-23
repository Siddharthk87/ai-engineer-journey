import anthropic
import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
client = anthropic.Anthropic()

# ── Input model ─────────────────────────────────────────────

class ValuationRequest(BaseModel):
    company_name: str
    revenue_prev: float
    revenue_curr: float
    ebitda: float
    debt: float
    cash: float
    sector: str

# ── Tools ───────────────────────────────────────────────────

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

def run_tool(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "calculate_wacc":
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

tools = [
    {
        "name": "get_comparable_companies",
        "description": "Retrieves comparable companies and valuation multiples for a sector",
        "input_schema": {
            "type": "object",
            "properties": {
                "sector": {"type": "string", "description": "Industry sector e.g. Education, Real Estate"}
            },
            "required": ["sector"]
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
    }
]

# ── Valuation endpoint ───────────────────────────────────────

@app.post("/value")
def value_company(request: ValuationRequest):
    financials = f"""
    Company: {request.company_name}
    Sector: {request.sector}
    Revenue previous year: AED {request.revenue_prev} billion
    Revenue current year: AED {request.revenue_curr} billion
    EBITDA: AED {request.ebitda} billion
    Debt: AED {request.debt} billion
    Cash: AED {request.cash} billion
    """

    system_prompt = """You are a senior valuation analyst at Deloitte Dubai.
    The user will provide company financials. You must:
    1. Get comparable companies for the sector
    2. Calculate WACC
    3. Write a full valuation report with: Key Metrics, Comparable Analysis, WACC, Valuation Range, Key Risks, Bottom Line."""

    messages = [{"role": "user", "content": f"Value this company:\n{financials}"}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2048,
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input)
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result)
                        }]
                    })
        else:
            return {"report": response.content[0].text}