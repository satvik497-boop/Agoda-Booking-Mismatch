%let path = /home/u64532522/sasuser.v94;  /* <-- your real path from Properties */

/* ── IMPORTING FILES ── */
proc import datafile="&path/hotel_summary.csv"
    out=hotel_summary dbms=csv replace; getnames=yes; run;
proc import datafile="&path/reviews_clean.csv"
    out=reviews dbms=csv replace; getnames=yes; run;
proc import datafile="&path/sub_scores.csv"
    out=sub_scores dbms=csv replace; getnames=yes; run;
proc import datafile="&path/reviewer_profile.csv"
    out=reviewer_profile dbms=csv replace; getnames=yes; run;

/* ── BASELINE: Confirm the gap is real (N=10 now) ── */
proc means data=hotel_summary mean std min max;
    var agoda_agg_score booking_agg_score score_gap;
    title "Baseline: Agoda vs Booking Aggregate Scores (N=10 hotels)";
run;

/* ── PAIRED T-TEST ── */
proc ttest data=hotel_summary;
    paired agoda_agg_score * booking_agg_score;
    title "Paired T-Test: Agoda vs Booking Score Gap (N=10, DF=9)";
run;

/* ── SUB-SCORE GAPS ── */
proc means data=sub_scores mean;
    class category;
    var gap;
    title "Sub-Score Gaps by Category (Agoda minus Booking), averaged across 10 hotels";
run;

/* ── PREPARE REVIEW-LEVEL DATA ── */
data reviews_prep;
    set reviews;
    platform_agoda = (platform = "Agoda");
    if nationality_known = 1 then asian_reviewer = is_asian_reviewer;
    solo_traveler = (is_solo = 1);
    if score = . then delete;
run;

/* ── H1 Model 1a: naive platform effect (no hotel control) ── */
proc reg data=reviews_prep;
    model score = platform_agoda;
    title "H1 Model 1a: Raw platform effect on score (naive)";
run;

/* ── H1 Model 1b: platform effect with hotel fixed effects ──
   With 10 hotels we now have 9 dummy variables instead of 2 -- this is
   the same fixed-effects logic as before, just scaled up. */
proc glm data=reviews_prep;
    class hotel_id;
    model score = platform_agoda hotel_id / solution;
    title "H1 Model 1b: Platform effect controlling for hotel fixed effects";
run;
quit;

/* ── H1 Model 2: NOW CROSS-PLATFORM TESTABLE -- nationality is real on
   both platforms in this dataset (Booking.com's userLocation field
   worked, unlike the previous scrape). This directly tests sampling
   bias as originally intended, no longer restricted to Agoda-only. ── */
proc glm data=reviews_prep;
    where nationality_known = 1;
    class hotel_id;
    model score = asian_reviewer platform_agoda hotel_id / solution;
    title "H1 Model 2: Nationality effect controlling for platform + hotel FE (cross-platform)";
run;
quit;

/* ── H1: REVIEWER MIX COMPARISON ── */
proc means data=reviewer_profile mean;
    class platform;
    var pct_asian pct_solo pct_couple pct_business avg_score pct_nationality_known;
    title "H1: Reviewer Profile by Platform (N=10 hotels)";
run;

/* ── H2: VARIANCE TEST ── */
proc ttest data=reviews_prep;
    class platform_agoda;
    var score;
    title "H2: Score Variance Comparison (Agoda vs Booking), N=10 hotels";
run;

proc means data=reviews_prep mean std var min max;
    class platform;
    var score;
    title "H2: Score Distribution Statistics by Platform";
run;

/* ── RISK SEGMENTATION (10 hotels) ── */
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
    title "BA: Hotel Risk Segmentation + Revenue at Risk (N=10)";
run;

proc means data=hotel_risk sum mean;
    class risk_tier;
    var annual_revenue_at_risk;
    title "BA: Total Annual Revenue at Risk by Tier";
run;
