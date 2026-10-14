"""
generate_cascade_goods.py  (v2)
===============================
Seeded synthetic-data generator for *The Agent-Augmented Data Scientist*.

Tier 1 = four tables: customers, products, orders, order_items.
Deterministic under SEED. Foreign keys resolve by construction. Order totals
reconcile with line items. Two interventions are planted with known effect sizes.
Test signals and dirty data are layered, not obvious. Every planted issue is
logged to known_plants.csv for the author, never labelled in the data.

v2 changes (from multi-AI stress tests):
  - Orders are always placed on or after the customer's signup_date.
  - signup_date spread back to 2022 so most customers are established.
  - account_status is derived from order recency (no "zombie" dormant buyers).
  - customer_segment loosely tracks behaviour but stays definition-ambiguous.
  - Geography keyed state -> city -> zip (consistent), with a small controlled
    city/state mismatch plant instead of pervasive nonsense.
  - Product weight is category-appropriate; shipping_class derives from weight;
    product-name size suffixes are category-appropriate.
  - The Mountain regional effect is a clean, evenly-spread, larger step that a
    synthetic control recovers, validated against donor regions (not raw before/after).
  - order_status reworked: ~93% Completed plus small Cancelled/Pending tails;
    Cancelled/Pending collect nothing; refunds live on Completed orders.
  - Refund header-vs-line gap is a bounded ~15% subset, not universal.
  - shipping_speed affects the late rate; num_items never reads 0; the free-ship
    threshold is realistic (bulky items can still incur shipping above it).
  - total_collected renamed gross_collected (gross cash at purchase, pre-refund).
  - age_band sentinel is "Unknown" (survives CSV; "N/A" auto-parses to null).

Run:  python data_generation/generate_cascade_goods.py
Out:  data_generation/generated/ (independent of working directory)
        customers.csv, products.csv, orders.csv, order_items.csv,
      data_dictionary.csv, known_plants.csv
"""

import os
import random
from pathlib import Path
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# KNOBS                                                                        #
# --------------------------------------------------------------------------- #
SEED            = 42
OUTPUT_DIR      = str(Path(__file__).resolve().parent / "generated")

N_CUSTOMERS     = 2000
N_PRODUCTS      = 150
N_ORDERS        = 9000          # ~4-5 orders/customer, realistic for electronics retail

DATE_START      = date(2024, 1, 1)   # observation window for orders
DATE_END        = date(2025, 12, 31)
SIGNUP_START    = date(2022, 1, 1)   # customers can have signed up before the window
SNAPSHOT_DATE   = date(2025, 12, 31)
CHURN_WINDOW    = 90

# Intervention 1: free-shipping threshold lowered 50 -> 35 on this date
THRESHOLD_DATE      = date(2025, 6, 15)
THRESHOLD_BEFORE    = 50.0
THRESHOLD_AFTER     = 35.0

# Intervention 2: Mountain region gets free 2-day shipping on this date
REGIONAL_DATE       = date(2025, 8, 1)
REGIONAL_REGION     = "Mountain"
REGIONAL_LIFT       = 0.18      # clean post-period order lift, recovered by synthetic control

# Plant / realism rates
TEST_ACCOUNT_RATE   = 0.015
TEST_FLAG_COVERAGE  = 0.60
DIRTY_STATE_RATE    = 0.02      # lowercase state strings
DIRTY_AGE_RATE      = 0.015     # age_band = "Unknown"
GEO_MISMATCH_RATE   = 0.015     # controlled city/state mismatch
N_DUPLICATE_PAIRS   = 2
NUM_ITEMS_MISMATCH  = 0.01
ORDER_DISCOUNT_RATE = 0.15
REFUND_MISMATCH_RATE = 0.15     # share of refunded orders where header != line sum
SINGLE_ITEM_SHARE   = 0.60      # basket size target
RETURN_CENSOR_DAYS  = 21        # orders newer than this (vs snapshot) cannot be returned yet
FREE_SHIP_EXCEPTION_RATE = 0.12 # above-threshold orders that still pay (excluded/bulky items)

rng = np.random.default_rng(SEED)
random.seed(SEED)
np.random.seed(SEED)

# --------------------------------------------------------------------------- #
# REFERENCE DATA                                                               #
# --------------------------------------------------------------------------- #
REGION_STATES = {
    "Pacific NW":   ["WA", "OR"],
    "California":   ["CA"],
    "Southwest":    ["AZ", "NM", "NV"],
    "Mountain":     ["CO", "UT", "ID", "MT", "WY"],
    "Midwest":      ["MO", "KS", "NE", "IA"],
    "Great Lakes":  ["IL", "MI", "OH", "IN", "WI"],
    "Northeast":    ["NY", "MA", "CT", "NJ"],
    "Mid-Atlantic": ["MD", "VA", "DC", "DE", "PA"],
    "Southeast":    ["FL", "GA", "NC", "SC", "TN"],
    "South Central":["TX", "OK", "AR", "LA"],
}
REGIONS = list(REGION_STATES.keys())
STATE_REGION = {s: r for r, sts in REGION_STATES.items() for s in sts}

# state -> representative cities (real)
STATE_CITY = {
    "WA": ["Seattle", "Spokane", "Tacoma"], "OR": ["Portland", "Eugene", "Salem"],
    "CA": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
    "AZ": ["Phoenix", "Tucson", "Mesa"], "NM": ["Albuquerque", "Santa Fe", "Las Cruces"],
    "NV": ["Las Vegas", "Reno", "Henderson"], "CO": ["Denver", "Colorado Springs", "Boulder"],
    "UT": ["Salt Lake City", "Provo", "Ogden"], "ID": ["Boise", "Nampa", "Idaho Falls"],
    "MT": ["Billings", "Bozeman", "Missoula"], "WY": ["Cheyenne", "Casper", "Laramie"],
    "MO": ["Kansas City", "St. Louis", "Springfield"], "KS": ["Wichita", "Overland Park", "Topeka"],
    "NE": ["Omaha", "Lincoln", "Bellevue"], "IA": ["Des Moines", "Cedar Rapids", "Davenport"],
    "IL": ["Chicago", "Aurora", "Naperville"], "MI": ["Detroit", "Grand Rapids", "Ann Arbor"],
    "OH": ["Columbus", "Cleveland", "Cincinnati"], "IN": ["Indianapolis", "Fort Wayne", "Bloomington"],
    "WI": ["Milwaukee", "Madison", "Green Bay"], "NY": ["New York", "Buffalo", "Rochester"],
    "MA": ["Boston", "Worcester", "Cambridge"], "CT": ["Hartford", "New Haven", "Stamford"],
    "NJ": ["Newark", "Jersey City", "Trenton"], "MD": ["Baltimore", "Rockville", "Annapolis"],
    "VA": ["Richmond", "Virginia Beach", "Arlington"], "DC": ["Washington"],
    "DE": ["Wilmington", "Dover", "Middletown"], "PA": ["Philadelphia", "Pittsburgh", "Allentown"],
    "FL": ["Miami", "Orlando", "Tampa"], "GA": ["Atlanta", "Savannah", "Augusta"],
    "NC": ["Charlotte", "Raleigh", "Durham"], "SC": ["Charleston", "Columbia", "Greenville"],
    "TN": ["Nashville", "Memphis", "Knoxville"], "TX": ["Austin", "Dallas", "Houston", "San Antonio"],
    "OK": ["Oklahoma City", "Tulsa", "Norman"], "AR": ["Little Rock", "Fayetteville", "Fort Smith"],
    "LA": ["New Orleans", "Baton Rouge", "Shreveport"],
}
# state -> leading 2 zip digits (realistic, distinct enough)
STATE_ZIP = {
    "WA": 98, "OR": 97, "CA": 90, "AZ": 85, "NM": 87, "NV": 89, "CO": 80, "UT": 84,
    "ID": 83, "MT": 59, "WY": 82, "MO": 63, "KS": 66, "NE": 68, "IA": 50, "IL": 60,
    "MI": 48, "OH": 44, "IN": 46, "WI": 53, "NY": 10, "MA": 2, "CT": 6, "NJ": 7,
    "MD": 21, "VA": 23, "DC": 20, "DE": 19, "PA": 15, "FL": 33, "GA": 30, "NC": 28,
    "SC": 29, "TN": 37, "TX": 75, "OK": 73, "AR": 72, "LA": 70,
}

