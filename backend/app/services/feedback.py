from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
FEEDBACK_FILE = DATA_DIR / "feedback_log.csv"


def save_feedback(query, feedback):
    file_exists = FEEDBACK_FILE.exists()

    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["query", "feedback"])

        writer.writerow([query, feedback])

    return {
        "message": "Feedback saved successfully"
    }