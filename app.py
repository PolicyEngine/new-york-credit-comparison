# app.py

import streamlit as st
from inputs import render_household_inputs
from simulation import run_simulations
from format import render_results
from constants import colors


def set_page_config():
    st.set_page_config(
        page_title="NY WFTC and ESCC Expansion Calculator", 
        page_icon="📊"
    )

    # App title and description
    st.markdown(
        f"""
        <h1 style="font-family: Roboto;">
            <span style="color: {colors["TEAL_ACCENT"]}; font-weight: bold;">
                NY WFTC and ESCC Expansion
            </span>
            <span style="color: {colors["TEAL_ACCENT"]}; font-weight: normal;">
                Calculator
            </span>
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "Compare the impact of WFTC and the ESCC expansion proposals on New York households across different years."
    )
    st.divider()

    # Inject custom CSS for the "Calculate" primary button
    st.markdown(
        f"""
        <style>
        div.stButton > button:first-child {{
            background-color: {colors["BLUE"]} !important;
            color: {colors["WHITE"]} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    """Main application function."""
    set_page_config()

    # Render the inputs
    inputs = render_household_inputs()

    # Calculate button
    if st.button("Calculate", type="primary"):
        with st.spinner("Running simulations..."):
            # Run simulations
            results, results_df = run_simulations(inputs)

            # Display results
            render_results(results, results_df)

    # Add information about the reforms
    with st.expander("About the Reforms"):
        st.markdown(
            """
        ### Working Family Tax Credit (WFTC)
        The NY WFTC reform includes:
        - Taking effect from 2025 onwards
        - Maximum credit amounts increasing over time:
          - $550 in 2025
          - $854 in 2026
          - $1,091 in 2027
          - $1,338 in 2028
          - $1,822 in 2029 and beyond
        - Adjusted phase-out thresholds over time:
          - \$75,000/$110,000 in 2025
          - \$65,000/$110,000 in 2026
          - \$55,000/$110,000 in 2027
          - \$45,000/$90,000 in 2028
          - \$28,462/$56,924 in 2029
        - Phases-out at a 2 percent rate
        - Minimum benefit of $100 per child starting in 2026:
        - Phases out the NY EITC over 5 years
        - Limits the dependent exemption to those ineligible for the WFTC

        ### Empire State Child Credit Expansion
        The enhanced ESSC reform includes:
        - Increasing benefit amounts:
          - $1,000 for children under age 4, beginning in 2025
          - $500 for children 4-16 in 2026
        - Eliminating the income requirement for low-income families
          - Households below the phaseout threshold receive the maximum benefit
        - Same phase-out rate and thresholds:
          - Phase-out rate of 1.65%
          - $110,000 for joint filers
          - $75,000 for single, head of household, and surviving spouse filers
          - $55,000 for married filing separately
        - Reform decouples ESCC from pre-TCJA Child Tax Credit
        """
        )


if __name__ == "__main__":
    main()
