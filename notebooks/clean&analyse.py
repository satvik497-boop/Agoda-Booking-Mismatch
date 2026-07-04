"""
The Trust Deficit — Data Cleaning + Analysis Ready Output
Inputs:  bali_a.csv, singapore_a.csv, tokyo_a.csv  (Booking scraper - has both platforms)
         bali_b.csv, singapore_b.csv, tokyo_b.csv  (Agoda scraper - Agoda-only reviews)
Outputs: reviews_clean.csv      — review-level, SAS-ready
         hotel_summary.csv      — hotel-level scores + gap
         sub_scores.csv         — sub-score breakdown by category
         reviewer_profile.csv   — nationality + trip type breakdown
"""

import pandas as pd
import numpy as np
import os

# ── CONFIG ────────
DATA_DIR = "." 
OUT_DIR  = "output"
os.makedirs(OUT_DIR, exist_ok=True)

CITIES = ["bali", "singapore", "tokyo"]

HOTEL_NAMES = {
    "bali":      "Four Seasons Resort Bali at Sayan",
    "singapore": "Marina Bay Sands",
    "tokyo":     "Park Hyatt Tokyo",
}

TIERS = {
    "bali":      "Luxury",
    "singapore": "Luxury",
    "tokyo":     "Luxury",
}

# Asian vs Western nationality classification for H1
ASIAN_COUNTRIES = {
    "Japan", "China", "South Korea", "Indonesia", "Singapore",
    "Thailand", "Malaysia", "India", "Philippines", "Vietnam",
    "Taiwan", "Hong Kong", "Cambodia", "Myanmar", "Bangladesh"
}

# ── STEP 1: BUILDING REVIEW-LEVEL DATASET ──────────────────────────

all_reviews = []

for city in CITIES:
    print(f"\nProcessing {city}...")

    # ── _a file: Booking scraper (has both Agoda + Booking reviews) ──
    df_a = pd.read_csv(f"{DATA_DIR}/{city}_a.csv")

    # Extract aggregate scores (same for all rows in this hotel)
    agoda_agg   = df_a["agodaAggregateReviewScore"].iloc[0]
    booking_agg = df_a["bookingAggregateReviewScore"].iloc[0]

    # Clean review-level columns
    df_a_clean = pd.DataFrame({
        "city":        city.title(),
        "hotel_name":  HOTEL_NAMES[city],
        "tier":        TIERS[city],
        "platform":    df_a["reviewProviderText"].str.strip(),
        "score":       pd.to_numeric(df_a["rating"], errors="coerce"),
        "nationality": df_a["reviewerCountryName"].fillna("Unknown"),
        "trip_type":   df_a["reviewerGroupName"].fillna("Unknown"),
        "room_type":   df_a["reviewerRoomTypeName"].fillna("Unknown"),
        "stay_nights": pd.to_numeric(df_a["reviewerLengthOfStay"], errors="coerce"),
        "review_text": df_a["reviewComments"].fillna("") + " " +
                       df_a["reviewPositives"].fillna("") + " " +
                       df_a["reviewNegatives"].fillna(""),
        "review_date": df_a["reviewDate"],
        "source_file": f"{city}_a",
        "agoda_agg_score":   agoda_agg,
        "booking_agg_score": booking_agg,
    })

    # ── _b file: Agoda scraper (Agoda-only reviews, richer text) ──
    df_b = pd.read_csv(f"{DATA_DIR}/{city}_b.csv")

    df_b_clean = pd.DataFrame({
        "city":        city.title(),
        "hotel_name":  HOTEL_NAMES[city],
        "tier":        TIERS[city],
        "platform":    "Agoda",
        "score":       pd.to_numeric(df_b["rating"], errors="coerce"),
        "nationality": df_b["travelerType"].fillna("Unknown") if "travelerType" in df_b.columns else "Unknown",
        "trip_type":   df_b["travelerType"].fillna("Unknown") if "travelerType" in df_b.columns else "Unknown",
        "room_type":   "Unknown",
        "stay_nights": pd.to_numeric(df_b["numberOfNights"], errors="coerce") if "numberOfNights" in df_b.columns else np.nan,
        "review_text": df_b["likedText"].fillna("") + " " + df_b["dislikedText"].fillna(""),
        "review_date": df_b["reviewDate"] if "reviewDate" in df_b.columns else np.nan,
        "source_file": f"{city}_b",
        "agoda_agg_score":   agoda_agg,
        "booking_agg_score": booking_agg,
    })

    all_reviews.append(df_a_clean)
    all_reviews.append(df_b_clean)

    print(f"  _a: {len(df_a_clean)} reviews | Agoda agg: {agoda_agg} | Booking agg: {booking_agg}")
    print(f"  _b: {len(df_b_clean)} reviews")

