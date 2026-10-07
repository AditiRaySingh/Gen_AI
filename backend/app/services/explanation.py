def create_explanation(plan):
    explanation = []

    # Metric
    explanation.append(
        f"The system identified '{plan.metric}' as the main metric."
    )

    # Grouping
    if plan.dimensions:
        explanation.append(
            f"The result was grouped by {', '.join(plan.dimensions)}."
        )

    # Filters
    if plan.filters:
        filters = []

        for condition in plan.filters:
            filters.append(
                f"{condition['column']} = {condition['value']}"
            )

        explanation.append(
            "The query was filtered using: "
            + ", ".join(filters)
            + "."
        )

    # Ranking
    if plan.operation == "ranking" and plan.limit:
        explanation.append(
            f"The system ranked the results and returned the top "
            f"{plan.limit} item(s) for each relevant group."
        )

    # Contribution
    elif plan.operation == "contribution":
        explanation.append(
            "The system calculated each group's percentage contribution "
            "to the total metric."
        )

    # Target comparison
    elif (
        plan.operation == "comparison"
        and plan.comparison == "target"
    ):
        explanation.append(
            "The system compared actual revenue with the corresponding "
            "target revenue and identified whether each region met or "
            "missed its target."
        )

    # YoY comparison
    elif (
        plan.operation == "comparison"
        and plan.comparison == "yoy"
    ):
        explanation.append(
            "The system compared revenue between the current year and "
            "the previous year."
        )

        explanation.append(
            "If previous-year data is unavailable, YoY growth is returned "
            "as unavailable instead of being estimated."
        )

    # Normal operation
    else:
        explanation.append(
            f"The system used the '{plan.operation}' operation "
            "to calculate the result."
        )

    return " ".join(explanation)