# category -> (price_low, price_high, return_rate, subcategories)
CATEGORIES = {
    "Laptops":    (200, 3500, 0.12, ["Ultrabook", "Gaming Laptop", "2-in-1", "Budget"]),
    "Desktops":   (350, 3000, 0.08, ["Tower", "All-in-One", "Mini PC", "Gaming Rig"]),
    "Phones":     (120, 1700, 0.10, ["Flagship", "Mid-range", "Budget"]),
    "Tablets":    (100, 1300, 0.09, ["Standard", "Pro", "Kids"]),
    "TVs":        (150, 5000, 0.06, ["4K LED", "OLED", "QLED", "Budget HD"]),
    "Audio":      (20, 600,  0.07, ["Headphones", "Earbuds", "Soundbar", "Speaker"]),
    "Gaming":     (40, 700,  0.09, ["Console", "Controller", "Headset", "Accessory"]),
    "Smart Home": (25, 400,  0.07, ["Speaker", "Camera", "Thermostat", "Lighting", "Plug"]),
    "Wearables":  (50, 800,  0.10, ["Smartwatch", "Fitness Band", "Smart Ring"]),
    "Cameras":    (120, 4000, 0.08, ["Mirrorless", "Action", "Compact", "Lens"]),
    "Accessories":(8, 120,   0.03, ["Cable", "Case", "Charger", "Stand", "Adapter"]),
    "Networking": (30, 500,  0.05, ["Router", "Mesh", "Switch", "Extender"]),
}
# category -> (weight_low_kg, weight_high_kg)
CATEGORY_WEIGHT = {
    "Laptops": (1.1, 2.8), "Desktops": (5.0, 14.0), "Phones": (0.14, 0.24),
    "Tablets": (0.4, 0.8), "TVs": (6.0, 35.0), "Audio": (0.2, 4.0),
    "Gaming": (0.1, 4.5), "Smart Home": (0.1, 1.5), "Wearables": (0.03, 0.12),
    "Cameras": (0.3, 1.6), "Accessories": (0.05, 0.9), "Networking": (0.2, 1.6),
}
CATEGORY_WEIGHTS = {
    "Accessories": 0.22, "Audio": 0.15, "Smart Home": 0.12, "Gaming": 0.10,
    "Phones": 0.08, "Wearables": 0.07, "Networking": 0.06, "Tablets": 0.06,
    "Laptops": 0.05, "TVs": 0.04, "Cameras": 0.03, "Desktops": 0.02,
}
BRANDS = ["Vireo", "Kestrel", "Pinemark", "Halcyon", "Northpeak", "Lumen", "Cascade Basics"]
PRIVATE_LABEL = "Cascade Basics"
SERIES = ["Aero", "Pulse", "Core", "Edge", "Nova", "Flux", "Apex", "Drift", "Lyra", "Onyx"]

def shipping_class_from_weight(category, w):
    if category == "TVs":
        return "Oversized"          # dimensionally large regardless of weight
    if w < 1:    return "Small"
    if w < 5:    return "Standard"
    if w < 15:   return "Heavy"
    return "Oversized"

def name_size_suffix(category):
    if category == "TVs":       return rng.choice(['43"', '50"', '55"', '65"', '75"', '85"'])
    if category == "Laptops":   return rng.choice(['13"', '14"', '15"', '16"', '17"'])
    if category == "Tablets":   return rng.choice(['8"', '10"', '11"', '13"'])
    if category == "Phones":    return rng.choice(["128GB", "256GB", "512GB"])
    if category == "Wearables": return rng.choice(["41mm", "45mm", ""])
    if category == "Cameras":   return rng.choice(["24MP", "33MP", ""])
    if category == "Desktops":  return rng.choice(["16GB", "32GB", ""])
    return ""

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy", "Matthew", "Lisa",
               "Anthony", "Margaret", "Mark", "Betty", "Donald", "Sandra", "Steven", "Ashley",
               "Andrew", "Emily", "Joshua", "Kimberly", "Kevin", "Donna", "Brian", "Michelle",
               "Priya", "Wei", "Carlos", "Aisha", "Hiroshi", "Sofia", "Omar", "Ananya",
               "Olivia", "Liam", "Noah", "Emma", "Ava", "Isabella", "Mason", "Lucas", "Ethan",
               "Mia", "Amelia", "Harper", "Benjamin", "Henry", "Alexander", "Grace", "Chloe",
               "Nathan", "Zoe", "Diego", "Fatima", "Mei", "Raj", "Leila", "Tomas", "Yusuf", "Nadia"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
              "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
              "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen",
              "Hill", "Flores", "Patel", "Kim", "Chen", "Okafor", "Singh", "Rossi",
              "Hall", "Adams", "Nelson", "Baker", "Carter", "Mitchell", "Roberts", "Turner",
              "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart",
              "Morris", "Murphy", "Cook", "Rogers", "Reed", "Bailey", "Cooper", "Cox",
              "Howard", "Ward", "Peterson", "Gray", "Ramos", "Watson", "Brooks", "Bennett"]
NICKNAME = {"Robert": "Bob", "William": "Bill", "Richard": "Rick", "Margaret": "Peggy",
            "Elizabeth": "Liz", "James": "Jim", "Michael": "Mike", "Jennifer": "Jen",
            "Thomas": "Tom", "Joseph": "Joe", "Charles": "Charlie", "Daniel": "Dan"}

