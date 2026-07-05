"""
The Trust Deficit — Data Cleaning + Analysis (v3: 10 hotels, new schema)
Inputs:  {hotel_id}_a.csv  (Agoda-only reviews, via Fast Agoda Reviews Scraper)
         {hotel_id}_b.csv  (Booking.com-only reviews, via Booking Reviews Scraper)
Outputs: reviews_clean.csv, hotel_summary.csv, sub_scores.csv, reviewer_profile.csv
"""

import pandas as pd
import numpy as np
import os

DATA_DIR = "."
OUT_DIR  = "output"
os.makedirs(OUT_DIR, exist_ok=True)

HOTELS = [
    {"id": "4season_bali_atSayan",        "city": "Bali",      "hotel_name": "Four Seasons Resort Bali at Sayan", "tier": "Luxury"},
    {"id": "st_regis_bali_resort",        "city": "Bali",      "hotel_name": "The St. Regis Bali Resort",          "tier": "Luxury"},
    {"id": "alila_villas_uluwatu",        "city": "Bali",      "hotel_name": "Alila Villas Uluwatu",                "tier": "Luxury"},
    {"id": "marina_bay_sands",            "city": "Singapore", "hotel_name": "Marina Bay Sands",                    "tier": "Luxury"},
    {"id": "raffles_singapore",           "city": "Singapore", "hotel_name": "Raffles Singapore",                   "tier": "Luxury"},
    {"id": "mandarin_oriental_singapore", "city": "Singapore", "hotel_name": "Mandarin Oriental Singapore",         "tier": "Luxury"},
    {"id": "Park_Hayatt",                 "city": "Tokyo",      "hotel_name": "Park Hyatt Tokyo",                    "tier": "Luxury"},
    {"id": "mandarin_oriental_tokyo",     "city": "Tokyo",      "hotel_name": "Mandarin Oriental Tokyo",             "tier": "Luxury"},
    {"id": "the_peninsula",               "city": "Tokyo",      "hotel_name": "The Peninsula Tokyo",                 "tier": "Luxury"},
    {"id": "ritz_carlton",                "city": "Tokyo",      "hotel_name": "The Ritz-Carlton Tokyo",              "tier": "Luxury"},
]

ASIAN_COUNTRIES = {
    "Japan", "China", "South Korea", "Indonesia", "Singapore",
    "Thailand", "Malaysia", "India", "Philippines", "Vietnam",
    "Taiwan", "Hong Kong", "Cambodia", "Myanmar", "Bangladesh"
}

SUBSCORE_CATS = ["cleanliness", "facilities", "location", "roomComfort", "staffPerformance", "valueForMoney"]

all_reviews, hotel_rows, sub_rows, profile_rows = [], [], [], []

