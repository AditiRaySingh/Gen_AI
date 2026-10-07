def calculate_confidence(plan, execution_success=True):
    score = 0.0

    # Metric recognized
    if plan.metric:
        score += 0.25

    # Operation recognized
    if plan.operation:
        score += 0.20

    # Dimensions recognized
    if plan.dimensions:
        score += 0.15

    # Filters recognized
    if plan.filters:
        score += 0.10

    # Comparison recognized
    if plan.comparison:
        score += 0.10

    # Query executed successfully
    if execution_success:
        score += 0.15

    # Valid structured plan
    if plan.model_dump():
        score += 0.05

    return round(min(score, 1.0), 2)