from app.services.metadata import load_sales_data, load_targets


def execute_query(plan):
    df = load_sales_data()
    targets = load_targets()

    # =========================
    # BASIC DATA CHECK
    # =========================

    if df.empty:
        raise ValueError(
            "Sales dataset is empty."
        )

    # =========================
    # APPLY FILTERS
    # =========================

    for condition in plan.filters:
        column = condition["column"]
        value = condition["value"]

        if column not in df.columns:
            raise ValueError(
                f"Filter column '{column}' does not exist."
            )

        df = df[
            df[column].astype(str) == str(value)
        ]

    # =========================
    # EMPTY FILTER RESULT
    # =========================

    if df.empty:

        if plan.operation == "comparison":
            return []

        if (
            plan.operation in {
                "sum",
                "average",
                "count"
            }
            and not plan.dimensions
        ):

            if plan.metric == "avg_order_value":
                return {
                    "avg_order_value": 0
                }

            return {
                plan.metric: 0
            }

        return []

    # =========================
    # METRIC
    # =========================

    if plan.metric == "revenue":

        metric_series = df["revenue"]

    elif plan.metric == "profit":

        metric_series = df["profit"]

    elif plan.metric == "orders":

        metric_series = df["order_id"]

    elif plan.metric == "avg_order_value":

        metric_series = df["revenue"]

    else:

        raise ValueError(
            f"Unsupported metric: {plan.metric}"
        )

    # =========================
    # GROUPED QUERY
    # =========================

    if plan.dimensions:

        # -------------------------
        # AVERAGE ORDER VALUE
        # -------------------------

        if plan.metric == "avg_order_value":

            grouped = (
                df.groupby(plan.dimensions)
                .agg(
                    revenue=("revenue", "sum"),
                    orders=("order_id", "count")
                )
                .reset_index()
            )

            grouped["avg_order_value"] = (
                grouped["revenue"]
                / grouped["orders"]
            )

            result = grouped[
                plan.dimensions
                + ["avg_order_value"]
            ]

        # -------------------------
        # ORDERS
        # -------------------------

        elif plan.metric == "orders":

            result = (
                df.groupby(plan.dimensions)["order_id"]
                .count()
                .reset_index(name="orders")
            )

        # -------------------------
        # SUM
        # -------------------------

        elif plan.operation == "sum":

            result = (
                df.groupby(plan.dimensions)[plan.metric]
                .sum()
                .reset_index()
            )

        # -------------------------
        # AVERAGE
        # -------------------------

        elif plan.operation == "average":

            result = (
                df.groupby(plan.dimensions)[plan.metric]
                .mean()
                .reset_index()
            )

        # -------------------------
        # COUNT
        # -------------------------

        elif plan.operation == "count":

            result = (
                df.groupby(plan.dimensions)[plan.metric]
                .count()
                .reset_index()
            )

        # -------------------------
        # RANKING
        # -------------------------

        elif plan.operation == "ranking":

            if not plan.limit or plan.limit <= 0:
                raise ValueError(
                    "Ranking requires a positive limit."
                )

            result = (
                df.groupby(plan.dimensions)[plan.metric]
                .sum()
                .reset_index()
            )

        # -------------------------
        # CONTRIBUTION
        # -------------------------

        elif plan.operation == "contribution":

            grouped = (
                df.groupby(plan.dimensions)[plan.metric]
                .sum()
                .reset_index()
            )

            total = grouped[plan.metric].sum()

            if total == 0:

                grouped[
                    "contribution_percentage"
                ] = 0

            else:

                grouped[
                    "contribution_percentage"
                ] = (
                    grouped[plan.metric]
                    / total
                    * 100
                )

            result = grouped

        # -------------------------
        # COMPARISON
        # -------------------------

        elif plan.operation == "comparison":

            # =====================
            # TARGET COMPARISON
            # =====================

            if plan.comparison == "target":

                actual = (
                    df.groupby(
                        ["region", "month"],
                        as_index=False
                    )["revenue"]
                    .sum()
                )

                if targets.empty:
                    raise ValueError(
                        "Target dataset is empty."
                    )

                comparison = actual.merge(
                    targets,
                    on=["region", "month"],
                    how="left"
                )

                comparison = comparison.dropna(
                    subset=["target_revenue"]
                )

                if comparison.empty:
                    return []

                comparison["difference"] = (
                    comparison["revenue"]
                    - comparison["target_revenue"]
                )

                comparison["status"] = (
                    comparison.apply(
                        lambda row:
                        "Missed Target"
                        if row["revenue"]
                        < row["target_revenue"]
                        else "Met Target",
                        axis=1
                    )
                )

                result = comparison

            # =====================
            # YOY COMPARISON
            # =====================

            elif plan.comparison == "yoy":

                monthly_revenue = (
                    df.groupby("month")["revenue"]
                    .sum()
                    .reset_index()
                )

                monthly_revenue["year"] = (
                    monthly_revenue["month"]
                    .str[:4]
                    .astype(int)
                )

                current_year = (
                    monthly_revenue["year"].max()
                )

                previous_year = current_year - 1

                current_revenue = (
                    monthly_revenue[
                        monthly_revenue["year"]
                        == current_year
                    ]["revenue"]
                    .sum()
                )

                previous_revenue = (
                    monthly_revenue[
                        monthly_revenue["year"]
                        == previous_year
                    ]["revenue"]
                    .sum()
                )

                if previous_revenue == 0:

                    growth = None

                else:

                    growth = (
                        (
                            current_revenue
                            - previous_revenue
                        )
                        / previous_revenue
                        * 100
                    )

                result = {
                    "current_year": current_year,
                    "previous_year": previous_year,
                    "current_revenue": current_revenue,
                    "previous_revenue": previous_revenue,
                    "yoy_growth_percentage": growth
                }

            else:

                raise ValueError(
                    f"Unsupported comparison: "
                    f"{plan.comparison}"
                )

        else:

            raise ValueError(
                f"Unsupported operation: "
                f"{plan.operation}"
            )

    # =========================
    # NON-GROUPED QUERY
    # =========================

    else:

        if plan.metric == "orders":

            value = df["order_id"].count()

        elif plan.metric == "avg_order_value":

            orders = df["order_id"].count()

            if orders == 0:

                value = 0

            else:

                value = (
                    df["revenue"].sum()
                    / orders
                )

        elif plan.operation == "sum":

            value = metric_series.sum()

        elif plan.operation == "average":

            value = metric_series.mean()

        elif plan.operation == "count":

            value = metric_series.count()

        elif plan.operation == "comparison":

            if plan.comparison != "yoy":

                raise ValueError(
                    f"Unsupported comparison: "
                    f"{plan.comparison}"
                )

            monthly_revenue = (
                df.groupby("month")["revenue"]
                .sum()
                .reset_index()
            )

            monthly_revenue["year"] = (
                monthly_revenue["month"]
                .str[:4]
                .astype(int)
            )

            current_year = (
                monthly_revenue["year"].max()
            )

            previous_year = current_year - 1

            current_revenue = (
                monthly_revenue[
                    monthly_revenue["year"]
                    == current_year
                ]["revenue"]
                .sum()
            )

            previous_revenue = (
                monthly_revenue[
                    monthly_revenue["year"]
                    == previous_year
                ]["revenue"]
                .sum()
            )

            if previous_revenue == 0:

                growth = None

            else:

                growth = (
                    (
                        current_revenue
                        - previous_revenue
                    )
                    / previous_revenue
                    * 100
                )

            return {
                "current_year": current_year,
                "previous_year": previous_year,
                "current_revenue": current_revenue,
                "previous_revenue": previous_revenue,
                "yoy_growth_percentage": growth
            }

        else:

            raise ValueError(
                f"Unsupported operation: "
                f"{plan.operation}"
            )

        result = {
            plan.metric: value
        }

    # =========================
    # SORT RESULTS
    # =========================

    if hasattr(result, "sort_values"):

        if plan.operation == "contribution":

            sort_column = (
                "contribution_percentage"
            )

        elif plan.operation == "comparison":

            sort_column = "difference"

        else:

            sort_column = (
                "avg_order_value"
                if plan.metric == "avg_order_value"
                else "orders"
                if plan.metric == "orders"
                else plan.metric
            )

        if sort_column in result.columns:

            result = result.sort_values(
                by=sort_column,
                ascending=False
            )

        # =========================
        # TOP N
        # =========================

        if plan.limit:

            # Top N within each group
            if (
                plan.operation == "ranking"
                and len(plan.dimensions) > 1
            ):

                group_columns = (
                    plan.dimensions[:-1]
                )

                result = (
                    result
                    .groupby(
                        group_columns,
                        group_keys=False
                    )
                    .head(plan.limit)
                )

            # Normal Top N
            else:

                result = result.head(
                    plan.limit
                )

    return result