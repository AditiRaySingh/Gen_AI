function LoadingState() {
  return (
    <div className="loading-state">

      <div className="loading-spinner"></div>

      <div>
        <strong>Analyzing your query...</strong>
        <p>
          GenAI is understanding your question and generating insights.
        </p>
      </div>

    </div>
  );
}

export default LoadingState;