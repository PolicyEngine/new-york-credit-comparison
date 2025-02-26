from situation import create_household_situation
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import create_wftc_reform, create_ctc_reform
from constants import REFORM_YEARS, CURRENT_YEAR
import pandas as pd


def run_simulations(inputs):
    """Run all simulations and return the results."""
    results = {}

    # First calculate baseline for current year
    baseline_situation = create_household_situation(inputs, CURRENT_YEAR)
    baseline = Simulation(situation=baseline_situation)
    baseline_income = baseline.calculate("household_net_income", CURRENT_YEAR)
    baseline_ctc = baseline.calculate("ny_ctc", CURRENT_YEAR)

    # Create initial dataframe
    initial_df = pd.DataFrame(
        {
            "baseline_income": [baseline_income],
            "baseline_ctc": [baseline_ctc],
            "year": [CURRENT_YEAR],
        }
    )
    all_results = [initial_df]

    # Now run simulations for each reform year
    for year in REFORM_YEARS:
        # Create base household situation for this year
        situation = create_household_situation(inputs, year)

        # Baseline simulation (no reforms)
        baseline_sim = Simulation(situation=situation)
        baseline_net_income = baseline_sim.calculate("household_net_income", year)

        # WFTC reform simulation
        wftc_reform_dict = create_wftc_reform(year)
        wftc_reform = Reform.from_dict(wftc_reform_dict, country_id="us")
        wftc_sim = Simulation(situation=situation, reform=wftc_reform)
        wftc_net_income = wftc_sim.calculate("household_net_income", year)
        wftc_value = wftc_sim.calculate("ny_working_families_tax_credit", year)

        # CTC reform simulation
        ctc_reform_dict = create_ctc_reform(year)
        ctc_reform = Reform.from_dict(ctc_reform_dict, country_id="us")
        ctc_sim = Simulation(situation=situation, reform=ctc_reform)
        ctc_net_income = ctc_sim.calculate("household_net_income", year)
        ctc_value = ctc_sim.calculate("basic_income", year)

        # Store results for this year
        year_df = pd.DataFrame(
            {
                "year": [year],
                "baseline_income": [baseline_net_income],
                "baseline_ctc": [baseline_ctc],
                "wftc_reform_income": [wftc_net_income],
                "wftc_value": [wftc_value],
                "wftc_change": [wftc_net_income - baseline_net_income],
                "ctc_reform_income": [ctc_net_income],
                "ctc_value": [ctc_value],
                "ctc_change": [ctc_net_income - baseline_net_income],
            }
        )

        all_results.append(year_df)

        # Also store in dictionary format for backward compatibility
        results[year] = {
            "baseline": {
                "net_income": baseline_net_income,
                "baseline_ctc": baseline_ctc,
            },
            "wftc_reform": {
                "net_income": wftc_net_income,
                "wftc_value": wftc_value,
                "change": wftc_net_income - baseline_net_income,
            },
            "ctc_reform": {
                "net_income": ctc_net_income,
                "ctc_value": ctc_value,
                "change": ctc_net_income - baseline_net_income,
            },
        }

    # Combine all dataframes
    results_df = pd.concat(all_results, ignore_index=True)

    return results, results_df
