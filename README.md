# The Trust Deficit — Agoda vs Booking.com Review Score Analysis

> Why do identical hotels score 0.3–0.5 points lower on Agoda than 
> Booking.com — and what should Agoda do about it?

## Key Findings

- Gap is statistically significant: mean = −0.40, p = 0.020, t = −6.93
- Primary driver is **sampling bias (H1)**: Agoda reviewers are 60.4% 
  Asian vs. 0% on Booking.com for the same hotels — directly explaining 
  the two largest sub-score gaps (Location: −0.60, Room Comfort: −0.53)
- BA revenue model: 2 At-Risk hotels × $3,456/year = **$6,912 annual 
  GMV at risk** from supplier allocation reduction

## Methodology

| Step | Tool | Output |
|------|------|--------|
| Hotel selection | Manual seed (50 verified hotels) | `data/hotel_summary.csv` |
| Review scraping | Apify (Agoda + Booking.com) | Raw review CSVs |
| Data cleaning | Python (pandas) | 4 analysis-ready CSVs |
| Statistical analysis | SAS Studio | Paired t-test, regression, variance test |
| Visualization & strategy | PowerPoint, Word | Deck + PRD |

## Deliverables

| File | Description |
|------|-------------|
| `The_Trust_Deficit_Deck.pptx` | Consulting deck — gap analysis, H1 findings, BA risk model, strategic 2x2 |
| `Agoda_PRD_Contextual_Review_Routing.docx` | PM deliverable — full PRD for Contextual Review Routing feature |
| `SAS_Results.pdf` | Statistical output — paired t-test, regression, variance analysis |

## Project Structure

    agoda-trust-deficit/
    ├── data/
    │   ├── hotel_summary.csv
    │   ├── reviewer_profile.csv
    │   ├── reviews_clean.csv
    │   └── sub_scores.csv
    ├── scraping/
    │   ├── hotel_seeds.py
    │   ├── manual_seed.py
    │   └── scrape_reviews.py
    ├── analysis/
    │   └── sas_program.sas
    ├── notebooks/
    │   └── clean_and_analyze.py
    └── outputs/
        ├── The_Trust_Deficit_Deck.pptx
        ├── Agoda_PRD_Contextual_Review_Routing.docx
        └── SAS_Results.pdf


## Skills Demonstrated

`Python` `SAS` `Apify` `Selenium` `Statistical Analysis` 
`Hypothesis Testing` `Product Thinking` `Business Case Modelling` 
`Strategy Frameworks`

## Domain Coverage

| Domain | Deliverable |
|--------|-------------|
| Data Analytics | SAS analysis — t-test, regression, variance test, reviewer profiling |
| Business Analysis | Risk tier segmentation, revenue at risk model |
| Product Management | PRD — Contextual Review Routing feature spec |
| Strategy / Consulting | Competitor benchmark, strategic 2x2, Trust as Moat recommendation |

## Markets

Bali · Singapore · Tokyo — 3 luxury properties across Agoda-stronghold 
Asian markets

## Note on Data Collection

A Selenium-based scraper was built first but was blocked by anti-bot 
measures on both platforms. Apify was used for final data collection — 
consistent with professional data team practice. The full scraping 
pipeline is retained in `scraping/` for reference.
