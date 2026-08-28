# Product Experimentation: Upworthy Headline A/B Tests

An end-to-end experimentation project using the **Upworthy Research Archive**, a real collection of randomized headline and image experiments conducted from 2013 to 2015.

The archive contains 32,487 experiments, 150,817 experiment arms and more than 538 million participant assignments. This project focuses on decision quality: traffic validation, uncertainty, effect size and multiple-comparison control—not simply selecting the highest observed CTR.

## Business question

How should a content or growth team decide whether an experimental variant is reliable enough to ship?

## Dataset

- **Source:** [Upworthy Research Archive](https://osf.io/jd64p/)
- **Documentation:** [Archive methodology and data dictionary](https://upworthy.natematias.com/about-the-archive.html)
- **Research paper:** [Scientific Data, 2021](https://doi.org/10.1038/s41597-021-00934-7)
- **License:** CC BY 4.0
- **Unit of analysis:** headline/image package within a randomized test
- **Primary metric:** click-through rate (clicks ÷ impressions)

The archive maintainers reported randomization concerns affecting some tests from June 2013 to January 2014. Any confirmatory use should follow their current guidance and exclude or flag experiments carrying randomization-imbalance risk.

Data is downloaded from the original archive and is not committed to this repository.

## Analytical framework

1. Validate required fields and remove zero-impression arms.
2. Check traffic allocation with a sample-ratio-mismatch test.
3. Calculate CTR and Wilson confidence intervals for every arm.
4. Compare variants with a preselected control using two-proportion z-tests.
5. Apply Holm correction when an experiment has multiple variants.
6. Report absolute lift, relative lift and adjusted statistical significance.
7. Separate statistical evidence from the final product recommendation.

## Decision table

| Check | Why it matters |
|---|---|
| Sample-ratio mismatch | Detects allocation or instrumentation problems |
| Confidence interval | Shows uncertainty around CTR |
| Absolute lift | Quantifies practical impact in percentage points |
| Relative lift | Communicates change versus control |
| Adjusted p-value | Controls false positives across multiple variants |
| Risk flag | Prevents unreliable experiments entering decisions |

## Repository structure

```text
data/                           Download instructions; raw data is excluded
src/experiment_analysis.py      Reusable experiment-analysis functions and CLI
tests/test_experiment_analysis.py
requirements.txt
.github/workflows/python.yml
```

## Run the analysis

```bash
git clone https://github.com/AtifElmasry/ad-bidding-ab-test-zalando-case-study.git
cd ad-bidding-ab-test-zalando-case-study
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Download the exploratory packages file following [data/README.md](data/README.md), then run:

```bash
python src/experiment_analysis.py \
  --data data/upworthy-archive-exploratory-packages-03.12.2020.csv \
  --test-id YOUR_TEST_ID
```

The command prints an arm-level decision table and the sample-ratio-mismatch result.

## Skills demonstrated

Experiment design, KPI definition, data-quality checks, A/B/n testing, confidence intervals, effect sizes, multiple testing, reproducible Python and responsible interpretation.

## Limitations

- Results apply to Upworthy’s historical media context.
- Aggregate arm data does not support user-level heterogeneity analysis.
- Statistical significance does not guarantee meaningful business value.
- A control must be selected before reviewing results to avoid biased comparisons.
- Tests flagged by the archive’s updated randomization guidance should not be used for confirmatory claims.

## Author

[Atif Elmasry](https://github.com/AtifElmasry) · [LinkedIn](https://www.linkedin.com/in/tioatifelmasry/)
