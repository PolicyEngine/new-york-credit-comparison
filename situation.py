def create_household_situation(inputs, reform_year):
    """Create a PolicyEngine situation based on household inputs."""
    # Initialize people with the household head
    people = {
        "you": {
            "age": {reform_year: inputs["head_age"]},
            "employment_income": {reform_year: inputs["income"]},
        }
    }

    # Add members to the household
    members = ["you"]

    # Add spouse if married
    if inputs["is_married"]:
        people["spouse"] = {
            "age": {reform_year: inputs["spouse_age"]},
            "employment_income": {
                reform_year: 0
            },  # Assuming spouse has no income for simplicity
        }
        members.append("spouse")

    # Add children if any
    for i, age in enumerate(inputs["child_ages"]):
        child_id = f"child_{i}"
        people[child_id] = {
            "age": {reform_year: age},
            "employment_income": {reform_year: 0},
        }
        members.append(child_id)

    # Create the full situation
    situation = {
        "people": people,
        "families": {"your_family": {"members": members.copy()}},
        "marital_units": {"your_marital_unit": {"members": members.copy()}},
        "tax_units": {"your_tax_unit": {"members": members.copy()}},
        "spm_units": {"your_spm_unit": {"members": members.copy()}},
        "households": {
            "your_household": {
                "members": members.copy(),
                "state_name": {reform_year: "NY"},
                "in_nyc": {reform_year: False},  # Can be made configurable
            }
        },
    }

    return situation
