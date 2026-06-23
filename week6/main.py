import anthropic
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
client = anthropic.Anthropic()

class ValuationRequest(BaseModel):
    company_name: str
    revenue_prev: float
    revenue_curr: float
    ebitda: float
    debt: float
    cash: float
    sector: str

def get_comparable_companies(sector: str) -> dict:
    comparables = {
        "education": {
            "companies": ["Taaleem", "Aldar Education", "Inspired Education"],
            "avg_ev_ebitda": 11.5,
            "avg_ev_revenue": 2.8,
            "avg_pe": 22.0
        },
        "real estate": {
            "companies": ["Emaar", "Aldar Properties", "Damac"],
            "avg_ev_ebitda": 14.2,
            "avg_ev_revenue": 3.1,
            "avg_pe": 18.5
        }
    }
    key = sector.lower()
    if key in comparables:
        return {"sector": sector, "comparables": comparables[key]}
    return {"error": f"No comparables found for sector: {sector}"}

def calculate_wacc(cost_of_equity, cost_of_debt, equity_value, debt_value, tax_rate) -> dict:
    total = equity_value + debt_value
    wacc = (equity_value / total * cost_of_equity / 100) + \
           (debt_value / total * cost_of_debt / 100 * (1 - tax_rate / 100))
    return {
        "wacc_percentage": round(wacc * 100, 2),
        "equity_weight": round(equity_value / total * 100, 1),
        "debt_weight": round(debt_value / total * 100, 1)
    }

def run_tool(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "get_comparable_companies":
        return get_comparable_companies(tool_input["sector"])
    elif tool_name == "calculate_wacc":
        return calculate_wacc(
            tool_input["cost_of_equity"],
            tool_input["cost_of_debt"],
            tool_input["equity_value"],
            tool_input["debt_value"],
            tool_input["tax_rate"]
        )

tools = [
    {
        "name": "get_comparable_companies",
        "description": "Gets comparable listed companies and trading multiples for a given sector",
        "input_schema": {
            "type": "object",
            "properties": {
                "sector": {"type": "string", "description": "The industry sector"}
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
                "cost_of_equity": {"type": "number"},
                "cost_of_debt": {"type": "number"},
                "equity_value": {"type": "number"},
                "debt_value": {"type": "number"},
                "tax_rate": {"type": "number"}
            },
            "required": ["cost_of_equity", "cost_of_debt", "equity_value", "debt_value", "tax_rate"]
        }
    }
]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Deloitte Valuation Tool</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
        h1 { color: #86BC25; }
        input, select { width: 100%; padding: 8px; margin: 6px 0 14px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background: #86BC25; color: white; padding: 12px 30px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        #result { margin-top: 30px; background: white; padding: 20px; border-radius: 4px; white-space: pre-wrap; display: none; }
        #loading { display: none; color: #86BC25; margin-top: 20px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>Deloitte Valuation Tool</h1>
    <form id="valuationForm">
        <label>Company Name</label>
        <input name="company_name" placeholder="e.g. GEMS Education" required>

        <label>Sector</label>
        <select name="sector">
            <option value="education">Education</option>
            <option value="real estate">Real Estate</option>
        </select>

        <label>Revenue Previous Year (AED bn)</label>
        <input name="revenue_prev" type="number" step="0.1" placeholder="e.g. 50" required>

        <label>Revenue Current Year (AED bn)</label>
        <input name="revenue_curr" type="number" step="0.1" placeholder="e.g. 75" required>

        <label>EBITDA (AED bn)</label>
        <input name="ebitda" type="number" step="0.1" placeholder="e.g. 15" required>

        <label>Debt (AED bn)</label>
        <input name="debt" type="number" step="0.1" placeholder="e.g. 30" required>

        <label>Cash (AED bn)</label>
        <input name="cash" type="number" step="0.1" placeholder="e.g. 20" required>

        <button type="submit">Generate Valuation Report</button>
    </form>

    <div id="loading">⏳ Claude is generating your valuation report...</div>
    <div id="result"></div>

    <script>
        document.getElementById('valuationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';

            const data = {
                company_name: this.company_name.value,
                sector: this.sector.value,
                revenue_prev: parseFloat(this.revenue_prev.value),
                revenue_curr: parseFloat(this.revenue_curr.value),
                ebitda: parseFloat(this.ebitda.value),
                debt: parseFloat(this.debt.value),
                cash: parseFloat(this.cash.value)
            };

            const response = await fetch('/value', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            document.getElementById('loading').style.display = 'none';
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').innerText = result.report;
        });
    </script>
</body>
</html>
"""

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
    When asked to value a company, you MUST follow these steps in order:
    1. Get comparable companies for the sector using get_comparable_companies
    2. Calculate WACC using calculate_wacc with these assumptions: cost_of_equity=12, cost_of_debt=6, tax_rate=9
    3. Write a full valuation report with EV/EBITDA range, implied equity value, and recommendation."""

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
                    messages.append({"role": "user", "content": [{
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    }]})
        else:
            return {"report": response.content[0].text}