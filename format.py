import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from constants import GREY, TEAL_ACCENT, ORANGE_ACCENT


def render_results(results, results_df):
    """Visualization function that shows tax credit values and net income changes."""
    if results_df.empty:
        st.warning("No results to display. Please run the simulation first.")
        return

    # Process dataframe
    df = prepare_data(results_df)

    # Show tax credit values
    st.subheader("Tax Credit Values")
    credit_fig = create_bar_chart(
        df,
        metrics={
            "Current Law": {
                "column": "baseline_ctc",
                "year": 2024,
                "color": GREY,
                "label": "Current ESCC",
            },
            "Hochul": {
                "column": "ctc_value",
                "years": [2025, 2026],
                "color": TEAL_ACCENT,
                "label": "Hochul's ESCC Expansion",
            },
            "WFTC": {
                "column": "wftc_value",
                "years": [2025, 2026, 2029],
                "color": ORANGE_ACCENT,
                "label": "WFTC Proposal",
            },
        },
        y_title="Credit Amount ($)",
    )
    st.plotly_chart(credit_fig, use_container_width=False)

    # Show net income changes
    st.subheader("Net Income Change")
    income_fig = create_bar_chart(
        df,
        metrics={
            "Hochul": {
                "column": "ctc_change",
                "years": [2025, 2026],
                "color": TEAL_ACCENT,
                "label": "Hochul's ESCC Expansion",
            },
            "WFTC": {
                "column": "wftc_change",
                "years": [2025, 2026, 2029],
                "color": ORANGE_ACCENT,
                "label": "WFTC Proposal",
            },
        },
        y_title="Net Income Change ($)",
    )
    st.plotly_chart(income_fig, use_container_width=False)


def prepare_data(results_df):
    """Process and clean the input dataframe."""
    # Get the current year and reform years data
    current_year_data = (
        results_df[results_df["year"] == 2024].copy()
        if 2024 in results_df["year"].values
        else pd.DataFrame()
    )
    reform_years_data = results_df[results_df["year"] > 2024].copy()

    # Combine the data
    df = pd.concat([current_year_data, reform_years_data])

    # Convert any numpy arrays to simple numbers
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.item() if isinstance(x, np.ndarray) and x.size == 1 else x
        )

    # Fill NaN values with 0
    df = df.fillna(0)

    return df


def create_bar_chart(df, metrics, y_title):
    """Create a bar chart with specified metrics and formatting.

    Args:
        df: DataFrame with the data
        metrics: Dictionary with metrics definition:
            {
                "Policy Name": {
                    "column": column_name,
                    "years": [list of years] or "year": single_year,
                    "color": color_code,
                    "label": legend_label
                }
            }
        y_title: Title for Y axis
    """
    fig = go.Figure()

    # List to keep track of policies for legend
    legend_items = []

    # Process each policy metric
    for policy_name, config in metrics.items():
        # Handle either single year or multiple years
        years = config.get("years", [])
        if "year" in config:
            years = [config["year"]]

        column = config["column"]
        color = config["color"]
        label = config.get("label", policy_name)

        # Add to legend items if not already there
        if policy_name not in legend_items:
            legend_items.append(policy_name)

        # Add a bar for each year
        for year in years:
            value = extract_value(df, year, column)

            x_label = f"{label.split(' ')[0]} {year}" if year != 2024 else label

            fig.add_trace(
                go.Bar(
                    x=[x_label],
                    y=[value],
                    name=policy_name,
                    marker_color=color,
                    showlegend=False,  # We'll add custom legend items later
                )
            )

            # Add value label if value exists
            if value > 0:
                fig.add_annotation(
                    x=x_label,
                    y=value,
                    text=f"${int(value)}",
                    showarrow=False,
                    yshift=10,
                )

    # Create custom legend
    legend_colors = {policy: config["color"] for policy, config in metrics.items()}

    for policy in legend_items:
        fig.add_trace(
            go.Bar(
                x=[None],
                y=[None],
                name=metrics[policy]["label"],
                marker_color=legend_colors[policy],
                showlegend=True,
            )
        )

    # Layout configuration
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis_title="",
        yaxis_title=y_title,
        yaxis_tickformat="$,.0f",
        height=500,
        margin=dict(t=100),
    )

    return fig


def extract_value(df, year, column):
    """Safely extract a value from the dataframe."""
    value = 0
    if year in df["year"].values and column in df.columns:
        data = df[df["year"] == year]
        if not data.empty:
            value = data[column].values[0]
            if pd.isna(value) or not isinstance(value, (int, float)):
                value = 0
    return value
