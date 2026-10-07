from app.services.ai_planner import create_query_plan
from app.services.query_validator import validate_query_plan
from app.services.query_engine import execute_query
from app.services.confidence import calculate_confidence
from app.services.explanation import create_explanation


def process_query(user_query):
    # Step 1: Create plan using AI
    plan = create_query_plan(user_query)

    # Step 2: Validate the plan
    is_valid, message = validate_query_plan(plan)

    if not is_valid:
        raise ValueError(message)

    # Step 3: Execute the plan
    result = execute_query(plan)

    confidence_score = calculate_confidence(plan)

    explanation = create_explanation(plan)

    return {
        "query": user_query,
        "generated_logic": plan.model_dump(),
        "result": result.to_dict(orient="records")
        if hasattr(result, "to_dict")
        else result,
        "confidence_score": confidence_score,
        "explanation": explanation,
    }