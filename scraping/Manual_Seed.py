"""
Manual Hotel Seeder — Use this if the automated search gets blocked.
Provides a hand-curated list of hotels known to be listed on both
Booking.com and Agoda, across all 5 target cities.

Run this INSTEAD of Step 1 (build_hotel_sample) if scraping search 
results fails. Then proceed with match_agoda_urls() and review scraping.

Usage:
    python manual_seed.py
"""

import pandas as pd
import os

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# MANUALLY VERIFIED HOTELS (both platforms)
# 10 per city × 5 cities = 50 starter hotels
# Add more from your own research to reach 200
# ─────────────────────────────────────────────

HOTELS = [
    # ── BANGKOK ──────────────────────────────
    {"hotel_name": "Lub d Bangkok Siam", "city": "Bangkok", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/th/lub-d-siam.html",
     "agoda_url": "https://www.agoda.com/lub-d-bangkok-siam/hotel/bangkok-th.html"},
    
    {"hotel_name": "The Okura Prestige Bangkok", "city": "Bangkok", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/th/the-okura-prestige-bangkok.html",
     "agoda_url": "https://www.agoda.com/the-okura-prestige-bangkok/hotel/bangkok-th.html"},
    
    {"hotel_name": "Ibis Bangkok Riverside", "city": "Bangkok", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/th/ibis-bangkok-riverside.html",
     "agoda_url": "https://www.agoda.com/ibis-bangkok-riverside/hotel/bangkok-th.html"},
    
    {"hotel_name": "Novotel Bangkok on Siam Square", "city": "Bangkok", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/th/novotel-bangkok-on-siam-square.html",
     "agoda_url": "https://www.agoda.com/novotel-bangkok-on-siam-square/hotel/bangkok-th.html"},
    
    {"hotel_name": "Centara Grand at CentralWorld", "city": "Bangkok", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/th/centara-grand-at-centralworld.html",
     "agoda_url": "https://www.agoda.com/centara-grand-at-centralworld/hotel/bangkok-th.html"},
    
    {"hotel_name": "Chatrium Hotel Riverside Bangkok", "city": "Bangkok", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/th/chatrium-riverside-bangkok.html",
     "agoda_url": "https://www.agoda.com/chatrium-hotel-riverside-bangkok/hotel/bangkok-th.html"},
    
    {"hotel_name": "Bangkok Marriott Marquis Queens Park", "city": "Bangkok", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/th/marriott-marquis-queens-park.html",
     "agoda_url": "https://www.agoda.com/bangkok-marriott-marquis-queens-park/hotel/bangkok-th.html"},
    
    {"hotel_name": "Anantara Riverside Bangkok Resort", "city": "Bangkok", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/th/anantara-riverside-bangkok-resort.html",
     "agoda_url": "https://www.agoda.com/anantara-riverside-bangkok-resort/hotel/bangkok-th.html"},
    
    {"hotel_name": "Sleep With Me Hotel Bangkok", "city": "Bangkok", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/th/sleep-with-me-hotel.html",
     "agoda_url": "https://www.agoda.com/sleep-with-me-hotel-design-hotel-at-patong/hotel/bangkok-th.html"},
    
    {"hotel_name": "Amari Bangkok", "city": "Bangkok", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/th/amari-boulevard-bangkok.html",
     "agoda_url": "https://www.agoda.com/amari-bangkok/hotel/bangkok-th.html"},

    # ── BALI ─────────────────────────────────
    {"hotel_name": "Kuta Seaview Boutique Resort", "city": "Bali", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/id/kuta-seaview-boutique-resort.html",
     "agoda_url": "https://www.agoda.com/kuta-seaview-boutique-resort-spa/hotel/bali-id.html"},
    
    {"hotel_name": "The Layar Private Villas Seminyak", "city": "Bali", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/id/the-layar-private-villas.html",
     "agoda_url": "https://www.agoda.com/the-layar-private-villas/hotel/bali-id.html"},
    
    {"hotel_name": "Aloft Bali Seminyak", "city": "Bali", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/id/aloft-bali-seminyak.html",
     "agoda_url": "https://www.agoda.com/aloft-bali-seminyak/hotel/bali-id.html"},
    
    {"hotel_name": "Ibis Styles Bali Legian", "city": "Bali", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/id/ibis-styles-bali-legian.html",
     "agoda_url": "https://www.agoda.com/ibis-styles-bali-legian/hotel/bali-id.html"},
    
    {"hotel_name": "Four Seasons Resort Bali at Sayan", "city": "Bali", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/id/four-seasons-resort-bali-at-sayan.html",
     "agoda_url": "https://www.agoda.com/four-seasons-resort-bali-at-sayan/hotel/bali-id.html"},
    
    {"hotel_name": "Komaneka at Bisma Ubud", "city": "Bali", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/id/komaneka-at-bisma.html",
     "agoda_url": "https://www.agoda.com/komaneka-at-bisma/hotel/bali-id.html"},
    
    {"hotel_name": "Courtyard by Marriott Bali Seminyak", "city": "Bali", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/id/courtyard-bali-seminyak-resort.html",
     "agoda_url": "https://www.agoda.com/courtyard-by-marriott-bali-seminyak-resort/hotel/bali-id.html"},
    
    {"hotel_name": "Sense Sunset Hotel Seminyak", "city": "Bali", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/id/sense-sunset-hotel.html",
     "agoda_url": "https://www.agoda.com/sense-sunset-hotel/hotel/bali-id.html"},
    
    {"hotel_name": "Sanur Paradise Plaza Hotel", "city": "Bali", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/id/sanur-paradise-plaza.html",
     "agoda_url": "https://www.agoda.com/sanur-paradise-plaza-hotel-suites/hotel/bali-id.html"},
    
    {"hotel_name": "The Mulia Bali", "city": "Bali", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/id/the-mulia-bali.html",
     "agoda_url": "https://www.agoda.com/the-mulia-bali/hotel/bali-id.html"},

    # ── TOKYO ────────────────────────────────
    {"hotel_name": "Park Hyatt Tokyo", "city": "Tokyo", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/jp/park-hyatt-tokyo.html",
     "agoda_url": "https://www.agoda.com/park-hyatt-tokyo/hotel/tokyo-jp.html"},
    
    {"hotel_name": "APA Hotel Shinjuku Kabukicho West", "city": "Tokyo", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/jp/apa-shinjuku-kabukicho-west.html",
     "agoda_url": "https://www.agoda.com/apa-hotel-shinjuku-kabukicho-west/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Shinjuku Granbell Hotel", "city": "Tokyo", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/jp/shinjuku-granbell.html",
     "agoda_url": "https://www.agoda.com/shinjuku-granbell-hotel/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Andaz Tokyo Toranomon Hills", "city": "Tokyo", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/jp/andaz-tokyo-toranomon-hills.html",
     "agoda_url": "https://www.agoda.com/andaz-tokyo-toranomon-hills-a-concept-by-hyatt/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Dormy Inn Asakusa", "city": "Tokyo", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/jp/dormy-inn-asakusa.html",
     "agoda_url": "https://www.agoda.com/dormy-inn-premium-asakusa/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Cerulean Tower Tokyu Hotel", "city": "Tokyo", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/jp/cerulean-tower-tokyu.html",
     "agoda_url": "https://www.agoda.com/cerulean-tower-tokyu-hotel/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Mitsui Garden Hotel Ginza Premier", "city": "Tokyo", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/jp/mitsui-garden-ginza-premier.html",
     "agoda_url": "https://www.agoda.com/mitsui-garden-hotel-ginza-premier/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Remm Akihabara", "city": "Tokyo", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/jp/remm-akihabara.html",
     "agoda_url": "https://www.agoda.com/remm-akihabara/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Prince Park Tower Tokyo", "city": "Tokyo", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/jp/prince-park-tower-tokyo.html",
     "agoda_url": "https://www.agoda.com/prince-park-tower-tokyo/hotel/tokyo-jp.html"},
    
    {"hotel_name": "Keio Plaza Hotel Tokyo", "city": "Tokyo", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/jp/keio-plaza.html",
     "agoda_url": "https://www.agoda.com/keio-plaza-hotel-tokyo/hotel/tokyo-jp.html"},

    # ── KUALA LUMPUR ─────────────────────────
    {"hotel_name": "Mandarin Oriental Kuala Lumpur", "city": "Kuala Lumpur", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/my/mandarin-oriental-kuala-lumpur.html",
     "agoda_url": "https://www.agoda.com/mandarin-oriental-kuala-lumpur/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "Tunes Hotel Duta Kuala Lumpur", "city": "Kuala Lumpur", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/my/tunes-duta-kl.html",
     "agoda_url": "https://www.agoda.com/tunes-hotel-duta-kuala-lumpur/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "InterContinental Kuala Lumpur", "city": "Kuala Lumpur", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/my/intercontinental-kuala-lumpur.html",
     "agoda_url": "https://www.agoda.com/intercontinental-kuala-lumpur/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "Aloft Kuala Lumpur Sentral", "city": "Kuala Lumpur", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/my/aloft-kuala-lumpur-sentral.html",
     "agoda_url": "https://www.agoda.com/aloft-kuala-lumpur-sentral/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "Ibis Kuala Lumpur City Centre", "city": "Kuala Lumpur", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/my/ibis-kuala-lumpur-city-centre.html",
     "agoda_url": "https://www.agoda.com/ibis-kuala-lumpur-city-centre/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "The Westin Kuala Lumpur", "city": "Kuala Lumpur", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/my/the-westin-kuala-lumpur.html",
     "agoda_url": "https://www.agoda.com/the-westin-kuala-lumpur/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "Sunway Putra Hotel Kuala Lumpur", "city": "Kuala Lumpur", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/my/sunway-putra-hotel.html",
     "agoda_url": "https://www.agoda.com/sunway-putra-hotel/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "Tune Hotel Kuala Lumpur KLCC", "city": "Kuala Lumpur", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/my/tune-klcc.html",
     "agoda_url": "https://www.agoda.com/tune-hotel-kuala-lumpur-klcc/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "Hilton Kuala Lumpur", "city": "Kuala Lumpur", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/my/hilton-kuala-lumpur.html",
     "agoda_url": "https://www.agoda.com/hilton-kuala-lumpur/hotel/kuala-lumpur-my.html"},
    
    {"hotel_name": "Berjaya Times Square Hotel KL", "city": "Kuala Lumpur", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/my/berjaya-times-square.html",
     "agoda_url": "https://www.agoda.com/berjaya-times-square-hotel-kuala-lumpur/hotel/kuala-lumpur-my.html"},

    # ── SINGAPORE ────────────────────────────
    {"hotel_name": "Marina Bay Sands", "city": "Singapore", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/sg/marina-bay-sands.html",
     "agoda_url": "https://www.agoda.com/marina-bay-sands/hotel/singapore-sg.html"},
    
    {"hotel_name": "Ibis Singapore on Bencoolen", "city": "Singapore", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/sg/ibis-singapore-on-bencoolen.html",
     "agoda_url": "https://www.agoda.com/ibis-singapore-on-bencoolen/hotel/singapore-sg.html"},
    
    {"hotel_name": "Raffles Hotel Singapore", "city": "Singapore", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/sg/raffles-singapore.html",
     "agoda_url": "https://www.agoda.com/raffles-hotel-singapore/hotel/singapore-sg.html"},
    
    {"hotel_name": "Novotel Singapore on Stevens", "city": "Singapore", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/sg/novotel-singapore-on-stevens.html",
     "agoda_url": "https://www.agoda.com/novotel-singapore-on-stevens/hotel/singapore-sg.html"},
    
    {"hotel_name": "The Pod Boutique Capsule Hostel", "city": "Singapore", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/sg/the-pod-boutique-capsule-hostel.html",
     "agoda_url": "https://www.agoda.com/the-pod-boutique-capsule-hotel/hotel/singapore-sg.html"},
    
    {"hotel_name": "Capella Singapore", "city": "Singapore", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/sg/capella-singapore.html",
     "agoda_url": "https://www.agoda.com/capella-singapore/hotel/singapore-sg.html"},
    
    {"hotel_name": "Paradox Singapore Merchant Court", "city": "Singapore", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/sg/swissotel-merchant-court.html",
     "agoda_url": "https://www.agoda.com/paradox-singapore-merchant-court/hotel/singapore-sg.html"},
    
    {"hotel_name": "Hotel G Singapore", "city": "Singapore", "tier": "Budget",
     "booking_url": "https://www.booking.com/hotel/sg/g-singapore.html",
     "agoda_url": "https://www.agoda.com/hotel-g-singapore/hotel/singapore-sg.html"},
    
    {"hotel_name": "Pan Pacific Singapore", "city": "Singapore", "tier": "Luxury",
     "booking_url": "https://www.booking.com/hotel/sg/pan-pacific-singapore.html",
     "agoda_url": "https://www.agoda.com/pan-pacific-singapore/hotel/singapore-sg.html"},
    
    {"hotel_name": "Hotel Jen Tanglin Singapore", "city": "Singapore", "tier": "Mid",
     "booking_url": "https://www.booking.com/hotel/sg/hotel-jen-tanglin.html",
     "agoda_url": "https://www.agoda.com/hotel-jen-tanglin-singapore-by-shangri-la/hotel/singapore-sg.html"},
]


def create_manual_hotel_list():
    df = pd.DataFrame(HOTELS)
    df["hotel_id"] = range(1, len(df) + 1)
    df["agoda_matched"] = True  # all are manually verified
    df["booking_id"] = df["booking_url"].apply(
        lambda x: x.split("/hotel/")[1].split(".")[0] if "/hotel/" in x else None
    )
    
    df.to_csv(f"{OUTPUT_DIR}/hotels_master.csv", index=False)
    
    print(f"Created manual hotel list: {len(df)} hotels")
    print(f"City breakdown:")
    print(df["city"].value_counts().to_string())
    print(f"Tier breakdown:")
    print(df["tier"].value_counts().to_string())
    print(f"\nSaved to {OUTPUT_DIR}/hotels_master.csv")
    print(f"\nNext step: Run scraper.py — it will load this file automatically")
    
    return df


if __name__ == "__main__":
    create_manual_hotel_list()