CONSUMER_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com", "hotmail.com", "proton.me"]
INTERNAL_DOMAINS = ["cascadegoods.com", "qa.cascadegoods.test"]
ACQ_CHANNELS = ["Organic Search", "Paid Search", "Social", "Email", "Referral", "Direct", "Affiliate"]
AGE_BANDS    = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
GENDERS      = ["Female", "Male", "Nonbinary", "Undisclosed"]
SEGMENTS     = ["New", "Returning", "Loyal", "VIP", "Dormant"]
DEVICES      = ["Desktop", "Mobile", "Tablet"]
PAYMENTS     = ["Credit Card", "Debit Card", "PayPal", "Gift Card", "BNPL"]
PROMO_CODES  = ["SAVE10", "FREESHIP", "LAUNCH20", "WELCOME15"]
SHIP_SPEEDS  = ["Standard", "Expedited", "Two-Day"]
ORDER_CHANNELS = ["Web", "Mobile App", "In-Store"]
RETURN_REASONS = ["Defective", "Wrong Item", "Not As Described", "Changed Mind",
                  "Better Price Found", "Arrived Late"]
# late rate by shipping speed (optional fix 8)
LATE_RATE = {"Standard": 0.18, "Expedited": 0.09, "Two-Day": 0.05}

PLANTS = []
def log_plant(pid, table, cols, desc, hint, chapter):
    PLANTS.append({"plant_id": pid, "table": table, "columns": cols,
                   "description": desc, "detection_hint": hint, "chapter": chapter})

# --------------------------------------------------------------------------- #
# DATE WEIGHTING (seasonality + payday bumps)                                  #
# --------------------------------------------------------------------------- #
ALL_DATES = pd.date_range(DATE_START, DATE_END, freq="D")

def _day_weight(d):
    w = 1.0
    if d.month in (11, 12): w *= 1.6
    if d.month in (6, 7, 8): w *= 0.85
    if d.day in (1, 2, 3, 14, 15, 16): w *= 1.15
    return w

DAY_WEIGHTS = np.array([_day_weight(d) for d in ALL_DATES])

def sample_date_after(start_d):
    """Sample one order date in [max(start_d, DATE_START), DATE_END] by seasonality."""
    i0 = max(0, (start_d - DATE_START).days)
    if i0 >= len(ALL_DATES):
        i0 = len(ALL_DATES) - 1
    w = DAY_WEIGHTS[i0:]
    w = w / w.sum()
    k = rng.choice(len(w), p=w)
    return ALL_DATES[i0 + k].date()

def make_zip(state):
    return f"{STATE_ZIP[state]:02d}{int(rng.integers(0, 1000)):03d}"

# --------------------------------------------------------------------------- #
# 1. PRODUCTS                                                                  #
# --------------------------------------------------------------------------- #
def build_products():
    cats = list(CATEGORIES.keys())
    cat_w = np.array([CATEGORY_WEIGHTS[c] for c in cats]); cat_w /= cat_w.sum()
    rows = []
    for i in range(N_PRODUCTS):
        sku = f"SKU-{10001 + i}"
        category = rng.choice(cats, p=cat_w)
        plo, phi, ret, subs = CATEGORIES[category]
        subcategory = rng.choice(subs)
        brand = rng.choice(BRANDS)
        is_pl = brand == PRIVATE_LABEL
        suffix = name_size_suffix(category)
        name = " ".join(x for x in [brand, rng.choice(SERIES), subcategory, suffix] if x)
        list_price = round(float(rng.uniform(plo, phi)), 2)
        cost_ratio = rng.uniform(0.40, 0.60) if is_pl else rng.uniform(0.55, 0.80)
        unit_cost = round(list_price * cost_ratio, 2)
        markdown = rng.choice([0, 0, 0, 0.05, 0.10, 0.15], p=[0.55, 0.15, 0.10, 0.10, 0.06, 0.04])
        current_price = round(list_price * (1 - markdown), 2)
        wlo, whi = CATEGORY_WEIGHT[category]
        weight = round(float(rng.uniform(wlo, whi)), 2)
        launch = SIGNUP_START + timedelta(days=int(rng.integers(0, (date(2023, 12, 31) - SIGNUP_START).days)))
        rows.append({
            "sku": sku, "product_name": name, "category": category, "subcategory": subcategory,
            "brand": brand, "is_private_label": is_pl, "unit_cost": unit_cost, "list_price": list_price,
            "current_price": current_price, "margin_pct": round((list_price - unit_cost) / list_price, 3),
            "launch_date": launch.isoformat(), "is_active": bool(rng.random() > 0.08),
            "weight_kg": weight, "shipping_class": shipping_class_from_weight(category, weight),
            "return_rate": round(float(ret * rng.uniform(0.7, 1.3)), 3),
        })
    log_plant("P1", "products / order_items", "list_price vs unit_list_price",
              "Line items store a price snapshot that can differ from the product's current price.",
              "Join order_items.sku to products and compare unit_list_price with list_price.", "Ch 4")
    return pd.DataFrame(rows)