reviews = pd.concat(all_reviews, ignore_index=True)
reviews["review_text"] = reviews["review_text"].str.strip()

# Derived columns# 
reviews["nationality_known"] = (reviews["nationality"] != "Unknown").astype(int)
reviews["is_asian_reviewer"] = np.where(
    reviews["nationality_known"] == 1,
    reviews["nationality"].isin(ASIAN_COUNTRIES).astype(int),
    np.nan  # missing nationality is NOT coded as "not Asian"
)
reviews["is_solo"] = reviews["trip_type"].str.lower().str.contains("solo").fillna(False).astype(int)
reviews["score_gap"] = reviews["agoda_agg_score"] - reviews["booking_agg_score"]

print(f"\nTotal reviews: {len(reviews)}")
print(f"Platform breakdown:\n{reviews['platform'].value_counts()}")

reviews.to_csv(f"{OUT_DIR}/reviews_clean.csv", index=False)
print(f"\nSaved reviews_clean.csv")

# ── STEP 2: HOTEL SUMMARY TABLE ──────────────────────────────────

hotel_summary = pd.DataFrame()

rows = []
for city in CITIES:
    df_a = pd.read_csv(f"{DATA_DIR}/{city}_a.csv")

    agoda_reviews   = df_a[df_a["reviewProviderText"] == "Agoda"]["rating"]
    booking_reviews = df_a[df_a["reviewProviderText"] == "Booking.com"]["rating"]

    rows.append({
        "hotel_name":           HOTEL_NAMES[city],
        "city":                 city.title(),
        "tier":                 TIERS[city],

        # Aggregate scores (platform-level)
        "agoda_agg_score":      df_a["agodaAggregateReviewScore"].iloc[0],
        "booking_agg_score":    df_a["bookingAggregateReviewScore"].iloc[0],
        "score_gap":            round(
                                    df_a["agodaAggregateReviewScore"].iloc[0] -
                                    df_a["bookingAggregateReviewScore"].iloc[0], 2),

        # Sample-level averages from scraped reviews
        "agoda_sample_avg":     round(agoda_reviews.mean(), 2) if len(agoda_reviews) > 0 else None,
        "booking_sample_avg":   round(booking_reviews.mean(), 2) if len(booking_reviews) > 0 else None,
        "agoda_sample_n":       len(agoda_reviews),
        "booking_sample_n":     len(booking_reviews),
        "agoda_sample_std":     round(agoda_reviews.std(), 2) if len(agoda_reviews) > 0 else None,
        "booking_sample_std":   round(booking_reviews.std(), 2) if len(booking_reviews) > 0 else None,

        # Reviewer mix
         "pct_asian_reviewer": round(
             df_a.loc[df_a["reviewerCountryName"].notna(), "reviewerCountryName"]
             .isin(ASIAN_COUNTRIES).mean() * 100, 1),
         "pct_nationality_known": round(df_a["reviewerCountryName"].notna().mean() * 100, 1),
        "agoda_review_count":   df_a["agodaReviewsCount"].iloc[0],
        "booking_review_count": df_a["bookingReviewsCount"].iloc[0],
    })