for hotel in HOTELS:
    hid, city, hotel_name, tier = hotel["id"], hotel["city"], hotel["hotel_name"], hotel["tier"]
    print(f"Processing {hotel_name} ({city})...")

    df_a = pd.read_csv(f"{DATA_DIR}/{hid}_a.csv")   # Agoda-only reviews
    df_b = pd.read_csv(f"{DATA_DIR}/{hid}_b.csv")   # Booking.com-only reviews

    agoda_agg   = df_a["agodaAggregateReviewScore"].iloc[0]
    booking_agg = df_a["bookingAggregateReviewScore"].iloc[0]

    # ── review-level: Agoda rows ──
    a_clean = pd.DataFrame({
        "city": city, "hotel_name": hotel_name, "tier": tier, "hotel_id": hid,
        "platform": "Agoda",
        "score": pd.to_numeric(df_a["rating"], errors="coerce"),
        "nationality": df_a["reviewerCountryName"].fillna("Unknown"),
        "trip_type": df_a["reviewerGroupName"].fillna("Unknown"),
        "room_type": df_a["reviewerRoomTypeName"].fillna("Unknown"),
        "stay_nights": pd.to_numeric(df_a["reviewerLengthOfStay"], errors="coerce"),
        "source_file": f"{hid}_a",
        "agoda_agg_score": agoda_agg, "booking_agg_score": booking_agg,
    })

    # ── review-level: Booking.com rows (now with REAL nationality via userLocation) ──
    b_clean = pd.DataFrame({
        "city": city, "hotel_name": hotel_name, "tier": tier, "hotel_id": hid,
        "platform": "Booking.com",
        "score": pd.to_numeric(df_b["rating"], errors="coerce"),
        "nationality": df_b["userLocation"].fillna("Unknown"),
        "trip_type": df_b["travelerType"].fillna("Unknown"),
        "room_type": df_b["roomInfo"].fillna("Unknown") if "roomInfo" in df_b.columns else "Unknown",
        "stay_nights": pd.to_numeric(df_b["numberOfNights"], errors="coerce"),
        "source_file": f"{hid}_b",
        "agoda_agg_score": agoda_agg, "booking_agg_score": booking_agg,
    })

    all_reviews.append(a_clean)
    all_reviews.append(b_clean)

    # ── hotel_summary row ──
    a_score = pd.to_numeric(df_a["rating"], errors="coerce")
    b_score = pd.to_numeric(df_b["rating"], errors="coerce")
    all_nat = pd.concat([df_a["reviewerCountryName"], df_b["userLocation"]])
    known_nat = all_nat.dropna()

    hotel_rows.append({
        "hotel_id": hid, "hotel_name": hotel_name, "city": city, "tier": tier,
        "agoda_agg_score": agoda_agg, "booking_agg_score": booking_agg,
        "score_gap": round(agoda_agg - booking_agg, 2),
        "agoda_sample_avg": round(a_score.mean(), 2), "booking_sample_avg": round(b_score.mean(), 2),
        "agoda_sample_n": len(df_a), "booking_sample_n": len(df_b),
        "agoda_sample_std": round(a_score.std(), 2), "booking_sample_std": round(b_score.std(), 2),
        "pct_asian_reviewer": round(known_nat.isin(ASIAN_COUNTRIES).mean() * 100, 1) if len(known_nat) else None,
        "pct_nationality_known": round(len(known_nat) / len(all_nat) * 100, 1),
        "agoda_review_count": df_a["agodaReviewsCount"].iloc[0],
        "booking_review_count": df_a["bookingReviewsCount"].iloc[0],
    })

    # ── sub_scores rows (from Agoda file, which carries both platforms' aggregate sub-scores) ──
    row0 = df_a.iloc[0]
    for i, cat in enumerate(SUBSCORE_CATS):
        ags = row0.get(f"agodaAggregateDetailedReviewScore/{i}/score")
        bks = row0.get(f"bookingAggregateDetailedReviewScore/{i}/score")
        sub_rows.append({
            "hotel_id": hid, "city": city, "hotel_name": hotel_name, "category": cat,
            "agoda_score": ags, "booking_score": bks,
            "gap": round(float(ags) - float(bks), 2) if pd.notna(ags) and pd.notna(bks) else None,
        })

    # ── reviewer_profile rows ──
    profile_rows.append({
        "hotel_id": hid, "city": city, "platform": "Agoda", "n_reviews": len(df_a),
        "avg_score": round(a_score.mean(), 2),
        "pct_asian": round(df_a["reviewerCountryName"].dropna().isin(ASIAN_COUNTRIES).mean() * 100, 1) if df_a["reviewerCountryName"].notna().any() else None,
        "pct_nationality_known": round(df_a["reviewerCountryName"].notna().mean() * 100, 1),
        "pct_couple": round(df_a["reviewerGroupName"].str.lower().str.contains("couple", na=False).mean() * 100, 1),
        "pct_solo": round(df_a["reviewerGroupName"].str.lower().str.contains("solo", na=False).mean() * 100, 1),
        "pct_family": round(df_a["reviewerGroupName"].str.lower().str.contains("family", na=False).mean() * 100, 1),
        "pct_business": round(df_a["reviewerGroupName"].str.lower().str.contains("business", na=False).mean() * 100, 1),
        "avg_stay_nights": round(pd.to_numeric(df_a["reviewerLengthOfStay"], errors="coerce").mean(), 1),
        "score_std": round(a_score.std(), 2),
    })
    profile_rows.append({
        "hotel_id": hid, "city": city, "platform": "Booking.com", "n_reviews": len(df_b),
        "avg_score": round(b_score.mean(), 2),
        "pct_asian": round(df_b["userLocation"].dropna().isin(ASIAN_COUNTRIES).mean() * 100, 1) if df_b["userLocation"].notna().any() else None,
        "pct_nationality_known": round(df_b["userLocation"].notna().mean() * 100, 1),
        "pct_couple": round(df_b["travelerType"].str.lower().str.contains("couple", na=False).mean() * 100, 1),
        "pct_solo": round(df_b["travelerType"].str.lower().str.contains("solo", na=False).mean() * 100, 1),
        "pct_family": round(df_b["travelerType"].str.lower().str.contains("family", na=False).mean() * 100, 1),
        "pct_business": round(df_b["travelerType"].str.lower().str.contains("business", na=False).mean() * 100, 1),
        "avg_stay_nights": round(pd.to_numeric(df_b["numberOfNights"], errors="coerce").mean(), 1),
        "score_std": round(b_score.std(), 2),
    })

# ── finalize reviews_clean ──
reviews = pd.concat(all_reviews, ignore_index=True)
reviews["nationality_known"] = (reviews["nationality"] != "Unknown").astype(int)
reviews["is_asian_reviewer"] = np.where(
    reviews["nationality_known"] == 1,
    reviews["nationality"].isin(ASIAN_COUNTRIES).astype(int),
    np.nan
)
reviews["is_solo"] = reviews["trip_type"].str.lower().str.contains("solo", na=False).astype(int)
reviews["score_gap"] = reviews["agoda_agg_score"] - reviews["booking_agg_score"]
reviews.to_csv(f"{OUT_DIR}/reviews_clean.csv", index=False)

hotel_summary = pd.DataFrame(hotel_rows)
hotel_summary.to_csv(f"{OUT_DIR}/hotel_summary.csv", index=False)

sub_scores = pd.DataFrame(sub_rows)
sub_scores.to_csv(f"{OUT_DIR}/sub_scores.csv", index=False)

reviewer_profile = pd.DataFrame(profile_rows)
reviewer_profile.to_csv(f"{OUT_DIR}/reviewer_profile.csv", index=False)

print(f"\nTotal reviews: {len(reviews)}")
print(f"Nationality known: {reviews['nationality_known'].sum()} / {len(reviews)} ({reviews['nationality_known'].mean()*100:.1f}%)")
print("\n=== HOTEL SUMMARY ===")
print(hotel_summary[["hotel_name","city","agoda_agg_score","booking_agg_score","score_gap"]].to_string(index=False))
print("\nDone.")
