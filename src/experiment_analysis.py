"""Analyze randomized Upworthy headline experiments."""

import argparse

import numpy as np
import pandas as pd
from scipy.stats import chisquare
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint, proportions_ztest

REQUIRED_COLUMNS = {
    "clickability_test_id",
    "impressions",
    "clicks",
    "headline",
}


def load_data(path):
    """Load and validate an Upworthy package-level CSV file."""
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    clean = data.copy()
    clean["impressions"] = pd.to_numeric(clean["impressions"], errors="coerce")
    clean["clicks"] = pd.to_numeric(clean["clicks"], errors="coerce")
    clean = clean.dropna(subset=["impressions", "clicks"])
    clean = clean[(clean["impressions"] > 0) & (clean["clicks"] >= 0)]
    clean = clean[clean["clicks"] <= clean["impressions"]]
    return clean


def sample_ratio_mismatch(experiment):
    """Test whether traffic is evenly allocated across experiment arms."""
    observed = experiment["impressions"].to_numpy(dtype=float)
    expected = np.repeat(observed.sum() / len(observed), len(observed))
    statistic, p_value = chisquare(observed, expected)
    return {"srm_statistic": statistic, "srm_p_value": p_value}


def analyze_experiment(data, test_id, control_index=0, alpha=0.05):
    """Compare every variant in one test with a preselected control."""
    experiment = data.loc[
        data["clickability_test_id"].astype(str) == str(test_id)
    ].copy()
    experiment = experiment.sort_values("impressions", ascending=False).reset_index(drop=True)

    if len(experiment) < 2:
        raise ValueError("The selected test must contain at least two valid arms.")
    if not 0 <= control_index < len(experiment):
        raise ValueError("control_index is outside the available experiment arms.")

    experiment["ctr"] = experiment["clicks"] / experiment["impressions"]
    intervals = [
        proportion_confint(clicks, impressions, alpha=alpha, method="wilson")
        for clicks, impressions in zip(experiment["clicks"], experiment["impressions"])
    ]
    experiment["ci_low"] = [interval[0] for interval in intervals]
    experiment["ci_high"] = [interval[1] for interval in intervals]

    control = experiment.iloc[control_index]
    p_values = []
    comparison_rows = []

    for index, variant in experiment.iterrows():
        if index == control_index:
            continue
        _, p_value = proportions_ztest(
            [variant["clicks"], control["clicks"]],
            [variant["impressions"], control["impressions"]],
        )
        p_values.append(p_value)
        comparison_rows.append(index)

    adjusted = multipletests(p_values, alpha=alpha, method="holm")[1]
    experiment["absolute_lift"] = experiment["ctr"] - control["ctr"]
    experiment["relative_lift"] = experiment["absolute_lift"] / control["ctr"]
    experiment["p_value_adjusted"] = np.nan
    experiment["significant"] = False

    for index, p_value in zip(comparison_rows, adjusted):
        experiment.loc[index, "p_value_adjusted"] = p_value
        experiment.loc[index, "significant"] = p_value < alpha

    experiment["is_control"] = experiment.index == control_index
    columns = [
        "headline",
        "impressions",
        "clicks",
        "ctr",
        "ci_low",
        "ci_high",
        "absolute_lift",
        "relative_lift",
        "p_value_adjusted",
        "significant",
        "is_control",
    ]
    return experiment[columns], sample_ratio_mismatch(experiment)


def main():
    """Run experiment analysis from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--test-id", required=True)
    parser.add_argument("--control-index", type=int, default=0)
    args = parser.parse_args()

    data = load_data(args.data)
    results, srm = analyze_experiment(data, args.test_id, args.control_index)
    print(results.to_string(index=False))
    print(f"\nSample-ratio-mismatch p-value: {srm['srm_p_value']:.6f}")


if __name__ == "__main__":
    main()
