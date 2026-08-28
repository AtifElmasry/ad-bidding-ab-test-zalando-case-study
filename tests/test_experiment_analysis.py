"""Tests for the experiment-analysis pipeline."""

import pandas as pd
import pytest

from src.experiment_analysis import analyze_experiment, sample_ratio_mismatch


@pytest.fixture
def experiment_data():
    """Return a small deterministic two-arm experiment."""
    return pd.DataFrame(
        {
            "clickability_test_id": ["test-1", "test-1"],
            "headline": ["Control headline", "Variant headline"],
            "impressions": [10_000, 10_000],
            "clicks": [500, 620],
        }
    )


def test_analysis_calculates_lift_and_control(experiment_data):
    """The variant should be compared with the selected control."""
    results, _ = analyze_experiment(experiment_data, "test-1")

    assert results.loc[0, "is_control"]
    assert results.loc[1, "absolute_lift"] == pytest.approx(0.012)
    assert results.loc[1, "relative_lift"] == pytest.approx(0.24)


def test_balanced_traffic_has_no_srm(experiment_data):
    """Equal assignment should not trigger sample-ratio mismatch."""
    result = sample_ratio_mismatch(experiment_data)
    assert result["srm_p_value"] == pytest.approx(1.0)
