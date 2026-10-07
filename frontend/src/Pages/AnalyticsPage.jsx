import { useState } from "react";
import { runQuery } from "../api/analyticsApi";
import ResultTable from "../components/ResultTable";
import FeedbackButtons from "../components/FeedbackButtons";
import LoadingState from "../components/LoadingState";
import "../index.css";

function AnalyticsPage() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleQuery = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setErrorMessage("");
    setResult(null);

    try {
      const response = await runQuery(query);
      setResult(response);
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail ||
          "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleExample = (example) => {
    setQuery(example);
  };

  return (
    <div className="analytics-page">
      <div className="analytics-container">

        {/* Header */}
        <div className="page-header">
          <h1>Analytics Query Engine</h1>
          <p>
            Ask questions about your sales data using natural language.
          </p>
        </div>

        {/* Query Section */}
        <div className="query-card">
          <label>Enter your query</label>

          <div className="query-input-row">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleQuery();
                }
              }}
              placeholder="Example: Top 2 cities by profit"
            />

            <button
              onClick={handleQuery}
              disabled={loading || !query.trim()}
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>

          <div className="examples">
            <span>Examples:</span>

            <button onClick={() => handleExample("Top 2 cities by profit")}>
              Top 2 cities by profit
            </button>

            <button
              onClick={() =>
                handleExample("Average order value by region")
              }
            >
              Average order value by region
            </button>

            <button
              onClick={() =>
                handleExample("Sales contribution % by category")
              }
            >
              Sales contribution % by category
            </button>

            <button
              onClick={() =>
                handleExample("Which region missed its target in Feb?")
              }
            >
              Region missed target in Feb
            </button>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="loading-container">
            <LoadingState />
          </div>
        )}

        {/* Error */}
        {errorMessage && (
          <div className="error-message">
            <strong>Error:</strong> {errorMessage}
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="results-section">

            <h2>Query Result</h2>

            {/* Query */}
            <div className="result-card">
              <h3>Query</h3>
              <p className="query-text">{result.query}</p>
            </div>

            {/* Confidence */}
            <div className="result-card">
              <div className="card-header">
                <h3>Confidence Score</h3>
                <span className="confidence-value">
                  {Math.round(result.confidence_score * 100)}%
                </span>
              </div>

              <div className="confidence-bar">
                <div
                  className="confidence-fill"
                  style={{
                    width: `${result.confidence_score * 100}%`,
                  }}
                ></div>
              </div>
            </div>

            {/* Explanation */}
            <div className="result-card">
              <h3>Explanation</h3>
              <p>{result.explanation}</p>
            </div>

            {/* Generated Logic */}
            <div className="result-card">
              <h3>Generated Logic</h3>

              <pre className="logic-box">
                {JSON.stringify(result.generated_logic, null, 2)}
              </pre>
            </div>

            {/* Result Table */}
            <div className="result-card">
              <h3>Result</h3>

              <ResultTable data={result.result} />
            </div>

            {/* Feedback */}
            <div className="result-card feedback-card">
              <h3>Was this result helpful?</h3>
              <FeedbackButtons query={result.query} />
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default AnalyticsPage;