import { useState } from "react";
import { sendFeedback } from "../api/analyticsApi";

function FeedbackButtons({ query }) {
  const [submitted, setSubmitted] = useState(false);

  const handleFeedback = async (feedback) => {
    try {
      await sendFeedback(query, feedback);
      setSubmitted(true);
    } catch (error) {
      console.error(error);
      alert("Could not save feedback");
    }
  };

  if (submitted) {
    return (
      <div className="feedback-success">
        ✓ Thank you for your feedback
      </div>
    );
  }

  return (
    <div className="feedback-section">

      <span className="feedback-label">
        Was this result helpful?
      </span>

      <div className="feedback-buttons">

        <button
          onClick={() => handleFeedback("positive")}
        >
          👍 Yes
        </button>

        <button
          onClick={() => handleFeedback("negative")}
        >
          👎 No
        </button>

      </div>

    </div>
  );
}

export default FeedbackButtons;