# --------------------------------------------------------------------------- #
# 2. CUSTOMERS  (base attributes; status/segment derived later from behaviour) #
# --------------------------------------------------------------------------- #
def build_customers():
    rows = []
    n_test = int(N_CUSTOMERS * TEST_ACCOUNT_RATE)
    test_idx = set(rng.choice(N_CUSTOMERS, size=n_test, replace=False).tolist())
    est_days = (date(2023, 12, 31) - SIGNUP_START).days
    new_days = (date(2025, 10, 31) - DATE_START).days
    for i in range(N_CUSTOMERS):
        cid = f"C{i+1:06d}"
        region = rng.choice(REGIONS)
        state = rng.choice(REGION_STATES[region])
        city = rng.choice(STATE_CITY[state])
        zip_code = make_zip(state)
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        loyalty = bool(rng.random() < 0.25)
        # ~60% established (signed up 2022-2023), ~40% newer (within window)
        if rng.random() < 0.60:
            signup = SIGNUP_START + timedelta(days=int(rng.integers(0, est_days)))
        else:
            signup = DATE_START + timedelta(days=int(rng.integers(0, new_days)))
        is_test = i in test_idx
        if is_test:
            first = rng.choice([first, "Test", "QA"], p=[0.4, 0.4, 0.2])
            domain = rng.choice(INTERNAL_DOMAINS)
        else:
            domain = rng.choice(CONSUMER_DOMAINS)
        activity = rng.uniform(0.5, 1.5) * (1.6 if loyalty else 1.0)
        rows.append({
            "customer_id": cid, "first_name": first, "last_name": last, "email_domain": domain,
            "signup_date": signup.isoformat(), "acquisition_channel": rng.choice(ACQ_CHANNELS),
            "region": region, "state": state, "city": city, "zip_code": zip_code,
            "age_band": rng.choice(AGE_BANDS), "gender": rng.choice(GENDERS),
            "loyalty_member": loyalty, "marketing_opt_in": bool(rng.random() < 0.6),
            "preferred_device": rng.choice(DEVICES),
            "is_test_account": bool(is_test and rng.random() < TEST_FLAG_COVERAGE),
            "_activity": activity, "_is_test": is_test,
        })
    df = pd.DataFrame(rows)

    # planted near-duplicates: nickname + shared last/city/state/zip/email (resolvable)
    dup_sources = rng.choice(df.index[~df["_is_test"]], size=N_DUPLICATE_PAIRS, replace=False)
    dup_rows = []
    for j, src in enumerate(dup_sources):
        orig = df.loc[src].copy()
        dup = orig.copy()
        dup["customer_id"] = f"C{N_CUSTOMERS + j + 1:06d}"
        dup["first_name"] = NICKNAME.get(orig["first_name"], orig["first_name"][:3])
        dup["zip_code"] = orig["zip_code"]          # shared zip makes the true pair resolvable
        dup_rows.append(dup)
    if dup_rows:
        df = pd.concat([df, pd.DataFrame(dup_rows)], ignore_index=True)
        log_plant("C1", "customers", "first_name, last_name, city, zip_code, email_domain",
                  f"{N_DUPLICATE_PAIRS} near-duplicate customers (nickname, same last name/city/zip/email).",
                  "Fuzzy-match on last_name + zip_code + email_domain; first names differ by nickname.", "Ch 4")

    # controlled geo mismatch plant: city from a different state (Chicago, OH style)
    clean = df.index[(~df["_is_test"])]
    geo_idx = rng.choice(clean, size=max(1, int(len(df) * GEO_MISMATCH_RATE)), replace=False)
    for ix in geo_idx:
        wrong_state = rng.choice([s for s in STATE_CITY if s != df.at[ix, "state"]])
        df.at[ix, "city"] = rng.choice(STATE_CITY[wrong_state])
    log_plant("C7", "customers", "city, state, zip_code",
              f"~{GEO_MISMATCH_RATE*100:.1f}% of customers have a city that does not match their state/zip.",
              "Validate city against state with a zip-to-state lookup; a small share will fail.", "Ch 4")

    # lowercase state plant
    low_idx = rng.choice(df.index, size=int(len(df) * DIRTY_STATE_RATE), replace=False)
    df.loc[low_idx, "state"] = df.loc[low_idx, "state"].str.lower()
    log_plant("C2", "customers", "state", "A small share of state codes are lowercase ('ca' not 'CA').",
              "Check distinct state values for case inconsistency.", "Ch 4")

    # missing age plant (sentinel 'Unknown', survives CSV round-trip)
    age_idx = rng.choice(df.index, size=int(len(df) * DIRTY_AGE_RATE), replace=False)
    df.loc[age_idx, "age_band"] = "Unknown"
    log_plant("C3", "customers", "age_band", "Some age_band values are the sentinel string 'Unknown'.",
              "Treat 'Unknown' as missing; it will not behave like a numeric or ordered band.", "Ch 4")

    log_plant("C4", "customers", "is_test_account, email_domain, first_name",
              f"~{TEST_ACCOUNT_RATE*100:.1f}% are internal/test accounts but the flag catches only ~{int(TEST_FLAG_COVERAGE*100)}%.",
              "Combine the flag with internal email domains and first_name in (Test, QA).", "Ch 4")
    log_plant("C5", "customers", "customer_segment",
              "customer_segment loosely tracks behaviour but has no stated definition.",
              "Ask what 'Loyal' or 'VIP' means before using it in a metric.", "Ch 3")
    log_plant("C6", "customers", "loyalty_member",
              "Loyalty members are generated to be more active, so they churn less. Association, not cause.",
              "Comparing churn by loyalty invites a causal read the design does not support.", "Ch 5")
    return df

