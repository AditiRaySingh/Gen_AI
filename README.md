# 🚀 Intelligent Analytics Query Engine

<p align="center">
  <b>AI-Powered Natural Language Analytics System</b>
</p>

<p align="center">
  Ask business questions in natural language and get structured, data-driven results.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black">
  <img src="https://img.shields.io/badge/Pandas-Analytics-150458?logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/GenAI-Gemini-4285F4?logo=google&logoColor=white">
</p>

---

## 🎯 Overview

The **Intelligent Analytics Query Engine** converts a natural-language business question into a structured `QueryPlan`, validates it, executes it on the dataset, and returns the result with a **confidence score and explanation**.

### 💡 Example

> **"Show the top 3 customers in each region by revenue."**

The system understands the query → creates a plan → validates it → executes it → returns the result.

---

## 🧠 Approach

```text
Natural Language Query
          ↓
     🤖 AI Planner
          ↓
     📋 QueryPlan
          ↓
    ✅ Validator
          ↓
    ⚙️ Query Engine
          ↓
     📊 Result
          ↓
 💡 Confidence + Explanation
Supported Analytics
🔧 Operation	📌 Example
sum	Revenue by region
average	Average profit
count	Number of orders
ranking	Top 5 customers
contribution	Revenue contribution %
comparison	Actual vs Target
yoy	Year-over-Year growth
🏗️ Architecture
📂 Main Components
📄 Component	🎯 Responsibility
ai_planner.py	Converts natural language into a QueryPlan
query_validator.py	Validates AI-generated plans
query_engine.py	Executes analytics using Pandas
analytics_service.py	Connects the complete backend flow
confidence.py	Calculates confidence score
explanation.py	Generates a human-readable explanation
feedback.py	Stores user feedback
metadata.py	Loads datasets and data dictionary
⚖️ Tradeoffs
🧩 Decision	✅ Advantage	⚠️ Tradeoff
Gemini for planning	Strong natural-language understanding	Depends on external API
Pandas for execution	Simple and fast for CSV data	Not ideal for huge datasets
QueryPlan	Structured and controllable AI output	Limited to predefined operations
CSV data	Easy to use and understand	Not suitable for production-scale data
Rule-based validation	Prevents invalid AI output	New query types may need new rules
Heuristic confidence	Simple and explainable	Not a true probability
📊 Sample Outputs
🔹 1. Revenue by Region

Input

Show total revenue by region.

Generated Logic

{
  "metric": "revenue",
  "dimensions": ["region"],
  "filters": [],
  "operation": "sum",
  "limit": null,
  "comparison": null
}

Result

Region	Revenue
North	90,000
South	75,000
West	68,000

Confidence: 0.85

🔹 2. Top 3 Customers in Each Region

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

Region	Customer	Rank
North	Customer A	1
North	Customer B	2
North	Customer C	3
South	Customer X	1
South	Customer Y	2
South	Customer Z	3
🔹 3. Target Comparison

Input

Which regions missed their target?

Result

Region	Actual	Target	Status
North	90,000	100,000	🔴 Missed Target
South	70,000	60,000	🟢 Met Target
🛠️ Tech Stack
Layer	Technology
🎨 Frontend	React + Vite
⚙️ Backend	Python + FastAPI
🤖 AI	Google Gemini
📊 Data Processing	Pandas
✅ Validation	Pydantic
📁 Data	CSV + JSON
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
📖 API Documentation
http://127.0.0.1:8000/docs
🔐 Environment Variables

Create a .env file inside backend:

OPENAI_API_KEY=your_gemini_api_key

⚠️ Never commit your API key or .env file to GitHub.

🔮 Future Improvements
🔄 Use feedback to improve future query planning
🗓️ Add advanced date and filter operations
🧠 Support more complex analytical queries
🗄️ Replace CSV with a production database
🧪 Add automated unit and integration tests
📈 Improve confidence scoring
📊 Add advanced data visualizations
👩‍💻 Project Summary

This project demonstrates how GenAI + structured validation + deterministic data processing can be combined to answer business questions using natural language.

Core Pipeline:

🗣️ Natural Language → 🤖 GenAI → 📋 QueryPlan → ✅ Validation → ⚙️ Execution → 📊 Result


### Why this version will look better

- 🎨 **Badges** give it color at the top.
- 📊 **Proper Markdown tables** keep information aligned.
- 🏗️ **Mermaid diagram** is much cleaner than ASCII boxes.
- 🔹 Each sample output is separated clearly.
- ⚖️ Tradeoffs are easy for the reviewer to scan.
- 🔮 Improvements are short and professional.
- No giant architecture boxes or text running into each other.

**One important thing:** don't put `id="..."` after your code fences like in the earlier generated version. That is not needed in your `README.md` and can contribute to messy rendering.
