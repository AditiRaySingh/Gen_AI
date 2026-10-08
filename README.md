🚀 Intelligent Analytics Query Engine

Natural Language → AI Query Plan → Analytics Result

An AI-powered analytics system that allows users to ask business questions in natural language and get structured, data-driven results.



🧩 Approach

The system converts a natural-language business question into a structured QueryPlan and safely executes it on the dataset.

Processing Flow
User Query
    ↓
🤖 Gemini AI Planner
    ↓
📋 Structured QueryPlan
    ↓
✅ Query Validator
    ↓
⚙️ Pandas Query Engine
    ↓
📊 Result
    ↓
💡 Confidence + Explanation
Supported Analytics
Operation	Example
Sum	Revenue by region
Average	Average profit
Count	Number of orders
Ranking	Top 5 customers
Contribution	Revenue contribution %
Target Comparison	Actual vs Target
YoY	Year-over-Year growth
🏗️ Architecture
┌──────────────────┐
│  React Frontend  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│   FastAPI API    │
└────────┬─────────┘
         ↓
┌──────────────────┐
│    AI Planner    │
│     Gemini       │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Query Validator  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Query Engine    │
│     Pandas       │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ CSV / JSON Data  │
└──────────────────┘
Main Components
Component	Responsibility
ai_planner.py	Converts natural language into QueryPlan
query_validator.py	Validates AI-generated plans
query_engine.py	Executes analytics using Pandas
confidence.py	Calculates confidence score
explanation.py	Generates query explanation
feedback.py	Stores user feedback
metadata.py	Loads datasets and data dictionary
⚖️ Tradeoffs
Decision	Why	Tradeoff
Gemini for query planning	Handles natural language well	Depends on external API
Pandas for execution	Simple and fast for CSV data	Less suitable for very large datasets
QueryPlan schema	Makes AI output structured and controllable	Supports only predefined operations
CSV datasets	Easy to use and understand	Not ideal for production-scale data
Rule-based validation	Prevents invalid AI output	New query types may require new rules
Heuristic confidence score	Simple and explainable	Not a true probability
📤 Sample Outputs
Query 1 — Revenue by Region

Input

Show total revenue by region.

Output

{
  "query": "Show total revenue by region.",
  "generated_logic": {
    "metric": "revenue",
    "dimensions": ["region"],
    "operation": "sum"
  },
  "confidence_score": 0.85,
  "explanation": "Revenue is grouped by region and summed."
}
Query 2 — Top Customers

Input

Show the top 3 customers in each region by revenue.

Generated Logic

{
  "metric": "revenue",
  "dimensions": ["region", "customer_id"],
  "operation": "ranking",
  "limit": 3
}

Result

North → Customer A, Customer B, Customer C
South → Customer X, Customer Y, Customer Z
Query 3 — Target Comparison

Input

Which regions missed their target?

Output

Region    Actual     Target     Status
North     90,000     100,000    Missed Target
South     70,000      60,000    Met Target
🔮 Improvements With More Time
Use feedback to improve future query planning
Add advanced date and filter operations
Support more complex nested queries
Replace CSV with a production database
Add automated unit and integration tests
Improve confidence scoring using model-based evaluation
Add charts and advanced data visualization
🛠️ Tech Stack
Layer	Technology
Frontend	React + Vite
Backend	Python + FastAPI
AI	Google Gemini
Data Processing	Pandas
Validation	Pydantic
Data	CSV + JSON
🚀 Run Locally
Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
Frontend
cd frontend
npm install
npm run dev

API documentation:

http://127.0.0.1:8000/docs
👩‍💻 Project Summary

Intelligent Analytics Query Engine demonstrates how GenAI can be combined with structured validation and deterministic data processing to answer business questions using natural language.