# --------------------------------------------------------------------------- #
# 3 + 4. ORDERS and ORDER_ITEMS                                                #
# --------------------------------------------------------------------------- #
def build_orders_and_items(customers, products):
    cust = customers[customers["_is_test"] == False].copy()
    signup = {r.customer_id: date.fromisoformat(r.signup_date) for r in cust.itertuples()}
    home = dict(zip(customers["customer_id"], customers["region"]))

    # weight customer choice by activity and tenure (longer tenure -> more orders)
    tenure = np.array([(DATE_END - signup[c]).days for c in cust["customer_id"]], dtype=float)
    w = cust["_activity"].to_numpy() * np.sqrt(np.clip(tenure, 30, None))
    w = w / w.sum()
    cust_ids = cust["customer_id"].to_numpy()

    # base order specs: (customer, date>=signup, ship_region)
    chosen = rng.choice(len(cust_ids), size=N_ORDERS, p=w)
    specs = []
    for k in chosen:
        c = cust_ids[k]
        d = sample_date_after(max(signup[c], DATE_START))
        sr = rng.choice([r for r in REGIONS if r != home[c]]) if rng.random() < 0.08 else home[c]
        specs.append((c, d, sr))

    # Mountain post-shock bonus: clean, evenly spread, ships to Mountain (synthetic-control signal)
    base_mtn_post = sum(1 for (_, d, sr) in specs if sr == REGIONAL_REGION and d >= REGIONAL_DATE)
    n_bonus = int(round(base_mtn_post * REGIONAL_LIFT))
    mtn_pool = [c for c in cust_ids if home[c] == REGIONAL_REGION]
    post_days = pd.date_range(REGIONAL_DATE, DATE_END, freq="D")
    for j in range(n_bonus):
        d = post_days[(j * len(post_days)) // max(n_bonus, 1)].date()   # even spread = low noise
        eligible = [c for c in mtn_pool if signup[c] <= d]
        if not eligible:
            continue
        specs.append((rng.choice(eligible), d, REGIONAL_REGION))

    prod = products.set_index("sku")
    sku_pool = products["sku"].to_numpy()
    sku_w = (1.0 / (products["list_price"].to_numpy() ** 0.5)); sku_w /= sku_w.sum()
    basket_p = [SINGLE_ITEM_SHARE, 0.22, 0.10, 0.05, 0.03]
    basket_p = list(np.array(basket_p) / sum(basket_p))

    orders, items, oi = [], [], 1
    mismatch_target = int(len(specs) * NUM_ITEMS_MISMATCH); mismatch_done = 0

    for k, (cid, d, ship_region) in enumerate(specs):
        oid = f"ORD-{k+1:07d}"
        ts = datetime(d.year, d.month, d.day, int(rng.integers(6, 23)),
                      int(rng.integers(0, 60)), int(rng.integers(0, 60)))
        ship_state = rng.choice(REGION_STATES[ship_region])
        channel = rng.choice(ORDER_CHANNELS, p=[0.55, 0.33, 0.12])

        n_lines = int(rng.choice([1, 2, 3, 4, 5], p=basket_p))
        chosen_skus = rng.choice(sku_pool, size=n_lines, replace=False, p=sku_w)
        line_rows, subtotal, item_disc_total, classes = [], 0.0, 0.0, []
        for sku in chosen_skus:
            p = prod.loc[sku]
            qty = int(rng.choice([1, 1, 1, 2, 3], p=[0.6, 0.15, 0.1, 0.1, 0.05]))
            unit_list = float(p["current_price"]) if rng.random() < 0.7 else float(p["list_price"])
            unit_disc = round(unit_list * rng.choice([0, 0, 0.05, 0.10], p=[0.7, 0.1, 0.12, 0.08]), 2)
            line_gross = round(qty * unit_list, 2)
            line_rev = round(line_gross - qty * unit_disc, 2)
            unit_cost = float(p["unit_cost"])
            returned_prov = rng.random() < float(p["return_rate"])
            ret_qty_prov = int(rng.integers(1, qty + 1)) if returned_prov else 0
            subtotal += line_gross; item_disc_total += qty * unit_disc; classes.append(p["shipping_class"])
            line_rows.append({
                "order_item_id": f"OI-{oi:08d}", "order_id": oid, "sku": sku, "customer_id": cid,
                "quantity": qty, "unit_list_price": round(unit_list, 2), "unit_discount": unit_disc,
                "line_gross": line_gross, "line_revenue": line_rev, "unit_cost": unit_cost,
                "line_margin": round(line_rev - qty * unit_cost, 2), "category": p["category"],
                "is_gift": bool(rng.random() < 0.06), "item_status": "Fulfilled",
                "return_quantity": 0, "item_refund_amount": 0.0, "return_reason": "",
                "_returned": returned_prov, "_ret_qty": ret_qty_prov,
            })
            oi += 1
        subtotal = round(subtotal, 2); item_disc_total = round(item_disc_total, 2)

        order_discount, promo = (round(subtotal * rng.choice([0.05, 0.10, 0.15], p=[0.5, 0.35, 0.15]), 2),
                                 rng.choice(PROMO_CODES)) if rng.random() < ORDER_DISCOUNT_RATE else (0.0, "")
        revenue = round(subtotal - item_disc_total - order_discount, 2)

        # shipping: threshold by date, Mountain free post-shock; bulky items can still pay (fix 10)
        thresh = THRESHOLD_BEFORE if d < THRESHOLD_DATE else THRESHOLD_AFTER
        mountain_free = (ship_region == REGIONAL_REGION and d >= REGIONAL_DATE)
        bulky = any(c in ("Heavy", "Oversized") for c in classes)
        if mountain_free or promo == "FREESHIP":
            shipping_fee, free_ship = 0.0, True
        elif subtotal >= thresh and not ((bulky and rng.random() < 0.5) or rng.random() < FREE_SHIP_EXCEPTION_RATE):
            shipping_fee, free_ship = 0.0, True   # most clear the threshold; bulky/excluded items still pay
        else:
            base = {"Small": 5, "Standard": 9, "Heavy": 18, "Oversized": 30}
            shipping_fee, free_ship = round(base.get(classes[0], 9) * rng.uniform(0.9, 1.4), 2), False

        tax = round(revenue * rng.uniform(0.06, 0.09), 2)

        # order status: recent orders are mostly still pending (right-censoring), older mostly completed
        days_to_snap = (SNAPSHOT_DATE - d).days
        r0 = rng.random()
        if days_to_snap <= 7:
            status = "Pending" if r0 < 0.60 else ("Cancelled" if r0 < 0.64 else "Completed")
        else:
            status = "Cancelled" if r0 < 0.04 else ("Pending" if r0 < 0.07 else "Completed")

        # returns only on completed orders old enough to have come back
        can_return = status == "Completed" and days_to_snap >= RETURN_CENSOR_DAYS

        # allocate order_discount across lines so a refund never exceeds what was collected
        sum_line_rev = subtotal - item_disc_total
        for r in line_rows:
            share = (r["line_revenue"] / sum_line_rev) if sum_line_rev > 0 else 0.0
            net_paid = r["line_revenue"] - order_discount * share          # actual cash for this line
            if can_return and r["_returned"]:
                rq = r["_ret_qty"]
                r["return_quantity"] = rq
                r["item_status"] = "Returned"
                r["item_refund_amount"] = round(net_paid / r["quantity"] * rq, 2)
                r["return_reason"] = rng.choice(RETURN_REASONS)
            elif status == "Cancelled":
                r["item_status"] = "Cancelled"
            r.pop("_returned", None); r.pop("_ret_qty", None)

        line_refund = round(sum(r["item_refund_amount"] for r in line_rows), 2)
        if line_refund > 0 and rng.random() < REFUND_MISMATCH_RATE:
            refund_amount = round(line_refund * rng.uniform(0.90, 0.98), 2)   # restocking-fee style gap
        else:
            refund_amount = line_refund

        if status == "Completed":
            refund_amount = min(refund_amount, revenue)                       # never refund more than collected
            adjusted_revenue = round(max(0.0, revenue - refund_amount), 2)
            gross_collected = round(revenue + shipping_fee + tax, 2)
            return_flag = refund_amount > 0
        else:
            shipping_fee = tax = refund_amount = 0.0
            adjusted_revenue = gross_collected = 0.0
            free_ship, return_flag = False, False

        items.extend(line_rows)

        # num_items: usually true count; ~1% off by one, never below 1 (fix 9)
        true_count = n_lines
        if mismatch_done < mismatch_target and rng.random() < 0.5:
            delta = 1 if true_count == 1 else int(rng.choice([-1, 1]))
            num_items = true_count + delta; mismatch_done += 1
        else:
            num_items = true_count

        # shipping speed and lateness (fix 8)
        ship_speed = "Two-Day" if mountain_free else rng.choice(SHIP_SPEEDS, p=[0.6, 0.25, 0.15])
        late_rate = LATE_RATE[ship_speed] * (1.4 if bulky else 1.0)
        late = bool(status == "Completed" and rng.random() < late_rate)

        device = "In-Store POS" if channel == "In-Store" else ("Mobile" if channel == "Mobile App"
                 else rng.choice(DEVICES, p=[0.5, 0.35, 0.15]))

        orders.append({
            "order_id": oid, "customer_id": cid, "order_timestamp": ts.isoformat(), "order_date": d.isoformat(),
            "channel": channel, "ship_to_region": ship_region, "ship_to_state": ship_state,
            "num_items": int(num_items), "subtotal": subtotal, "item_discount_total": item_disc_total,
            "order_discount": order_discount, "shipping_fee": shipping_fee, "tax": tax, "revenue": revenue,
            "adjusted_revenue": adjusted_revenue, "gross_collected": gross_collected,
            "refund_amount": refund_amount, "return_flag": return_flag, "order_status": status,
            "payment_method": rng.choice(PAYMENTS), "promo_code": promo, "free_shipping_applied": free_ship,
            "shipping_speed": ship_speed, "delivery_late_flag": late, "device_type": device,
            "is_first_order": False,
        })

    orders_df = pd.DataFrame(orders)
    items_df = pd.DataFrame(items)
    first_idx = orders_df.sort_values("order_timestamp").groupby("customer_id").head(1).index
    orders_df.loc[first_idx, "is_first_order"] = True

    log_plant("O1", "orders / order_items", "revenue, order_discount, line_revenue",
              "order_discount is an order-level promo not allocated to lines, so SUM(line_revenue) != orders.revenue.",
              "revenue equals SUM(line_revenue) - order_discount. Naive line-summing overstates revenue.", "Ch 4")
    log_plant("O2", "orders", "revenue, adjusted_revenue, gross_collected",
              "Three revenue definitions: merchandise (revenue), net of refunds (adjusted_revenue), gross cash incl shipping+tax (gross_collected).",
              "Agree which one the metric means before reporting.", "Ch 3")
    log_plant("O3", "orders", "num_items",
              f"~{NUM_ITEMS_MISMATCH*100:.0f}% of orders have num_items not equal to their order_items line count (never 0).",
              "Compare num_items to COUNT(order_items) per order_id.", "Ch 4")
    log_plant("O4", "orders", "shipping_fee, free_shipping_applied, subtotal",
              f"Free-shipping threshold dropped from {THRESHOLD_BEFORE:.0f} to {THRESHOLD_AFTER:.0f} on {THRESHOLD_DATE}. Bulky items can still pay above it.",
              "RDD on subtotal at the cutoff; DiD on the newly-treated 35-50 band before/after.", "Ch 6")
    log_plant("O5", "orders", "ship_to_region, order_date",
              f"{REGIONAL_REGION} received free 2-day shipping on {REGIONAL_DATE}, lifting orders ~{REGIONAL_LIFT*100:.0f}%.",
              "Synthetic control: treat Mountain, donor pool = other 9 regions, weekly series.", "Ch 6")
    log_plant("O6", "orders", "ship_to_region vs customers.region",
              "~8% of orders ship to a region different from the customer's home region.",
              "Do not assume ship_to_region equals the customer's region in joins.", "Ch 4")
    log_plant("O7", "orders / order_items", "refund_amount vs item_refund_amount",
              f"~{REFUND_MISMATCH_RATE*100:.0f}% of refunded orders have an order-level refund that differs from the line sum.",
              "Most refunds reconcile exactly; a minority carry order-level adjustments.", "Ch 4")
    return orders_df, items_df

# --------------------------------------------------------------------------- #
# DERIVE account_status + customer_segment from behaviour (no zombie buyers)    #
# --------------------------------------------------------------------------- #
def derive_status_and_segment(customers, orders):
    active_orders = orders[orders["order_status"].isin(["Completed", "Pending"])].copy()
    active_orders["order_date"] = pd.to_datetime(active_orders["order_date"])
    last = active_orders.groupby("customer_id")["order_date"].max()          # recency for status
    comp = orders[orders["order_status"] == "Completed"].copy()
    ncomp = comp.groupby("customer_id").size()                                # purchases for segment
    value = comp.groupby("customer_id")["revenue"].sum()
    vip_cut = value.quantile(0.90) if len(value) else 0.0
    snap = pd.Timestamp(SNAPSHOT_DATE)

    statuses, segments = [], []
    for r in customers.itertuples():
        cid = r.customer_id
        signup = date.fromisoformat(r.signup_date)
        if cid in last.index:
            days = (snap - last[cid]).days
            n = int(ncomp.get(cid, 0)); val = float(value.get(cid, 0.0))
            status = "Active" if days <= 90 else ("Dormant" if days <= 365 else "Closed")
            if val >= vip_cut:   seg = "VIP"
            elif n >= 5:         seg = "Loyal"
            elif n >= 2:         seg = "Returning"
            else:                seg = "New"
            if status in ("Dormant", "Closed") and rng.random() < 0.5:
                seg = "Dormant"
        else:
            status = "Active" if (SNAPSHOT_DATE - signup).days <= 180 else "Dormant"
            seg = "New"
        if rng.random() < 0.12:                 # definition-ambiguity fuzz (plant C5)
            seg = rng.choice(SEGMENTS)
        statuses.append(status); segments.append(seg)
    customers = customers.copy()
    customers["account_status"] = statuses
    customers["customer_segment"] = segments
    return customers

# --------------------------------------------------------------------------- #
# VALIDATION                                                                   #
# --------------------------------------------------------------------------- #
def validate(customers, products, orders, items):
    print("\n" + "=" * 72 + "\nVALIDATION REPORT\n" + "=" * 72)
    def check(label, ok, detail=""):
        print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  ({detail})" if detail else "")); return ok

    print(f"\nRows: customers={len(customers)} products={len(products)} "
          f"orders={len(orders)} order_items={len(items)}")

    check("orders.customer_id in customers", orders["customer_id"].isin(customers["customer_id"]).all())
    check("order_items.order_id in orders", items["order_id"].isin(orders["order_id"]).all())
    check("order_items.sku in products", items["sku"].isin(products["sku"]).all())

    lg = items.groupby("order_id")["line_gross"].sum().round(2)
    sub = orders.set_index("order_id")["subtotal"].round(2)
    check("subtotal == SUM(line_gross)", ((lg - sub.reindex(lg.index)).abs() < 0.05).all())
    lr = items.groupby("order_id")["line_revenue"].sum().round(2)
    o = orders.set_index("order_id")
    gap = (lr - o["order_discount"].reindex(lr.index) - o["revenue"].reindex(lr.index)).abs()
    check("revenue == SUM(line_revenue) - order_discount", (gap < 0.05).all(), f"max {gap.max():.2f}")

    # orders after signup (the critical v1 bug)
    su = customers.set_index("customer_id")["signup_date"].apply(date.fromisoformat)
    od = orders.assign(sd=orders["customer_id"].map(su),
                       odt=pd.to_datetime(orders["order_date"]).dt.date)
    before = (od["odt"] < od["sd"]).sum()
    check("no orders before signup_date", before == 0, f"{before} violations")

    # cancelled/pending collect nothing
    bad_cancel = orders[(orders["order_status"] != "Completed") &
                        ((orders["gross_collected"] > 0) | (orders["adjusted_revenue"] > 0) |
                         (orders["refund_amount"] > 0))]
    check("non-Completed orders collect nothing", len(bad_cancel) == 0, f"{len(bad_cancel)} bad")

    # refunds never exceed collected revenue (no negative net merchandise revenue)
    check("adjusted_revenue >= 0 always", (orders["adjusted_revenue"] >= 0).all(),
          f"min {orders['adjusted_revenue'].min():.2f}")
    check("refund_amount <= revenue on Completed",
          (orders.loc[orders['order_status'] == 'Completed', 'refund_amount'] <=
           orders.loc[orders['order_status'] == 'Completed', 'revenue'] + 0.01).all())

    # no returns on non-Completed orders; no returns inside the censor window
    oi_st = items.merge(orders[["order_id", "order_status", "order_date"]], on="order_id")
    bad_ret_status = oi_st[(oi_st["order_status"] != "Completed") & (oi_st["return_quantity"] > 0)]
    check("no returned items on non-Completed orders", len(bad_ret_status) == 0, f"{len(bad_ret_status)}")
    oi_st["odt"] = pd.to_datetime(oi_st["order_date"])
    recent_ret = oi_st[(oi_st["return_quantity"] > 0) &
                       ((pd.Timestamp(SNAPSHOT_DATE) - oi_st["odt"]).dt.days < RETURN_CENSOR_DAYS)]
    check("no returns within the censor window", len(recent_ret) == 0,
          f"{len(recent_ret)} recent returns")

    # account_status consistent with recency (completed + pending count as activity)
    act = orders[orders["order_status"].isin(["Completed", "Pending"])].copy()
    act["order_date"] = pd.to_datetime(act["order_date"])
    last = act.groupby("customer_id")["order_date"].max()
    snap = pd.Timestamp(SNAPSHOT_DATE)
    cs = customers.set_index("customer_id")
    active_no_recent = 0
    for cid in cs.index[cs["account_status"] == "Active"]:
        if cid in last.index and (snap - last[cid]).days > 90:
            active_no_recent += 1
    check("Active accounts have a recent order (or are new)", active_no_recent == 0,
          f"{active_no_recent} contradictions")

    # geo consistency among clean rows (uppercase, not the planted mismatch)
    bad_city = bad_zip = bad_state = 0
    for r in customers.itertuples():
        st = r.state
        if st != st.upper():            # lowercase plant, skip
            continue
        if st not in STATE_REGION or STATE_REGION[st] != r.region: bad_state += 1
        if st in STATE_ZIP and not str(r.zip_code).startswith(f"{STATE_ZIP[st]:02d}"): bad_zip += 1
        if st in STATE_CITY and r.city not in STATE_CITY[st]: bad_city += 1
    # the controlled geo plant accounts for ~GEO_MISMATCH_RATE city mismatches
    expected_geo = int(len(customers) * GEO_MISMATCH_RATE) + 3
    check("region/state consistent (clean rows)", bad_state == 0, f"{bad_state}")
    check("zip prefix matches state (clean rows)", bad_zip == 0, f"{bad_zip}")
    check("city matches state except planted mismatch", bad_city <= expected_geo,
          f"{bad_city} city mismatches (~{expected_geo} planted)")

    # product weight plausible by category
    pw = products.merge(pd.DataFrame(
        [{"category": c, "wlo": lo, "whi": hi} for c, (lo, hi) in CATEGORY_WEIGHT.items()]), on="category")
    bad_w = ((pw["weight_kg"] < pw["wlo"] * 0.9) | (pw["weight_kg"] > pw["whi"] * 1.1)).sum()
    check("product weight plausible by category", bad_w == 0, f"{bad_w} implausible")

    # threshold discontinuity (now realistic, not a perfect 100%)
    band = orders[(orders["subtotal"] >= 35) & (orders["subtotal"] < 50) &
                  (orders["ship_to_region"] != REGIONAL_REGION) & (orders["promo_code"] != "FREESHIP")]
    pre = band[band["order_date"] < THRESHOLD_DATE.isoformat()]["free_shipping_applied"].mean()
    post = band[band["order_date"] >= THRESHOLD_DATE.isoformat()]["free_shipping_applied"].mean()
    check("threshold lifts free-shipping in 35-50 band", (post - (pre if pd.notna(pre) else 0)) > 0.5,
          f"free-ship pre={pre:.2f} post={post:.2f}")

    # Mountain effect via donor difference-in-differences (honest)
    o2 = orders.copy(); o2["order_date"] = pd.to_datetime(o2["order_date"])
    cut = pd.Timestamp(REGIONAL_DATE)
    pre_d = (cut - pd.Timestamp(DATE_START)).days; post_d = (pd.Timestamp(DATE_END) - cut).days + 1
    mtn = o2[o2["ship_to_region"] == REGIONAL_REGION]; don = o2[o2["ship_to_region"] != REGIONAL_REGION]
    mp = len(mtn[mtn["order_date"] < cut]) / pre_d; mq = len(mtn[mtn["order_date"] >= cut]) / post_d
    dp = len(don[don["order_date"] < cut]) / pre_d; dq = len(don[don["order_date"] >= cut]) / post_d
    did = (mq / mp) / (dq / dp) - 1
    check("Mountain effect recoverable above donor trend", did > 0.08,
          f"raw +{(mq/mp-1)*100:.0f}% (mostly seasonality), donor-adjusted +{did*100:.0f}%")

    # late rate gradient by shipping speed
    lr_rate = orders[orders["order_status"] == "Completed"].groupby("shipping_speed")["delivery_late_flag"].mean()
    grad = lr_rate.get("Standard", 0) > lr_rate.get("Two-Day", 1)
    check("faster shipping is less late", grad,
          f"Standard={lr_rate.get('Standard',0):.2f} Two-Day={lr_rate.get('Two-Day',0):.2f}")

    # num_items never 0
    check("num_items >= 1 always", (orders["num_items"] >= 1).all())

    # churn
    churn = (snap - last).dt.days > CHURN_WINDOW
    never = ~customers["customer_id"].isin(last.index)
    print(f"\nDerivable churn rate at {SNAPSHOT_DATE}: "
          f"{(churn.sum() + never.sum()) / len(customers) * 100:.1f}%")
    print(f"account_status mix: {customers['account_status'].value_counts(normalize=True).round(3).to_dict()}")
    print(f"order_status mix:   {orders['order_status'].value_counts(normalize=True).round(3).to_dict()}")
    print(f"single-item share:  {(items.groupby('order_id').size() == 1).mean()*100:.1f}%")
    print(f"plants catalogued in known_plants.csv: {len(PLANTS)}")
    print("=" * 72 + "\n")

# --------------------------------------------------------------------------- #
# DATA DICTIONARY                                                              #
# --------------------------------------------------------------------------- #
def build_data_dictionary():
    dd = [
        ("customers", "customer_id", "string", "Primary key, C000001 format"),
        ("customers", "first_name", "string", "Given name"),
        ("customers", "last_name", "string", "Family name"),
        ("customers", "email_domain", "string", "Email domain only; internal domains flag test accounts"),
        ("customers", "signup_date", "date", "Account creation date; always on or before the customer's first order"),
        ("customers", "acquisition_channel", "enum", "How the customer was acquired"),
        ("customers", "region", "enum", "Customer home region"),
        ("customers", "state", "string", "Customer home state, recorded as a 2-letter code"),
        ("customers", "city", "string", "Customer home city"),
        ("customers", "zip_code", "string", "5-digit, state-consistent prefix"),
        ("customers", "age_band", "enum", "Age bucket; 'Unknown' indicates an unspecified age band"),
        ("customers", "gender", "enum", "Customer gender category"),
        ("customers", "customer_segment", "enum", "CRM segment; assignment criteria are undocumented"),
        ("customers", "loyalty_member", "bool", "Loyalty program membership"),
        ("customers", "marketing_opt_in", "bool", "Marketing consent"),
        ("customers", "preferred_device", "enum", "Self-reported device preference"),
        ("customers", "account_status", "enum", "Active/Dormant/Closed, derived from order recency at the snapshot date"),
        ("customers", "is_test_account", "bool", "Indicates whether the account is flagged as internal or test"),
        ("products", "sku", "string", "Primary key, SKU-10001 format"),
        ("products", "product_name", "string", "Brand + series + subcategory + category-appropriate size"),
        ("products", "category", "enum", "12 product categories"),
        ("products", "subcategory", "string", "Category-specific subtype"),
        ("products", "brand", "enum", "Invented brands; Cascade Basics is private label"),
        ("products", "is_private_label", "bool", "True for Cascade Basics"),
        ("products", "unit_cost", "decimal", "Cost of goods"),
        ("products", "list_price", "decimal", "Reference list price"),
        ("products", "current_price", "decimal", "Current price, may reflect markdown"),
        ("products", "margin_pct", "decimal", "Catalog gross margin off list price: (list_price - unit_cost)/list_price"),
        ("products", "launch_date", "date", "First available date (2022-2023; in catalog for the whole order window)"),
        ("products", "is_active", "bool", "Current snapshot; discontinued products keep historical sales"),
        ("products", "weight_kg", "decimal", "Category-appropriate shipping weight"),
        ("products", "shipping_class", "enum", "Small/Standard/Heavy/Oversized, derived from weight (TVs Oversized)"),
        ("products", "return_rate", "decimal", "Baseline return propensity"),
        ("orders", "order_id", "string", "Primary key, ORD-0000001 format"),
        ("orders", "customer_id", "string", "FK to customers"),
        ("orders", "order_timestamp", "datetime", "Order placement time; on or after signup_date"),
        ("orders", "order_date", "date", "Date component of the timestamp"),
        ("orders", "channel", "enum", "Web/Mobile App/In-Store"),
        ("orders", "ship_to_region", "enum", "Order destination region, which may differ from the customer home region"),
        ("orders", "ship_to_state", "string", "Destination state, consistent with ship_to_region"),
        ("orders", "num_items", "int", "Recorded number of order lines, not units"),
        ("orders", "subtotal", "decimal", "Sum of line_gross before order discount/ship/tax"),
        ("orders", "item_discount_total", "decimal", "Sum of line-level discounts (allocated)"),
        ("orders", "order_discount", "decimal", "Order-level promo, NOT allocated to lines"),
        ("orders", "shipping_fee", "decimal", "By threshold date, region, class; 0 for non-Completed"),
        ("orders", "tax", "decimal", "Tax on net merchandise; 0 for non-Completed"),
        ("orders", "revenue", "decimal", "Gross merchandise value: subtotal - item_discount_total - order_discount (any status)"),
        ("orders", "adjusted_revenue", "decimal", "revenue - refund_amount for Completed; 0 otherwise"),
        ("orders", "gross_collected", "decimal", "Gross cash at purchase: revenue + shipping_fee + tax, pre-refund; 0 if not Completed"),
        ("orders", "refund_amount", "decimal", "Refund amount recorded at the order level"),
        ("orders", "return_flag", "bool", "True when refund_amount > 0"),
        ("orders", "order_status", "enum", "Completed / Cancelled / Pending (returns are an attribute, not a status)"),
        ("orders", "payment_method", "enum", "Tender type"),
        ("orders", "promo_code", "string", "Applied promo, blank if none"),
        ("orders", "free_shipping_applied", "bool", "Threshold/region marker"),
        ("orders", "shipping_speed", "enum", "Standard/Expedited/Two-Day; affects late rate"),
        ("orders", "delivery_late_flag", "bool", "Delivered later than promised"),
        ("orders", "device_type", "enum", "Desktop/Mobile/Tablet/In-Store POS"),
        ("orders", "is_first_order", "bool", "Customer's earliest order"),
        ("order_items", "order_item_id", "string", "Primary key, OI-00000001 format"),
        ("order_items", "order_id", "string", "FK to orders"),
        ("order_items", "sku", "string", "FK to products"),
        ("order_items", "customer_id", "string", "Denormalized FK to customers"),
        ("order_items", "quantity", "int", "Units in the line"),
        ("order_items", "unit_list_price", "decimal", "Price snapshot; may differ from products.list_price"),
        ("order_items", "unit_discount", "decimal", "Per-unit line discount"),
        ("order_items", "line_gross", "decimal", "quantity * unit_list_price"),
        ("order_items", "line_revenue", "decimal", "line_gross - quantity*unit_discount"),
        ("order_items", "unit_cost", "decimal", "Cost snapshot"),
        ("order_items", "line_margin", "decimal", "line_revenue - quantity*unit_cost"),
        ("order_items", "category", "string", "Denormalized product category"),
        ("order_items", "is_gift", "bool", "Marked as gift"),
        ("order_items", "item_status", "enum", "Fulfilled / Returned / Cancelled"),
        ("order_items", "return_quantity", "int", "Units returned"),
        ("order_items", "item_refund_amount", "decimal", "Line refund value"),
        ("order_items", "return_reason", "enum", "One of: " + ", ".join(RETURN_REASONS) + "; blank otherwise"),
    ]
    return pd.DataFrame(dd, columns=["table", "column", "type", "description"])

# --------------------------------------------------------------------------- #
# MAIN                                                                         #
# --------------------------------------------------------------------------- #
def main():
    products = build_products()
    customers = build_customers()
    orders, items = build_orders_and_items(customers, products)
    customers = derive_status_and_segment(customers, orders)

    validate(customers, products, orders, items)

    cust_out = customers.drop(columns=[c for c in customers.columns if c.startswith("_")])
    # column order: put derived status/segment near the other customer attributes
    cols = ["customer_id", "first_name", "last_name", "email_domain", "signup_date",
            "acquisition_channel", "region", "state", "city", "zip_code", "age_band", "gender",
            "customer_segment", "loyalty_member", "marketing_opt_in", "preferred_device",
            "account_status", "is_test_account"]
    cust_out = cust_out[cols]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cust_out.to_csv(os.path.join(OUTPUT_DIR, "customers.csv"), index=False)
    products.to_csv(os.path.join(OUTPUT_DIR, "products.csv"), index=False)
    orders.to_csv(os.path.join(OUTPUT_DIR, "orders.csv"), index=False)
    items.to_csv(os.path.join(OUTPUT_DIR, "order_items.csv"), index=False)
    build_data_dictionary().to_csv(os.path.join(OUTPUT_DIR, "data_dictionary.csv"), index=False)
    pd.DataFrame(PLANTS).to_csv(os.path.join(OUTPUT_DIR, "known_plants.csv"), index=False)
    print("Wrote customers.csv, products.csv, orders.csv, order_items.csv, data_dictionary.csv, known_plants.csv")


if __name__ == "__main__":
    main()