hotel_summary = pd.DataFrame(rows)
hotel_summary.to_csv(f"{OUT_DIR}/hotel_summary.csv", index=False)

print("\n=== HOTEL SUMMARY ===")
print(hotel_summary[["hotel_name", "city", "agoda_agg_score",
                      "booking_agg_score", "score_gap"]].to_string(index=False))

# ── STEP 3: SUB-SCORE BREAKDOWN ──────────────────────────────────

sub_rows = []
categories = ["cleanliness", "facilities", "location",
              "roomComfort", "staffPerformance", "valueForMoney"]

for city in CITIES:
    df_a = pd.read_csv(f"{DATA_DIR}/{city}_a.csv")
    row = df_a.iloc[0]

    for i, cat in enumerate(categories):
        agoda_score   = row.get(f"agodaAggregateDetailedReviewScore/{i}/score", None)
        booking_score = row.get(f"bookingAggregateDetailedReviewScore/{i}/score", None)

        sub_rows.append({
            "city":          city.title(),
            "hotel_name":    HOTEL_NAMES[city],
            "category":      cat,
            "agoda_score":   agoda_score,
            "booking_score": booking_score,
            "gap":           round(float(agoda_score) - float(booking_score), 2)
                             if agoda_score and booking_score else None,
        })

sub_scores = pd.DataFrame(sub_rows)
sub_scores.to_csv(f"{OUT_DIR}/sub_scores.csv", index=False)

print("\n=== SUB-SCORE GAPS (Agoda - Booking) ===")
pivot = sub_scores.pivot_table(
    values="gap", index="category", columns="city", aggfunc="mean"
)
print(pivot.round(2).to_string())

# ── STEP 4: REVIEWER PROFILE ──────────────────────────────────────

profile_rows = []
for city in CITIES:
    df_a = pd.read_csv(f"{DATA_DIR}/{city}_a.csv")

    for platform in ["Agoda", "Booking.com"]:
        sub = df_a[df_a["reviewProviderText"] == platform]
        if len(sub) == 0:
            continue

        profile_rows.append({
            "city":             city.title(),
            "platform":         platform,
            "n_reviews":        len(sub),
            "avg_score":        round(sub["rating"].mean(), 2),
            "pct_asian": round(sub.loc[sub["reviewerCountryName"].notna(), "reviewerCountryName"].isin(ASIAN_COUNTRIES).mean() * 100, 1) if sub["reviewerCountryName"].notna().any() else None,
            "pct_nationality_known": round(sub["reviewerCountryName"].notna().mean() * 100, 1),
            "pct_couple":       round(sub["reviewerGroupName"].str.lower().str.contains("couple").mean() * 100, 1),
            "pct_solo":         round(sub["reviewerGroupName"].str.lower().str.contains("solo").mean() * 100, 1),
            "pct_family":       round(sub["reviewerGroupName"].str.lower().str.contains("family").mean() * 100, 1),
            "pct_business":     round(sub["reviewerGroupName"].str.lower().str.contains("business").mean() * 100, 1),
            "avg_stay_nights":  round(pd.to_numeric(sub["reviewerLengthOfStay"], errors="coerce").mean(), 1),
            "score_std":        round(sub["rating"].std(), 2),
        })

reviewer_profile = pd.DataFrame(profile_rows)
reviewer_profile.to_csv(f"{OUT_DIR}/reviewer_profile.csv", index=False)

print("\n=== REVIEWER PROFILE ===")
print(reviewer_profile[["city", "platform", "n_reviews",
                         "avg_score", "pct_asian", "pct_solo",
                         "pct_couple"]].to_string(index=False))

print(f"\n✅ All done. Output files in '{OUT_DIR}/':")
print("   reviews_clean.csv")
print("   hotel_summary.csv")
print("   sub_scores.csv")
print("   reviewer_profile.csv")
print("\nNext step: import these into SAS for H1/H2/H3 analysis")
