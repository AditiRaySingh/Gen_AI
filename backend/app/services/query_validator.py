from app.services.metadata import load_data_dictionary


ALLOWED_OPERATIONS = {
    "sum",
    "average",
    "count",
    "ranking",
    "contribution",
    "comparison"
}


ALLOWED_COMPARISONS = {
    "target",
    "yoy"
}


def validate_query_plan(plan):

    data_dictionary = load_data_dictionary()

    valid_metrics = set(
        data_dictionary["metrics"].keys()
    )

    valid_dimensions = set(
        data_dictionary["dimensions"]
    )

    # =========================
    # METRIC
    # =========================

    if plan.metric not in valid_metrics:
        return False, (
            f"Invalid metric: {plan.metric}"
        )


    # =========================
    # OPERATION
    # =========================

    if plan.operation not in ALLOWED_OPERATIONS:
        return False, (
            f"Unsupported operation: {plan.operation}"
        )


    # =========================
    # DIMENSIONS
    # =========================

    if len(plan.dimensions) != len(set(plan.dimensions)):
        return False, "Duplicate dimensions are not allowed."

    for dimension in plan.dimensions:

        if dimension not in valid_dimensions:
            return False, (
                f"Invalid dimension: {dimension}"
            )


    # =========================
    # FILTERS
    # =========================

    if not isinstance(plan.filters, list):
        return False, "Filters must be a list."

    for condition in plan.filters:

        if not isinstance(condition, dict):
            return False, (
                "Each filter must be an object."
            )

        if "column" not in condition:
            return False, (
                "Filter is missing 'column'."
            )

        if "value" not in condition:
            return False, (
                "Filter is missing 'value'."
            )

        column = condition["column"]
        value = condition["value"]

        if column not in valid_dimensions:
            return False, (
                f"Invalid filter column: {column}"
            )

        if value is None or str(value).strip() == "":
            return False, (
                f"Filter value cannot be empty for {column}."
            )


    # =========================
    # LIMIT
    # =========================

    if plan.limit is not None:

        if not isinstance(plan.limit, int):
            return False, (
                "Limit must be an integer."
            )

        if plan.limit <= 0:
            return False, (
                "Limit must be greater than zero."
            )


    # =========================
    # COMPARISON
    # =========================

    if plan.comparison is not None:

        if plan.comparison not in ALLOWED_COMPARISONS:
            return False, (
                f"Unsupported comparison: "
                f"{plan.comparison}"
            )


    # =========================
    # OPERATION-SPECIFIC RULES
    # =========================

    if plan.operation == "ranking":

        if not plan.dimensions:
            return False, (
                "Ranking requires at least one dimension."
            )

        if plan.limit is None:
            return False, (
                "Ranking requires a limit."
            )


    if plan.operation == "contribution":

        if not plan.dimensions:
            return False, (
                "Contribution requires at least one dimension."
            )


    if plan.operation == "comparison":

        if plan.comparison is None:
            return False, (
                "Comparison operation requires "
                "a comparison type."
            )


    return True, "Query plan is valid"