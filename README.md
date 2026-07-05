# The Trust Deficit — Agoda vs Booking.com Review Score Analysis

> Why do identical hotels score 0.3–0.5 points lower on Agoda than 
> Booking.com; and what should Agoda do about it?

## Key Findings

- A consistent **−0.37 rating gap** was observed across all **10 hotels** 
  in Bali, Singapore, and Tokyo (paired t-test: t = −11.04, p < .0001, 
  DF = 9) — a large-sample, statistically robust result, up from an 
  initial 3-hotel pilot (DF=2)
- Gap concentrates most in **Room Comfort (−0.41)**, followed by 
  **Location (−0.37)** and **Staff Performance (−0.33)**; Cleanliness 
  shows the smallest gap (−0.14)
- **Sampling bias (H1) — supported**: Agoda's reviewer base is 65.1% 
  Asian vs. Booking.com's 16.9% (both platforms now have ~100% 
  nationality data captured). Controlling for hotel and platform via 
  fixed effects (N=1,850 reviews), reviewer nationality significantly 
  predicts score (p = 0.027); once nationality is accounted for, 
  platform itself has no remaining explanatory power (p = 0.89). The 
  platform-level score gap is best explained by *who* reviews on each 
  platform, not a platform-caused experience difference
- **OTA-caused friction (H3) — plausible, not statistically tested**: 
  review text suggests booking confirmation and check-in issues occur, 
  but this analysis did not quantitatively test H3 as a driver of the 
  aggregate gap; it remains a secondary, qualitative hypothesis worth 
  further investigation independent of the sampling-bias finding above
- **Secondary finding (H2)**: Booking.com reviews show significantly 
  higher score variance than Agoda's (Folded F test, p < .0001) — a 
  separate, confirmed pattern
- BA revenue model: 7 At-Risk hotels × $3,456/year = **$24,192 annual 
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

Bali · Singapore · Tokyo — 10 luxury properties across Agoda-stronghold 
Asian markets

## Note on Data Collection

A Selenium-based scraper was built first but was blocked by anti-bot 
measures on both platforms. Apify was used for final data collection — 
consistent with professional data team practice. The full scraping 
pipeline is retained in `scraping/` for reference.
