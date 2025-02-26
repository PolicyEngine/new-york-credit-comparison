def create_wftc_reform(reform_year):
    return {
        "gov.contrib.states.ny.wftc.in_effect": {"2023-01-01.2100-12-31": True},
        "gov.contrib.states.ny.wftc.amount.max": {
            "2026-01-01.2026-12-31": 854,
            "2027-01-01.2027-12-31": 1091,
            "2028-01-01.2028-12-31": 1338,
            "2029-01-01.2100-12-31": 1822,
        },
        "gov.contrib.states.ny.wftc.amount.min": {"2025-01-01.2025-12-31": 0},
        "gov.contrib.states.ny.wftc.reduction.single[1].threshold": {
            "2029-01-01.2100-12-31": 28462
        },
        "gov.contrib.states.ny.wftc.reduction.married[1].threshold": {
            "2029-01-01.2100-12-31": 56924
        },
    }


def create_ctc_reform(reform_year):
    return {
        "gov.contrib.ubi_center.basic_income.phase_out.rate": {
            "2025-01-01.2100-12-31": 0.0165
        },
        "gov.states.ny.tax.income.credits.ctc.amount.minimum": {
            "2025-01-01.2100-12-31": 0
        },
        "gov.states.ny.tax.income.credits.ctc.amount.percent": {
            "2025-01-01.2100-12-31": 0
        },
        "gov.contrib.ubi_center.basic_income.phase_out.threshold.JOINT": {
            "2025-01-01.2100-12-31": 110000
        },
        "gov.contrib.ubi_center.basic_income.phase_out.threshold.SINGLE": {
            "2025-01-01.2100-12-31": 75000
        },
        "gov.contrib.ubi_center.basic_income.phase_out.threshold.SEPARATE": {
            "2025-01-01.2100-12-31": 55000
        },
        "gov.contrib.ubi_center.basic_income.amount.person.by_age[0].amount": {
            "2025-01-01.2100-12-31": 1000
        },
        "gov.contrib.ubi_center.basic_income.amount.person.by_age[1].amount": {
            "2025-01-01.2025-12-31": 330,
            "2026-01-01.2100-12-31": 500,
        },
        "gov.contrib.ubi_center.basic_income.amount.person.by_age[1].threshold": {
            "2025-01-01.2100-12-31": 4
        },
        "gov.contrib.ubi_center.basic_income.amount.person.by_age[2].threshold": {
            "2025-01-01.2100-12-31": 17
        },
        "gov.contrib.ubi_center.basic_income.phase_out.threshold.SURVIVING_SPOUSE": {
            "2025-01-01.2100-12-31": 75000
        },
        "gov.contrib.ubi_center.basic_income.phase_out.threshold.HEAD_OF_HOUSEHOLD": {
            "2025-01-01.2100-12-31": 75000
        },
    }
