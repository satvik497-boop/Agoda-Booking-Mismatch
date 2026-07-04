%let path = /home/u64532522/sasuser.v94;  /* <-- REPLACE with your real path from Properties */

/* ── IMPORTING FILES ── */
proc import datafile="&path/hotel_summary.csv"
    out=hotel_summary dbms=csv replace; getnames=yes; run;
proc import datafile="&path/reviews_for_sas.csv"
    out=reviews dbms=csv replace; getnames=yes; run;
proc import datafile="&path/sub_scores.csv"
    out=sub_scores dbms=csv replace; getnames=yes; run;
proc import datafile="&path/reviewer_profile.csv"
    out=reviewer_profile dbms=csv replace; getnames=yes; run;

/* ── BASELINE: Confirm the gap is real ── */
proc means data=hotel_summary mean std min max;
    var agoda_agg_score booking_agg_score score_gap;
    title "Baseline: Agoda vs Booking Aggregate Scores";
run;

/* ── PAIRED T-TEST: Is the gap statistically significant? ── */
proc ttest data=hotel_summary;
    paired agoda_agg_score * booking_agg_score;
    title "Paired T-Test: Agoda vs Booking Score Gap";
run;

/* ── SUB-SCORE GAPS: Which category drives the gap most? ── */
proc means data=sub_scores mean;
    class category;
    var gap;
    title "Sub-Score Gaps by Category (Agoda minus Booking)";
run;

/* ── PREPARE REVIEW-LEVEL DATA FOR REGRESSION ── */
data reviews_prep;
    set reviews;
    platform_agoda = (platform = "Agoda");
    if nationality_known = 1 then asian_reviewer = is_asian_reviewer;
    /* else leave asian_reviewer missing (.) -- do not code as 0 */
    solo_traveler  = (is_solo = 1);
    city_bali      = (city = "Bali");
    city_singapore = (city = "Singapore");
    if score = . then delete;
run;

/* ── H1: REGRESSION — Does sampling bias explain the gap? ── */
proc reg data=reviews_prep;
    model score = platform_agoda;
    title "H1 Model 1: Raw platform effect on score";
run;

/* NOTE: A "platform effect controlling for reviewer nationality" model is
   NOT estimable — nationality is 0% known on Booking.com, so the nationality
   covariate has zero variance on one side of platform_agoda (perfect
   confounding). H1 cannot be tested as a platform comparison with this data.
   Instead, we test nationality's effect on score WITHIN Agoda only, where
   nationality is actually known, as a secondary/exploratory check. */
proc reg data=reviews_prep;
    where platform = "Agoda" and nationality_known = 1;
    model score = asian_reviewer solo_traveler city_bali city_singapore;
    title "H1 (exploratory, Agoda-only): Does reviewer nationality predict score within Agoda?";
run;

/* ── H1: REVIEWER MIX COMPARISON ── */
proc means data=reviewer_profile mean;
    class platform;
    var pct_asian pct_solo pct_couple pct_business avg_score;
    title "H1: Reviewer Profile by Platform";
run;

/* ── H2: VARIANCE TEST ── */
proc ttest data=reviews_prep;
    class platform_agoda;
    var score;
    title "H2: Score Variance Comparison (Agoda vs Booking)";
run;

proc means data=reviews_prep mean std var min max;
    class platform;
    var score;
    title "H2: Score Distribution Statistics by Platform";
run;

/* ── RISK SEGMENTATION ── */
data hotel_risk;
    set hotel_summary;
    if score_gap <= -0.4 then risk_tier = "At-Risk";
    else if score_gap <= -0.2 then risk_tier = "Watch";
    else risk_tier = "Safe";

    avg_monthly_bookings = 120;
    avg_booking_value    = 80;
    commission_rate      = 0.15;
    allocation_reduction = 0.20;

    monthly_revenue_at_risk = avg_monthly_bookings * avg_booking_value
                              * commission_rate * allocation_reduction;
    annual_revenue_at_risk  = monthly_revenue_at_risk * 12;
run;

proc print data=hotel_risk;
    var hotel_name city score_gap risk_tier annual_revenue_at_risk;
    title "BA: Hotel Risk Segmentation + Revenue at Risk";
run;

proc means data=hotel_risk sum mean;
    var annual_revenue_at_risk;
    title "BA: Total Annual Revenue at Risk";
run;
