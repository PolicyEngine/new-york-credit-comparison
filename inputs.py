import streamlit as st


def render_household_inputs():
    """Render input fields for household information in a two-column layout."""
    # Create two main columns
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.subheader("Household Information")

        # Employment income
        income = st.number_input(
            "How much income did you receive in wages and salaries?",
            min_value=0,
            max_value=1000000,
            value=30000,
            step=1000,
        )

        # Marital status
        is_married = st.checkbox("Are you married?", value=False)

        # Ages for adults - in sub-columns when married
        if is_married:
            head_col, spouse_col = st.columns(2)
            with head_col:
                head_age = st.number_input(
                    "How old are you?", min_value=16, max_value=100, value=40
                )
            with spouse_col:
                spouse_age = st.number_input(
                    "How old is your spouse?", min_value=16, max_value=100, value=40
                )
        else:
            head_age = st.number_input(
                "How old are you?", min_value=16, max_value=100, value=40
            )
            spouse_age = None

    with right_col:
        st.subheader("Children")

        # Number of children
        num_children = st.number_input(
            "How many children do you have?",
            min_value=0,
            max_value=6,
            value=0,
            step=1,
        )

        # Child ages if there are children
        child_ages = []
        if num_children > 0:
            # Create rows with two children per row (up to 3 rows for 6 children max)
            for i in range(0, num_children, 2):
                # Create two columns for each pair of children
                cols = st.columns(2)

                # First child in pair
                with cols[0]:
                    child_age = st.number_input(
                        f"Age of child {i+1}",
                        min_value=0,
                        max_value=23,
                        value=min(i * 2, 17),
                        key=f"child_{i}",
                    )
                    child_ages.append(child_age)

                # Second child in pair (if exists)
                if i + 1 < num_children:
                    with cols[1]:
                        child_age = st.number_input(
                            f"Age of child {i+2}",
                            min_value=0,
                            max_value=23,
                            value=min((i + 1) * 2, 17),
                            key=f"child_{i+1}",
                        )
                        child_ages.append(child_age)

    return {
        "income": income,
        "is_married": is_married,
        "head_age": head_age,
        "spouse_age": spouse_age,
        "num_children": num_children,
        "child_ages": child_ages,
    }
