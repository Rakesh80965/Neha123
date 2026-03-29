import os
import re
import httpx
from flask import Flask, render_template_string, request, jsonify, send_from_directory, session, redirect, url_for

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(24).hex())

# ============================================================================
# SUPABASE CONFIGURATION
# ============================================================================
SUPABASE_URL = "https://gscxycvoeprxmkzfvnks.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdzY3h5Y3ZvZXByeG1remZ2bmtzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzNjA0OTAsImV4cCI6MjA4OTkzNjQ5MH0.CVqLTwGfTCdA2EeSu2ayEv3ID4P68STHgm8XM0c-rus"

def _sb_headers(extra=None):
    h = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}
    if extra:
        h.update(extra)
    return h

def sb_auth_signup(email, password):
    r = httpx.post(f"{SUPABASE_URL}/auth/v1/signup", json={"email": email, "password": password}, headers=_sb_headers(), timeout=30.0)
    if r.status_code >= 400:
        data = r.json()
        raise Exception(data.get("msg") or data.get("error_description") or data.get("message") or r.text)
    return r.json()

def sb_auth_signin(email, password):
    r = httpx.post(f"{SUPABASE_URL}/auth/v1/token?grant_type=password", json={"email": email, "password": password}, headers=_sb_headers(), timeout=30.0)
    if r.status_code >= 400:
        data = r.json()
        raise Exception(data.get("error_description") or data.get("msg") or data.get("message") or r.text)
    return r.json()

def sb_select(table, columns="*", filters=None, order=None, limit=None):
    params = {"select": columns}
    if order:
        params["order"] = order
    if limit:
        params["limit"] = str(limit)
    if filters:
        params.update(filters)
    r = httpx.get(f"{SUPABASE_URL}/rest/v1/{table}", params=params, headers=_sb_headers(), timeout=30.0)
    r.raise_for_status()
    return r.json()

def sb_insert(table, data):
    r = httpx.post(f"{SUPABASE_URL}/rest/v1/{table}", json=data, headers=_sb_headers({"Prefer": "return=representation"}), timeout=30.0)
    r.raise_for_status()
    return r.json()

def sb_delete(table, filters):
    r = httpx.delete(f"{SUPABASE_URL}/rest/v1/{table}", params=filters, headers=_sb_headers(), timeout=30.0)
    r.raise_for_status()

# ============================================================================
# SAMPLES SEED DATA
# ============================================================================
SAMPLES = [
    {"sample_no": 1001, "article": "SQUARE FLORAL", "product": "WHITE + PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "104*072", "construction_total": 176, "blend": "100% VISCOSE", "weave": "TWILL", "finish": "SOFT TOUCH", "gsm": 147},
    {"sample_no": 1002, "article": "HBS DOT PRINT", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "110*070", "construction_total": 180, "blend": "100% COTTON", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 113},
    {"sample_no": 1003, "article": "BELLE MEADE", "product": "DYED", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "140*076", "construction_total": 216, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "COTTON SOFT FIN", "gsm": 135},
    {"sample_no": 1004, "article": "GLENDALE", "product": "WHITE + PRINT", "yarn": "COMPACT", "count": "50*50", "count_avg": 50, "construction": "132*084", "construction_total": 216, "blend": "100% COTTON", "weave": "DOBBY", "finish": "SOFT TOUCH", "gsm": 109},
    {"sample_no": 1005, "article": "NAVY PEACOAT", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "104*072", "construction_total": 176, "blend": "100% COTTON", "weave": "PLAIN", "finish": "PEACH FIN HAND", "gsm": 111},
    {"sample_no": 1006, "article": "MSHR84 CHAVAL", "product": "WHITE + PRINT", "yarn": "CARDED", "count": "40*40", "count_avg": 40, "construction": "104*072", "construction_total": 176, "blend": "100% COTTON", "weave": "PLAIN", "finish": "COTTON SOFT FIN", "gsm": 111},
    {"sample_no": 1007, "article": "GARY", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "21*21", "count_avg": 21, "construction": "054*048", "construction_total": 102, "blend": "COTTON:LINEN", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 122},
    {"sample_no": 1008, "article": "NPD 44", "product": "DYED", "yarn": "COMPACT", "count": "30*44", "count_avg": 37, "construction": "076*044", "construction_total": 120, "blend": "COTTON:LENIN", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 133},
    {"sample_no": 1009, "article": "24P5 BL", "product": "WHITE + PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "148*106", "construction_total": 254, "blend": "100% COTTON", "weave": "PLAIN", "finish": "SOFT FIN TOUCH", "gsm": 106},
    {"sample_no": 1010, "article": "f323 091", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "50*50", "count_avg": 50, "construction": "130*084", "construction_total": 214, "blend": "COTTON:LYCRA", "weave": "TWILL", "finish": "SOFT FIN TOUCH", "gsm": 108},
    {"sample_no": 1011, "article": "MAROO", "product": "WHITE + PRINT", "yarn": "COMPACT YARN", "count": "40*40", "count_avg": 40, "construction": "116*080", "construction_total": 196, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "PEACH FIN HAND", "gsm": 123},
    {"sample_no": 1012, "article": "ALMETA", "product": "CHECKS", "yarn": "SLUB", "count": "40*30", "count_avg": 35, "construction": "080*054", "construction_total": 134, "blend": "100% COTTON", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 119},
    {"sample_no": 1013, "article": "LUMBERTON", "product": "CHECKS", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "094*080", "construction_total": 174, "blend": "100% COTTON", "weave": "DOBBY", "finish": "EASY TO IRON+SOFT TOUCH", "gsm": 144},
    {"sample_no": 1014, "article": "A37900DA", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "128*066", "construction_total": 194, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "PEACH FIN HAND", "gsm": 121},
    {"sample_no": 1015, "article": "A37055PA", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "50*60", "count_avg": 55, "construction": "144*104", "construction_total": 248, "blend": "COTTON:MODAL", "weave": "TWILL", "finish": "EASY TO IRON", "gsm": 118},
    {"sample_no": 1016, "article": "SANGARIA BASE", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "132*072", "construction_total": 204, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 123},
    {"sample_no": 1017, "article": "AG-2220", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "116*080", "construction_total": 196, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "PEACH FIN HAND", "gsm": 123},
    {"sample_no": 1018, "article": "61606V", "product": "DYED", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "195*104", "construction_total": 299, "blend": "100% COTTON", "weave": "DOBBY-SATIN", "finish": "COTTON SOFT FIN", "gsm": 123},
    {"sample_no": 1019, "article": "AW24-DBCH", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "104*072", "construction_total": 176, "blend": "100%VISCOSE", "weave": "TWILL", "finish": "SOFT FIN TOUCH", "gsm": 147},
    {"sample_no": 1020, "article": "AW24-WBST", "product": "PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "104*072", "construction_total": 176, "blend": "100%VISCOSE", "weave": "TWILL", "finish": "SOFT FIN TOUCH", "gsm": 147},
    {"sample_no": 1021, "article": "CRECK", "product": "CHECKS", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "064*054", "construction_total": 118, "blend": "COTTON:TENCEL", "weave": "TWILL", "finish": "BRUSHED", "gsm": 196},
    {"sample_no": 1022, "article": "BARBOUR", "product": "DYED", "yarn": "TFO", "count": "60*30", "count_avg": 45, "construction": "200*128", "construction_total": 328, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 273},
    {"sample_no": 1023, "article": "MOUNTAIN - E", "product": "DYED", "yarn": "TFO", "count": "20*20", "count_avg": 20, "construction": "064*054", "construction_total": 118, "blend": "100% COTTON", "weave": "TWILL", "finish": "NORMAL SOFT FIN", "gsm": 294},
    {"sample_no": 1024, "article": "A29600PC", "product": "YD+PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "138*096", "construction_total": 234, "blend": "100% COTTON", "weave": "TWILL", "finish": "NORMAL SOFT FIN", "gsm": 97},
    {"sample_no": 1025, "article": "A37864PB", "product": "YD+PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "062*056", "construction_total": 118, "blend": "100% VISCOSE", "weave": "TWILL", "finish": "BRUSHED", "gsm": 147},
    {"sample_no": 1026, "article": "A37342PA", "product": "DYED +PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "180*104", "construction_total": 284, "blend": "COTTON:MODAL", "weave": "SATIN", "finish": "EASY TO IRON+CALENDER", "gsm": 118},
    {"sample_no": 1027, "article": "CV PRI", "product": "DYED +PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "110*076", "construction_total": 186, "blend": "COTTON:VISCOSE", "weave": "TWILL", "finish": "BRUSHED", "gsm": 117},
    {"sample_no": 1028, "article": "BLUE SNOW FLAKES", "product": "PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "096*060", "construction_total": 156, "blend": "COTTON:VISCOSE", "weave": "TWILL", "finish": "BRUSHED", "gsm": 131},
    {"sample_no": 1029, "article": "A37238RA", "product": "PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "180*104", "construction_total": 284, "blend": "COTTON:MODAL", "weave": "SATIN", "finish": "EASY TO IRON+CALENDER", "gsm": 118},
    {"sample_no": 1030, "article": "F326PJSH", "product": "STRIPES", "yarn": "SLUB", "count": "20*20", "count_avg": 20, "construction": "072*062", "construction_total": 134, "blend": "100% COTTON", "weave": "DOBBY", "finish": "NORMAL SOFT FIN", "gsm": 167},
    {"sample_no": 1031, "article": "47F003G", "product": "DYED", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "128*080", "construction_total": 208, "blend": "COTTON:LINEN", "weave": "PLAIN", "finish": "COTTON SOFT FIN", "gsm": 130},
    {"sample_no": 1032, "article": "62068", "product": "WHITE+PRINT", "yarn": "COMPACT", "count": "50*50", "count_avg": 50, "construction": "144*092", "construction_total": 236, "blend": "100% COTTON", "weave": "DOBBY", "finish": "SOFT FIN TOUCH", "gsm": 119},
    {"sample_no": 1033, "article": "HARLAN", "product": "YD+PRINT", "yarn": "COMPACT", "count": "40*30", "count_avg": 35, "construction": "120*066", "construction_total": 186, "blend": "100% COTTON", "weave": "TWILL", "finish": "SOFT TOUCH", "gsm": 131},
    {"sample_no": 1034, "article": "MS12-375", "product": "DYED", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "194*104", "construction_total": 298, "blend": "100% COTTON", "weave": "DOBBY*SATIN", "finish": "COTTON SOFT FIN", "gsm": 124},
    {"sample_no": 1035, "article": "MFS-15346", "product": "PRINT", "yarn": "COMPACT", "count": "50*60", "count_avg": 55, "construction": "144*104", "construction_total": 248, "blend": "COTTON:MODAL", "weave": "TWILL", "finish": "SOFT FIN TOUCH", "gsm": 116},
    {"sample_no": 1036, "article": "MFS_16730", "product": "CHECKS", "yarn": "COMPACT", "count": "60*20", "count_avg": 40, "construction": "124*064", "construction_total": 188, "blend": "COTTON:LINEN", "weave": "PLAIN", "finish": "COTTON SOFT FIN", "gsm": 128},
    {"sample_no": 1037, "article": "MIDLAND", "product": "PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "154*096", "construction_total": 250, "blend": "100%MODAL", "weave": "DOBBY", "finish": "SOFT TOUCH", "gsm": 112},
    {"sample_no": 1038, "article": "A38235PA", "product": "DYED + PRINT", "yarn": "COMPACT*SLUB", "count": "50*30", "count_avg": 40, "construction": "112*066", "construction_total": 178, "blend": "100% COTTON", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 121},
    {"sample_no": 1039, "article": "A5680", "product": "YD+PIGMENT PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "104*088", "construction_total": 192, "blend": "COTTON:TENCEL", "weave": "TWILL", "finish": "SOFT TOUCH", "gsm": 120},
    {"sample_no": 1040, "article": "MOUNTAIN-B", "product": "DYED", "yarn": "TFO", "count": "20*20", "count_avg": 20, "construction": "064*054", "construction_total": 118, "blend": "100% COTTON", "weave": "DOBBY", "finish": "NORMAL SOFT FIN", "gsm": 294},
    {"sample_no": 1041, "article": "BDLN-0010", "product": "WHITE", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "180*110", "construction_total": 290, "blend": "100% COTTON", "weave": "SATIN", "finish": "ANTI MICROBIAL", "gsm": 122},
    {"sample_no": 1042, "article": "CREW", "product": "WHITE+PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "104*072", "construction_total": 176, "blend": "100%VISCOSE", "weave": "TWILL", "finish": "ANTI MICROBIAL", "gsm": 146},
    {"sample_no": 1043, "article": "BLOSSOM", "product": "WHITE+PRINT", "yarn": "COMPACT", "count": "40*30", "count_avg": 35, "construction": "120*072", "construction_total": 192, "blend": "COTTON:VISCOSE", "weave": "TWILL", "finish": "SOFT TOUCH+ANTI MICROBIAL", "gsm": 134},
    {"sample_no": 1044, "article": "40017252", "product": "WHITE+PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "084*068", "construction_total": 152, "blend": "TENCEL:LINEN", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 126},
    {"sample_no": 1045, "article": "OLIVE", "product": "DYED+PRINT", "yarn": "COMPACT", "count": "70*70", "count_avg": 70, "construction": "110*092", "construction_total": 202, "blend": "100% COTTON GIZ", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 73},
    {"sample_no": 1046, "article": "A37681PA", "product": "WHITE+PRINT", "yarn": "COMPACT", "count": "80*70", "count_avg": 75, "construction": "154*120", "construction_total": 274, "blend": "100% COTTON GIZ", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 91},
    {"sample_no": 1047, "article": "16027", "product": "CHECKS", "yarn": "TFO", "count": "80*40", "count_avg": 60, "construction": "104*072", "construction_total": 176, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 111},
    {"sample_no": 1048, "article": "F323PX", "product": "WHITE + PRINT", "yarn": "COMPACT", "count": "50*50", "count_avg": 50, "construction": "130*084", "construction_total": 214, "blend": "COTTON:LYCRA", "weave": "TWILL", "finish": "SOFT FIN TOUCH", "gsm": 108},
    {"sample_no": 1049, "article": "SMIL08182", "product": "CHECKS", "yarn": "SLUB", "count": "30*30", "count_avg": 30, "construction": "084*076", "construction_total": 160, "blend": "100% COTTON", "weave": "TWILL", "finish": "COTTON SOFT FIN", "gsm": 134},
    {"sample_no": 1050, "article": "TS23FMFW", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "180*104", "construction_total": 284, "blend": "100% COTTON", "weave": "SATIN", "finish": "SOFT FIN TOUCH", "gsm": 119},
]

def seed_database():
    """Seed the Supabase samples table if empty."""
    try:
        data = sb_select("samples", columns="sample_no", limit=1)
        if not data:
            sb_insert("samples", SAMPLES)
    except Exception:
        pass

def get_all_samples():
    """Get all samples from Supabase as list of dicts."""
    return sb_select("samples", order="sample_no")

# ============================================================================
# FEEL TERMS DICTIONARY
# ============================================================================
FEEL_DICTIONARY = {
    "Soft Feel": ["soft handfeel", "soft touch", "silky touch", "smooth feel", "peach finish", "soft fleece", "soft", "silky", "smooth", "peach"],
    "Good Drape": ["drapey", "drapy", "good fall", "flowy", "fluid", "elegant fall", "drape", "flow", "good drape"],
    "Shiny": ["high shine", "lustrous", "glossy", "sheen", "bright surface", "satin look", "shiny", "shine", "gloss", "lustre"],
    "Crisp": ["crisp", "stiff", "paper touch", "structured feel", "firm hand", "firm", "crisp look"],
    "Stretchable": ["stretchable", "stretch", "elastic", "lycra", "flex", "flexible", "spandex"],
    "Easy Care": ["easy care", "easy iron", "wrinkle free", "wrinkle resistant", "low maintenance", "wrinkle", "easy"],
    "Textured": ["textured", "grainy", "slub look", "uneven surface", "raw texture", "texture", "slub"],
    "Dense": ["durable", "strong", "long life", "sturdy", "dense", "thick", "heavy"],
    "Anti Microbial": ["anti microbial", "antimicrobial", "anti-microbial", "antibacterial", "anti bacterial", "germ resistant", "hygienic"],
}

# ============================================================================
# RULE TABLE
# ============================================================================
RULE_TABLE = {
    "Soft Feel": {
        "yarn": {"values": ["compact", "combed", "slub", "tfo"], "priority": "HIGH"},
        "count": {"min": 30, "priority": "HIGH"},
        "blend": {"values": ["modal", "tencel", "viscose", "giz", "cotton"], "pure_first": True, "priority": "HIGH"},
        "blend_exclude": ["linen", "lenin"],
        "finish": {"values": ["soft touch", "brushed", "peach fin hand", "normal soft fin", "soft fin touch", "cotton soft fin", "chemical soft fin", "calender", "easy to iron", "anti microbial"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [
            {"blend": "100% cotton", "finish": ["anti microbial", "easy to iron"], "finish_override": ["soft touch", "brushed", "peach fin hand", "soft fin touch", "cotton soft fin"]}
        ],
    },
    "Good Drape": {
        "yarn": {"values": ["compact", "tfo", "combed", "slub"], "priority": "HIGH"},
        "blend": {"values": ["viscose", "tencel", "modal", "giz"], "pure_first": True, "priority": "HIGH"},
        "blend_exclude": ["100% cotton", "cotton:lycra", "cotton:linen", "cotton:lenin"],
        "blend_allow": ["giz"],
        "weave": {"values": ["satin", "twill", "dobby", "plain"], "priority": "HIGH"},
        "gsm": {"max": 200, "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Shiny": {
        "yarn": {"values": ["compact", "tfo"], "priority": "HIGH"},
        "count": {"min": 30, "priority": "HIGH"},
        "blend": {"values": ["tencel", "viscose", "modal", "giz", "cotton"], "pure_first": True, "priority": "HIGH"},
        "blend_exclude": ["linen", "lenin", "cotton:lycra"],
        "weave": {"values": ["twill", "satin", "dobby", "plain"], "priority": "HIGH"},
        "finish": {"values": ["calender", "calendar", "easy to iron"], "priority": "LOW"},
        "yarn_exclude": [],
        "negative_cross": [
            {"blend": "100% cotton", "weave": ["plain", "twill", "dobby", "satin"],
             "weave_override": ["dobby-satin", "dobby*satin"],
             "finish_override": ["anti microbial", "calender"]}
        ],
    },
    "Crisp": {
        "blend": {"values": ["linen", "lenin", "cotton"], "priority": "HIGH"},
        "weave": {"values": ["plain"], "priority": "LOW"},
        "yarn_exclude": [],
        "negative_cross": [
            {"blend": "100% cotton", "weave": ["twill", "satin", "dobby", "hbt"]}
        ],
    },
    "Stretchable": {
        "blend": {"values": ["lycra", "modal", "tencel", "viscose"], "priority": "HIGH"},
        "weave": {"values": ["twill", "satin", "dobby", "plain"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Easy Care": {
        "finish": {"values": ["easy to iron", "resin"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Textured": {
        "weave": {"values": ["dobby", "twill", "plain"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Dense": {
        "weave": {"values": ["matt", "twill", "plain", "dobby"], "priority": "HIGH"},
        "gsm": {"min": 190, "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Anti Microbial": {
        "finish": {"values": ["anti microbial"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_product(product):
    """Normalize product type by removing spaces around + for consistent matching"""
    return re.sub(r'\s*\+\s*', '+', product.upper().strip())

def contains_any(text, patterns):
    """Check if text contains any of the patterns (case-insensitive)"""
    text_lower = text.lower()
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return True
    return False

def get_blend_order_index(sample, standard_terms):
    """Return the lowest blend-values index matched across all active rules.
    Samples matching the first value in the list sort before those matching later values."""
    best = float('inf')
    for term in standard_terms:
        rule = RULE_TABLE.get(term)
        if not rule or "blend" not in rule:
            continue
        blend_values = rule["blend"].get("values", [])
        sample_blend = sample["blend"].lower()
        for idx, val in enumerate(blend_values):
            if val.lower() in sample_blend:
                if idx < best:
                    best = idx
                break
    return best if best != float('inf') else 9999

def calculate_priority_score(sample, standard_terms):
    """Calculate priority ranking score based on BLEND only.
    Follows the exact sequence in the rule table's blend values list.
    Pure 100% fiber ranks above mixed blends of the same fiber.
    Higher score = better match."""
    total_score = 0

    for term in standard_terms:
        rule = RULE_TABLE.get(term)
        if not rule:
            continue

        if "blend" not in rule or not isinstance(rule["blend"], dict):
            continue

        blend_values = rule["blend"].get("values", [])
        sample_blend = sample["blend"].lower().strip()
        max_positions = len(blend_values)

        # Find the highest-priority fiber that matches
        best_fiber_idx = None
        for idx, val in enumerate(blend_values):
            if val.lower() in sample_blend:
                best_fiber_idx = idx
                break

        if best_fiber_idx is not None:
            # Earlier position in list = higher score
            fiber_score = (max_positions - best_fiber_idx) * 1000

            # Pure/100% blend bonus: 100% of a fiber ranks above mixed
            is_pure = ("100%" in sample_blend) and (":" not in sample_blend) and ("/" not in sample_blend)
            if is_pure:
                # If pure_first flag is set, use large bonus so ALL pure blends
                # rank above ALL mixed blends regardless of fiber position
                if rule["blend"].get("pure_first", False):
                    fiber_score += (max_positions + 1) * 1000
                else:
                    fiber_score += 500

            total_score += fiber_score

    return total_score

def find_standard_terms(feel_text):
    """Parse feel_terms text and return list of matched standard terms"""
    if not feel_text or not feel_text.strip():
        return []

    feel_input_lower = feel_text.lower()
    matched = []

    for standard_term, keywords in FEEL_DICTIONARY.items():
        for kw in sorted(keywords, key=len, reverse=True):
            if kw.lower() in feel_input_lower:
                if standard_term not in matched:
                    matched.append(standard_term)
                break

    return matched

def check_attribute_match(sample, attr_key, attr_rule):
    """Check if a single attribute matches the rule condition"""
    if attr_key in ("yarn", "blend", "weave", "finish"):
        values = attr_rule.get("values", [])
        exact_values = attr_rule.get("exact_values", [])
        if contains_any(sample[attr_key], values):
            return True
        for ev in exact_values:
            if sample[attr_key].lower().strip() == ev.lower().strip():
                return True
        return False
    elif attr_key == "count":
        if "min" in attr_rule and sample["count_avg"] < attr_rule["min"]:
            return False
        if "max" in attr_rule and sample["count_avg"] > attr_rule["max"]:
            return False
        return True
    elif attr_key == "gsm":
        if "min" in attr_rule and sample["gsm"] < attr_rule["min"]:
            return False
        if "max" in attr_rule and sample["gsm"] > attr_rule["max"]:
            return False
        return True
    return True

def check_combo_rule(sample, rule):
    """Check sample against combination-based rules.
    Returns (passes, score) where score indicates match quality.
    """
    best_score = 0
    for combo in rule.get("positive_combos", []):
        combo_score = combo["score"]
        match = True
        for attr in ("yarn", "blend", "weave"):
            if attr in combo:
                if not contains_any(sample[attr], combo[attr]):
                    match = False
                    break
        if match:
            best_score = max(best_score, combo_score)

    if best_score == 0:
        return False, 0

    # Add finish bonus
    finish_bonus = rule.get("finish_bonus", [])
    if finish_bonus and contains_any(sample["finish"], finish_bonus):
        best_score += 1

    return True, best_score

def check_sample_against_rule(sample, standard_term):
    """Check sample against rule with priority support.
    Returns (passes, score):
      - passes: False if any HIGH priority attribute fails or negative rules trigger
      - score: count of LOW priority attributes that match (for sorting)
    """
    rule = RULE_TABLE.get(standard_term)
    if not rule:
        return True, 0

    # Handle combination-based rules (e.g., Textured)
    if rule.get("combo_mode"):
        return check_combo_rule(sample, rule)

    # Check yarn_exclude (always hard reject)
    if rule.get("yarn_exclude"):
        if contains_any(sample["yarn"], rule["yarn_exclude"]):
            return False, 0

    # Check blend_exclude (always hard reject, unless blend_allow overrides)
    if rule.get("blend_exclude"):
        if contains_any(sample["blend"], rule["blend_exclude"]):
            if not contains_any(sample["blend"], rule.get("blend_allow", [])):
                return False, 0

    # Check negative cross-attribute rules (always hard reject)
    for neg in rule.get("negative_cross", []):
        all_match = True
        for attr, condition in neg.items():
            if attr.endswith("_override"):
                continue
            sample_val = sample.get(attr, "")
            if isinstance(condition, list):
                if not contains_any(sample_val, condition):
                    all_match = False
                    break
            elif isinstance(condition, str):
                if condition.lower() not in sample_val.lower():
                    all_match = False
                    break
        if all_match:
            # Check if an override cancels the rejection
            overridden = False
            for attr, condition in neg.items():
                if attr.endswith("_override"):
                    base_attr = attr.replace("_override", "")
                    sample_val = sample.get(base_attr, "")
                    if contains_any(sample_val, condition):
                        overridden = True
                        break
            if not overridden:
                return False, 0

    # Check each attribute with priority
    score = 0
    for attr_key in ("yarn", "count", "blend", "weave", "finish", "gsm"):
        if attr_key not in rule:
            continue
        attr_rule = rule[attr_key]
        if not isinstance(attr_rule, dict) or "priority" not in attr_rule:
            continue

        priority = attr_rule.get("priority")
        if priority is None:
            continue

        matches = check_attribute_match(sample, attr_key, attr_rule)

        if priority == "HIGH":
            if not matches:
                return False, 0
        elif priority == "LOW":
            if matches:
                score += 1

    return True, score

def filter_samples(product_type, gsm_min, gsm_max, blend, weave, yarn, feel_terms):
    """Apply all filters and return matching samples"""
    results = get_all_samples()

    has_filters = (
        (product_type and product_type.upper() != "ALL") or
        gsm_min or gsm_max or
        (blend and blend.strip()) or
        (weave and weave.upper() != "ALL") or
        (yarn and yarn.upper() != "ALL") or
        (feel_terms and feel_terms.strip())
    )

    # Step 1: Filter by direct parameters
    if product_type and product_type.upper() != "ALL":
        norm_filter = normalize_product(product_type)
        results = [s for s in results if normalize_product(s["product"]) == norm_filter]

    if gsm_min:
        try:
            gsm_min_val = int(gsm_min)
            results = [s for s in results if s["gsm"] >= gsm_min_val]
        except ValueError:
            pass

    if gsm_max:
        try:
            gsm_max_val = int(gsm_max)
            results = [s for s in results if s["gsm"] <= gsm_max_val]
        except ValueError:
            pass

    if blend and blend.strip():
        results = [s for s in results if blend.lower() in s["blend"].lower()]

    if weave and weave.upper() != "ALL":
        results = [s for s in results if weave.lower() in s["weave"].lower()]

    if yarn and yarn.upper() != "ALL":
        results = [s for s in results if yarn.lower() in s["yarn"].lower()]

    # Step 2-4: Find standard terms and apply rules
    standard_terms = find_standard_terms(feel_terms)

    if feel_terms and feel_terms.strip() and not standard_terms:
        return [], standard_terms

    if standard_terms:
        for standard_term in standard_terms:
            filtered = []
            for s in results:
                passes, score = check_sample_against_rule(s, standard_term)
                if passes:
                    filtered.append(s)
            results = filtered

        # Calculate priority scores and sort best match first
        scored_results = []
        for s in results:
            s_copy = dict(s)
            s_copy["priority_score"] = calculate_priority_score(s, standard_terms)
            scored_results.append(s_copy)
        scored_results.sort(key=lambda s: -s["priority_score"])

        # Add recommendation rank
        for idx, s in enumerate(scored_results):
            s["rank"] = idx + 1
        results = scored_results

    if not has_filters:
        return [], standard_terms

    return results, standard_terms

# ============================================================================
# FLASK ROUTES
# ============================================================================

IMAGES_DIR = os.path.join(BASE_DIR, "SAMPLE IMAGES")

def login_required(f):
    """Simple login check decorator."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/sample-image/<int:sample_no>")
def sample_image(sample_no):
    filename = f"{sample_no}.jpeg"
    local_path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(local_path):
        return send_from_directory(IMAGES_DIR, filename)
    return redirect(f"{SUPABASE_URL}/storage/v1/object/public/Neha/{filename}")

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        try:
            result = sb_auth_signin(email, password)
            session["user_id"] = result["user"]["id"]
            session["username"] = result["user"]["email"]
            return redirect(url_for("dashboard"))
        except Exception:
            return render_template_string(LOGIN_TEMPLATE, error="Invalid email or password")
    return render_template_string(LOGIN_TEMPLATE, error=None)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not email or not password:
            return render_template_string(REGISTER_TEMPLATE, error="Email and password are required")
        if password != confirm:
            return render_template_string(REGISTER_TEMPLATE, error="Passwords do not match")
        if len(password) < 6:
            return render_template_string(REGISTER_TEMPLATE, error="Password must be at least 6 characters")
        try:
            result = sb_auth_signup(email, password)
            user = result.get("user")
            if user and user.get("id"):
                session["user_id"] = user["id"]
                session["username"] = user.get("email", email)
                return redirect(url_for("dashboard"))
            return render_template_string(REGISTER_TEMPLATE, error="Registration failed")
        except Exception as e:
            msg = str(e)
            if "already" in msg.lower():
                return render_template_string(REGISTER_TEMPLATE, error="Email already registered")
            return render_template_string(REGISTER_TEMPLATE, error=f"Error: {msg}")
    return render_template_string(REGISTER_TEMPLATE, error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE, username=session.get("username", ""))

@app.route("/api/samples")
@login_required
def api_all_samples():
    samples = get_all_samples()
    return jsonify({"samples": samples, "total_count": len(samples)})

@app.route("/search", methods=["POST"])
@login_required
def search():
    product_type = request.form.get("product_type", "ALL")
    gsm_min = request.form.get("gsm_min", "").strip()
    gsm_max = request.form.get("gsm_max", "").strip()
    blend = request.form.get("blend", "").strip()
    weave = request.form.get("weave", "ALL")
    yarn = request.form.get("yarn", "ALL")
    feel_terms = request.form.get("feel_terms", "").strip()

    results, standard_terms = filter_samples(product_type, gsm_min, gsm_max, blend, weave, yarn, feel_terms)

    return jsonify({
        "results": results,
        "standard_terms": standard_terms,
        "total_count": len(results),
    })

@app.route("/api/wishlist")
@login_required
def get_wishlist():
    user_id = session["user_id"]
    groups = sb_select("wishlist_groups", filters={"user_id": f"eq.{user_id}"}, order="name")
    result = []
    all_sample_nos = []
    for g in groups:
        items = sb_select("wishlists", columns="sample_no", filters={"user_id": f"eq.{user_id}", "group_id": f"eq.{g['id']}"})
        sample_nos = [item["sample_no"] for item in items]
        all_sample_nos.extend(sample_nos)
        if sample_nos:
            in_list = ",".join(str(n) for n in sample_nos)
            samples = sb_select("samples", filters={"sample_no": f"in.({in_list})"})
        else:
            samples = []
        result.append({"group_id": g["id"], "group_name": g["name"], "samples": samples, "count": len(samples)})
    return jsonify({"groups": result, "all_sample_nos": all_sample_nos, "total_count": len(all_sample_nos)})

@app.route("/api/wishlist/groups", methods=["GET"])
@login_required
def get_wishlist_groups():
    user_id = session["user_id"]
    groups = sb_select("wishlist_groups", columns="id,name", filters={"user_id": f"eq.{user_id}"}, order="name")
    return jsonify({"groups": groups})

@app.route("/api/wishlist/groups/create", methods=["POST"])
@login_required
def create_wishlist_group():
    data = request.get_json()
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Group name is required"}), 400
    user_id = session["user_id"]
    existing = sb_select("wishlist_groups", columns="id", filters={"user_id": f"eq.{user_id}", "name": f"eq.{name}"})
    if existing:
        return jsonify({"error": "Group already exists"}), 400
    result = sb_insert("wishlist_groups", {"user_id": user_id, "name": name})
    group = result[0]
    return jsonify({"status": "created", "group_id": group["id"], "name": group["name"]})

@app.route("/api/wishlist/groups/delete", methods=["POST"])
@login_required
def delete_wishlist_group():
    data = request.get_json()
    group_id = data.get("group_id")
    user_id = session["user_id"]
    group = sb_select("wishlist_groups", columns="id", filters={"id": f"eq.{group_id}", "user_id": f"eq.{user_id}"})
    if not group:
        return jsonify({"error": "Group not found"}), 404
    sb_delete("wishlists", {"user_id": f"eq.{user_id}", "group_id": f"eq.{group_id}"})
    sb_delete("wishlist_groups", {"id": f"eq.{group_id}", "user_id": f"eq.{user_id}"})
    return jsonify({"status": "deleted"})

@app.route("/api/wishlist/add", methods=["POST"])
@login_required
def add_to_wishlist():
    data = request.get_json()
    sample_no = data.get("sample_no")
    group_id = data.get("group_id")
    if not sample_no or not group_id:
        return jsonify({"error": "sample_no and group_id required"}), 400
    user_id = session["user_id"]
    group = sb_select("wishlist_groups", columns="id", filters={"id": f"eq.{group_id}", "user_id": f"eq.{user_id}"})
    if not group:
        return jsonify({"error": "Group not found"}), 404
    existing = sb_select("wishlists", columns="id", filters={"user_id": f"eq.{user_id}", "group_id": f"eq.{group_id}", "sample_no": f"eq.{sample_no}"})
    if not existing:
        sb_insert("wishlists", {"user_id": user_id, "group_id": group_id, "sample_no": sample_no})
    return jsonify({"status": "added", "sample_no": sample_no})

@app.route("/api/wishlist/remove", methods=["POST"])
@login_required
def remove_from_wishlist():
    data = request.get_json()
    sample_no = data.get("sample_no")
    group_id = data.get("group_id")
    if not sample_no or not group_id:
        return jsonify({"error": "sample_no and group_id required"}), 400
    user_id = session["user_id"]
    sb_delete("wishlists", {"user_id": f"eq.{user_id}", "group_id": f"eq.{group_id}", "sample_no": f"eq.{sample_no}"})
    return jsonify({"status": "removed", "sample_no": sample_no})

# ============================================================================
# HTML TEMPLATES
# ============================================================================

_AUTH_STYLES = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        background: linear-gradient(135deg, #0f1923 0%, #1a2740 40%, #2d4a7a 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .auth-container {
        width: 100%; max-width: 420px; padding: 1rem;
    }
    .auth-logo {
        text-align: center; margin-bottom: 2rem; color: white;
    }
    .auth-logo h1 { font-size: 1.8rem; letter-spacing: -0.5px; margin-bottom: 0.3rem; }
    .auth-logo p { opacity: 0.7; font-size: 0.95rem; }
    .auth-card {
        background: white;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .auth-card h2 { color: #1a2740; margin-bottom: 1.5rem; font-size: 1.4rem; text-align: center; }
    .auth-field { margin-bottom: 1.2rem; }
    .auth-field label {
        display: block; font-weight: 600; color: #1a2740;
        font-size: 0.85rem; margin-bottom: 0.4rem;
    }
    .auth-field input {
        width: 100%;
        padding: 0.8rem 1rem;
        border: 1.5px solid #dde1e6;
        border-radius: 10px;
        font-size: 1rem;
        font-family: inherit;
        transition: border-color 0.25s, box-shadow 0.25s;
        background: #fafbfc;
    }
    .auth-field input:focus {
        outline: none; border-color: #0097a7;
        box-shadow: 0 0 0 3px rgba(0,151,167,0.12);
        background: white;
    }
    .auth-btn {
        width: 100%;
        padding: 0.85rem;
        background: linear-gradient(135deg, #0097a7, #00838f);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.25s;
        margin-top: 0.5rem;
    }
    .auth-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,151,167,0.4); }
    .auth-error {
        background: #fff0f0;
        border: 1px solid #ffcdd2;
        color: #c62828;
        padding: 0.7rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        text-align: center;
    }
    .auth-link {
        text-align: center; margin-top: 1.5rem; font-size: 0.9rem; color: #666;
    }
    .auth-link a { color: #0097a7; text-decoration: none; font-weight: 600; }
    .auth-link a:hover { text-decoration: underline; }
</style>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In - Fabric Sample Tool</title>
    """ + _AUTH_STYLES + """
</head>
<body>
    <div class="auth-container">
        <div class="auth-logo">
            <h1>Fabric Sample Tool</h1>
            <p>Smart Search by Buyer Requirements</p>
        </div>
        <div class="auth-card">
            <h2>Sign In</h2>
            {% if error %}
            <div class="auth-error">{{ error }}</div>
            {% endif %}
            <form method="POST">
                <div class="auth-field">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="Enter your email" required autofocus>
                </div>
                <div class="auth-field">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" required>
                </div>
                <button type="submit" class="auth-btn">Sign In</button>
            </form>
            <div class="auth-link">
                Don't have an account? <a href="/register">Create one</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Fabric Sample Tool</title>
    """ + _AUTH_STYLES + """
</head>
<body>
    <div class="auth-container">
        <div class="auth-logo">
            <h1>Fabric Sample Tool</h1>
            <p>Create your account</p>
        </div>
        <div class="auth-card">
            <h2>Register</h2>
            {% if error %}
            <div class="auth-error">{{ error }}</div>
            {% endif %}
            <form method="POST">
                <div class="auth-field">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="Enter your email" required autofocus>
                </div>
                <div class="auth-field">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Create a password" required>
                </div>
                <div class="auth-field">
                    <label for="confirm">Confirm Password</label>
                    <input type="password" id="confirm" name="confirm" placeholder="Confirm your password" required>
                </div>
                <button type="submit" class="auth-btn">Create Account</button>
            </form>
            <div class="auth-link">
                Already have an account? <a href="/login">Sign in</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Fabric Sample Tool</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            background-color: #f0f2f5;
            color: #333;
            line-height: 1.6;
        }

        /* ---- HEADER (sticky) ---- */
        .header {
            background: linear-gradient(135deg, #1a2740 0%, #2d4a7a 100%);
            color: white;
            padding: 1.2rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            position: sticky;
            top: 0;
            z-index: 200;
        }
        .header-left h1 { font-size: 1.5rem; letter-spacing: -0.5px; }
        .header-left p { font-size: 0.85rem; opacity: 0.7; }
        .header-right { display: flex; align-items: center; gap: 1rem; }
        .header-user {
            display: flex; align-items: center; gap: 0.6rem;
            background: rgba(255,255,255,0.1);
            padding: 0.5rem 1rem;
            border-radius: 10px;
        }
        .header-avatar {
            width: 34px; height: 34px;
            background: linear-gradient(135deg, #0097a7, #00bcd4);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 0.9rem; color: white;
        }
        .header-username { font-weight: 600; font-size: 0.95rem; }
        .btn-logout {
            padding: 0.5rem 1.2rem;
            background: rgba(255,255,255,0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.25s;
        }
        .btn-logout:hover { background: rgba(255,255,255,0.25); }

        /* ---- SIDEBAR (sticky) ---- */
        .app-layout { display: flex; min-height: calc(100vh - 70px); }

        .sidebar {
            width: 240px;
            background: white;
            box-shadow: 2px 0 8px rgba(0,0,0,0.06);
            padding: 1.5rem 0;
            flex-shrink: 0;
            position: sticky;
            top: 70px;
            height: calc(100vh - 70px);
            overflow-y: auto;
        }
        .sidebar-label {
            padding: 0 1.5rem;
            font-size: 0.7rem; font-weight: 700;
            text-transform: uppercase; letter-spacing: 1px;
            color: #999; margin-bottom: 0.8rem;
        }
        .nav-item {
            display: flex; align-items: center; gap: 0.8rem;
            padding: 0.8rem 1.5rem;
            color: #555; font-weight: 500; font-size: 0.95rem;
            cursor: pointer; transition: all 0.2s;
            border-left: 3px solid transparent;
        }
        .nav-item:hover { background: #f5fafa; color: #0097a7; }
        .nav-item.active {
            background: #e0f7fa; color: #0097a7;
            border-left-color: #0097a7; font-weight: 600;
        }
        .nav-icon { font-size: 1.2rem; width: 24px; text-align: center; }
        .nav-badge {
            margin-left: auto;
            background: #0097a7; color: white;
            font-size: 0.7rem; padding: 0.15rem 0.5rem;
            border-radius: 10px; font-weight: 600;
        }

        @media (max-width: 768px) {
            .sidebar { width: 60px; }
            .nav-item span:not(.nav-icon) { display: none; }
            .nav-badge { display: none; }
            .sidebar-label { display: none; }
            .nav-item { justify-content: center; padding: 0.8rem; }
        }

        /* ---- MAIN CONTENT ---- */
        .main-content { flex: 1; padding: 2rem; overflow-y: auto; }
        .page-section { display: none; }
        .page-section.active { display: block; }
        .container { max-width: 1100px; margin: 0 auto; }

        .card {
            background: white; border-radius: 12px;
            padding: 2rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
        }

        /* ---- FORM ---- */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1.25rem; margin-bottom: 1.25rem;
        }
        @media (max-width: 900px) { .form-grid { grid-template-columns: 1fr 1fr; } }
        @media (max-width: 600px) { .form-grid { grid-template-columns: 1fr; } }

        .form-group { display: flex; flex-direction: column; }
        .form-group.full-width { grid-column: 1 / -1; }

        label { font-weight: 600; margin-bottom: 0.4rem; color: #1a2740; font-size: 0.9rem; }

        input[type="text"], input[type="number"], select {
            padding: 0.7rem 0.9rem;
            border: 1.5px solid #dde1e6; border-radius: 8px;
            font-size: 0.95rem; font-family: inherit;
            transition: border-color 0.25s, box-shadow 0.25s;
            background: #fafbfc;
        }
        input:focus, select:focus {
            outline: none; border-color: #0097a7;
            box-shadow: 0 0 0 3px rgba(0,151,167,0.12); background: white;
        }

        .button-group { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1.5rem; }

        button {
            padding: 0.7rem 1.5rem; font-size: 0.95rem; font-weight: 600;
            border: none; border-radius: 8px; cursor: pointer;
            transition: all 0.25s;
        }
        .btn-search { background: linear-gradient(135deg, #0097a7, #00838f); color: white; }
        .btn-search:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,151,167,0.35); }
        .btn-reset { background: #f0f0f0; color: #555; }
        .btn-reset:hover { background: #e0e0e0; }

        /* ---- RESULTS ---- */
        .results-section { display: none; }
        .results-section.show { display: block; }
        .results-info {
            background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
            border-left: 4px solid #4caf50;
            padding: 1rem 1.25rem; margin-bottom: 1.5rem; border-radius: 8px;
        }
        .results-info h3 { color: #2e7d32; margin-bottom: 0.3rem; }
        .results-info p { color: #556b2f; font-size: 0.9rem; }
        .tags { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
        .tag {
            background: #e0f2f1; color: #00796b;
            padding: 0.2rem 0.7rem; border-radius: 20px;
            font-size: 0.82rem; font-weight: 500;
        }

        /* ---- SAMPLE CARDS ---- */
        .samples-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
            gap: 1.5rem;
        }
        .sample-card {
            background: white; border-radius: 12px; overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            transition: transform 0.25s, box-shadow 0.25s;
            position: relative; cursor: pointer;
        }
        .sample-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.14);
        }
        .sample-card-img {
            width: 100%; height: 200px;
            object-fit: cover; display: block; background: #eee;
        }
        .sample-card-body { padding: 1rem 1.1rem 1.1rem; }
        .sample-card-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 0.6rem;
        }
        .sample-card-no { font-weight: 700; font-size: 1rem; color: #0097a7; }
        .sample-card-article { font-size: 0.82rem; color: #888; font-weight: 500; }
        .sample-card-props {
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 0.3rem 0.8rem;
        }
        .sample-prop { font-size: 0.8rem; }
        .sample-prop-label {
            color: #999; font-weight: 600;
            text-transform: uppercase; font-size: 0.68rem; letter-spacing: 0.5px;
        }
        .sample-prop-value { color: #333; font-weight: 500; }

        /* ---- RANK BADGE ---- */
        .rank-badge {
            position: absolute; top: 10px; left: 10px;
            padding: 0.25rem 0.6rem; border-radius: 8px;
            font-weight: 700; font-size: 0.78rem; z-index: 2;
            backdrop-filter: blur(4px);
        }
        .rank-top { background: rgba(76,175,80,0.92); color: white; }
        .rank-mid { background: rgba(255,152,0,0.92); color: white; }
        .rank-normal { background: rgba(255,255,255,0.9); color: #555; }
        .rank-label {
            position: absolute; top: 38px; left: 10px;
            font-size: 0.62rem; color: white;
            background: rgba(0,0,0,0.45);
            padding: 0.1rem 0.45rem; border-radius: 4px; z-index: 2;
        }

        /* ---- PAGE HEADER ---- */
        .page-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;
        }
        .page-header h2 { color: #1a2740; font-size: 1.4rem; }
        .count-badge {
            background: #e3f2fd; color: #1565c0;
            padding: 0.35rem 1rem; border-radius: 20px;
            font-weight: 600; font-size: 0.85rem;
        }

        /* ---- EMPTY STATE ---- */
        .empty-state { text-align: center; padding: 4rem 2rem; color: #999; }
        .empty-state .empty-icon { font-size: 3rem; margin-bottom: 1rem; }
        .empty-state p { font-size: 1.1rem; font-weight: 500; }
        .empty-state .sub { font-size: 0.9rem; margin-top: 0.5rem; font-weight: 400; }

        /* ---- LOADING ---- */
        .loading { display: none; text-align: center; padding: 3rem; color: #0097a7; }
        .loading.show { display: block; }
        .spinner {
            border: 3px solid #e0e0e0; border-top: 3px solid #0097a7;
            border-radius: 50%; width: 36px; height: 36px;
            animation: spin 0.8s linear infinite; margin: 0 auto 1rem;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .no-results { text-align: center; padding: 3rem 1rem; color: #999; }
        .no-results p { font-size: 1.1rem; font-weight: 500; }

        .error-message {
            background: #ffebee; border-left: 4px solid #f44336;
            padding: 1rem; margin-bottom: 1.5rem; border-radius: 8px;
            color: #c62828; display: none;
        }
        .error-message.show { display: block; }

        /* ---- WISHLIST GROUPS ---- */
        .group-bar {
            display: flex; gap: 0.8rem; align-items: center;
            margin-bottom: 1.5rem; flex-wrap: wrap;
        }
        .group-chip {
            padding: 0.5rem 1.2rem;
            border-radius: 20px; font-size: 0.9rem; font-weight: 600;
            cursor: pointer; border: 2px solid #dde1e6;
            background: white; color: #555; transition: all 0.25s;
            display: flex; align-items: center; gap: 0.4rem;
        }
        .group-chip:hover { border-color: #0097a7; color: #0097a7; }
        .group-chip.active { background: #0097a7; color: white; border-color: #0097a7; }
        .group-chip .delete-group {
            font-size: 0.8rem; margin-left: 0.3rem; opacity: 0.6;
            cursor: pointer;
        }
        .group-chip .delete-group:hover { opacity: 1; }
        .add-group-btn {
            padding: 0.5rem 1rem; border-radius: 20px;
            font-size: 0.85rem; font-weight: 600;
            cursor: pointer; border: 2px dashed #bbb;
            background: transparent; color: #888;
            transition: all 0.25s;
        }
        .add-group-btn:hover { border-color: #0097a7; color: #0097a7; }

        /* ---- MODAL ---- */
        .modal-overlay {
            display: none;
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); z-index: 500;
            align-items: center; justify-content: center;
            backdrop-filter: blur(4px);
        }
        .modal-overlay.show { display: flex; }

        .modal-box {
            background: white; border-radius: 16px;
            max-width: 700px; width: 90%; max-height: 90vh;
            overflow-y: auto; box-shadow: 0 24px 80px rgba(0,0,0,0.3);
            position: relative;
        }
        .modal-close {
            position: absolute; top: 12px; right: 16px;
            background: rgba(0,0,0,0.5); color: white;
            border: none; border-radius: 50%; width: 36px; height: 36px;
            font-size: 1.3rem; cursor: pointer; z-index: 510;
            display: flex; align-items: center; justify-content: center;
            transition: background 0.2s;
        }
        .modal-close:hover { background: rgba(0,0,0,0.8); }
        .modal-img {
            width: 100%; height: 350px;
            object-fit: cover; display: block; border-radius: 16px 16px 0 0;
        }
        .modal-body { padding: 1.5rem 2rem 2rem; }
        .modal-title {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 1.2rem;
        }
        .modal-title h2 { color: #0097a7; font-size: 1.3rem; }
        .modal-title span { color: #888; font-size: 0.9rem; font-weight: 500; }
        .modal-props {
            display: grid; grid-template-columns: 1fr 1fr 1fr;
            gap: 1rem; margin-bottom: 1.5rem;
        }
        @media (max-width: 500px) { .modal-props { grid-template-columns: 1fr 1fr; } }
        .modal-prop { }
        .modal-prop-label {
            color: #999; font-weight: 700;
            text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.5px;
        }
        .modal-prop-value { color: #333; font-weight: 600; font-size: 1rem; }
        .modal-wishlist-bar {
            display: flex; gap: 0.8rem; align-items: center;
            padding-top: 1rem; border-top: 1px solid #eee;
        }
        .modal-wishlist-bar select {
            flex: 1; padding: 0.7rem 0.9rem;
            border: 1.5px solid #dde1e6; border-radius: 8px;
            font-size: 0.95rem; font-family: inherit;
            background: #fafbfc;
        }
        .modal-wishlist-bar select:focus {
            outline: none; border-color: #0097a7;
        }
        .btn-add-wish {
            padding: 0.7rem 1.5rem;
            background: linear-gradient(135deg, #ff5252, #f44336);
            color: white; border: none; border-radius: 8px;
            font-size: 0.9rem; font-weight: 600; cursor: pointer;
            white-space: nowrap; transition: all 0.25s;
        }
        .btn-add-wish:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(244,67,54,0.35); }
        .modal-msg {
            margin-top: 0.7rem; font-size: 0.85rem; color: #4caf50;
            font-weight: 500; display: none;
        }
        .modal-msg.show { display: block; }

        /* ---- NEW GROUP MODAL ---- */
        .group-modal-overlay {
            display: none;
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5); z-index: 600;
            align-items: center; justify-content: center;
        }
        .group-modal-overlay.show { display: flex; }
        .group-modal-box {
            background: white; border-radius: 14px;
            padding: 2rem; width: 90%; max-width: 400px;
            box-shadow: 0 16px 48px rgba(0,0,0,0.25);
        }
        .group-modal-box h3 { color: #1a2740; margin-bottom: 1rem; }
        .group-modal-box input {
            width: 100%; padding: 0.8rem 1rem;
            border: 1.5px solid #dde1e6; border-radius: 10px;
            font-size: 1rem; font-family: inherit; margin-bottom: 1rem;
        }
        .group-modal-box input:focus {
            outline: none; border-color: #0097a7;
            box-shadow: 0 0 0 3px rgba(0,151,167,0.12);
        }
        .group-modal-actions { display: flex; gap: 0.8rem; justify-content: flex-end; }
        .group-modal-actions button { padding: 0.6rem 1.3rem; border-radius: 8px; font-size: 0.9rem; font-weight: 600; }
        .btn-cancel-group { background: #f0f0f0; color: #555; border: none; cursor: pointer; }
        .btn-save-group { background: linear-gradient(135deg,#0097a7,#00838f); color: white; border: none; cursor: pointer; }
        .btn-save-group:hover { transform: translateY(-1px); }
    </style>
</head>
<body>
    <!-- ======= HEADER ======= -->
    <div class="header">
        <div class="header-left">
            <h1>Fabric Sample Tool</h1>
            <p>Dashboard</p>
        </div>
        <div class="header-right">
            <div class="header-user">
                <div class="header-avatar">{{ username[0]|upper }}</div>
                <span class="header-username">{{ username }}</span>
            </div>
            <a href="/logout" class="btn-logout">Sign Out</a>
        </div>
    </div>

    <div class="app-layout">
        <!-- ======= SIDEBAR ======= -->
        <div class="sidebar">
            <div class="sidebar-label">Menu</div>
            <div class="nav-item active" onclick="switchPage('search', this)">
                <span class="nav-icon">&#128269;</span>
                <span>Search</span>
            </div>
            <div class="nav-item" onclick="switchPage('wishlist', this)">
                <span class="nav-icon">&#10084;</span>
                <span>Wishlist</span>
                <span class="nav-badge" id="wishlistBadge">0</span>
            </div>
            <div class="nav-item" onclick="switchPage('data', this)">
                <span class="nav-icon">&#128202;</span>
                <span>Data</span>
            </div>
        </div>

        <!-- ======= MAIN CONTENT ======= -->
        <div class="main-content">

            <!-- ---- SEARCH PAGE ---- -->
            <div id="page-search" class="page-section active">
                <div class="container">
                    <div class="card">
                        <h2 style="margin-bottom: 1.5rem; color: #1a2740;">Search Fabric Samples</h2>
                        <form id="searchForm">
                            <div class="form-grid">
                                <div class="form-group">
                                    <label for="product_type">Product Type</label>
                                    <select id="product_type" name="product_type">
                                        <option value="ALL">All Products</option>
                                        <option value="DYED">DYED</option>
                                        <option value="PRINT">PRINT</option>
                                        <option value="CHECKS">CHECKS</option>
                                        <option value="STRIPES">STRIPES</option>
                                        <option value="WHITE">WHITE</option>
                                        <option value="YD+PRINT">YD+PRINT</option>
                                        <option value="WHITE+PRINT">WHITE+PRINT</option>
                                        <option value="DYED+PRINT">DYED+PRINT</option>
                                        <option value="YD+PIGMENT PRINT">YD+PIGMENT PRINT</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="weave">Weave</label>
                                    <select id="weave" name="weave">
                                        <option value="ALL">All Weaves</option>
                                        <option value="PLAIN">PLAIN</option>
                                        <option value="TWILL">TWILL</option>
                                        <option value="DOBBY">DOBBY</option>
                                        <option value="SATIN">SATIN</option>
                                        <option value="HBT">HBT</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="yarn">Yarn Type</label>
                                    <select id="yarn" name="yarn">
                                        <option value="ALL">All Yarn Types</option>
                                        <option value="COMPACT">COMPACT</option>
                                        <option value="COMBED">COMBED</option>
                                        <option value="SLUB">SLUB</option>
                                        <option value="TFO">TFO</option>
                                        <option value="CARDED">CARDED</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="blend">Composition/Blend</label>
                                    <input type="text" id="blend" name="blend" placeholder="e.g., cotton, modal, viscose">
                                </div>
                                <div class="form-group">
                                    <label for="gsm_min">GSM Min</label>
                                    <input type="number" id="gsm_min" name="gsm_min" placeholder="e.g., 100" min="0">
                                </div>
                                <div class="form-group">
                                    <label for="gsm_max">GSM Max</label>
                                    <input type="number" id="gsm_max" name="gsm_max" placeholder="e.g., 200" min="0">
                                </div>
                                <div class="form-group full-width">
                                    <label for="feel_terms">Performance / Feel Terms</label>
                                    <input type="text" id="feel_terms" name="feel_terms" placeholder="e.g., soft feel, shiny, stretchable">
                                </div>
                            </div>
                            <div class="button-group">
                                <button type="reset" class="btn-reset">Clear</button>
                                <button type="submit" class="btn-search">Search Samples</button>
                            </div>
                        </form>
                    </div>

                    <div class="loading" id="loading">
                        <div class="spinner"></div><p>Searching samples...</p>
                    </div>
                    <div class="error-message" id="errorMessage"></div>

                    <div class="results-section" id="resultsSection">
                        <div class="results-info">
                            <h3><span id="resultCount">0</span> samples found</h3>
                            <div id="termsDisplay"></div>
                        </div>
                        <div class="samples-grid" id="resultsContent"></div>
                    </div>
                </div>
            </div>

            <!-- ---- WISHLIST PAGE ---- -->
            <div id="page-wishlist" class="page-section">
                <div class="container">
                    <div class="page-header">
                        <h2>My Wishlist</h2>
                        <span class="count-badge" id="wishlistCount">0 samples</span>
                    </div>
                    <div class="group-bar" id="groupBar">
                        <!-- group chips rendered by JS -->
                    </div>
                    <div id="wishlistContent">
                        <div class="empty-state">
                            <div class="empty-icon">&#10084;</div>
                            <p>Your wishlist is empty</p>
                            <p class="sub">Create a group, then click on any sample to add it</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ---- DATA PAGE ---- -->
            <div id="page-data" class="page-section">
                <div class="container">
                    <div class="page-header">
                        <h2>All Fabric Samples</h2>
                        <span class="count-badge" id="dataCount">Loading...</span>
                    </div>
                    <div class="loading show" id="dataLoading">
                        <div class="spinner"></div><p>Loading all samples...</p>
                    </div>
                    <div class="samples-grid" id="dataGrid"></div>
                </div>
            </div>

        </div>
    </div>

    <!-- ======= SAMPLE DETAIL MODAL ======= -->
    <div class="modal-overlay" id="sampleModal">
        <div class="modal-box">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <img class="modal-img" id="modalImg" src="" alt="">
            <div class="modal-body">
                <div class="modal-title">
                    <h2 id="modalSampleNo"></h2>
                    <span id="modalArticle"></span>
                </div>
                <div class="modal-props" id="modalProps"></div>
                <div class="modal-wishlist-bar">
                    <select id="modalGroupSelect">
                        <option value="">-- Select Wishlist Group --</option>
                    </select>
                    <button class="btn-add-wish" onclick="addFromModal()">Add to Wishlist</button>
                </div>
                <div class="modal-msg" id="modalMsg">Added to wishlist!</div>
            </div>
        </div>
    </div>

    <!-- ======= NEW GROUP MODAL ======= -->
    <div class="group-modal-overlay" id="groupModal">
        <div class="group-modal-box">
            <h3>Create Wishlist Group</h3>
            <input type="text" id="groupNameInput" placeholder="e.g.,  Arvind, Aditya Birla....">
            <div class="group-modal-actions">
                <button class="btn-cancel-group" onclick="closeGroupModal()">Cancel</button>
                <button class="btn-save-group" onclick="saveNewGroup()">Create</button>
            </div>
        </div>
    </div>

    <script>
        let allGroups = [];       // [{id, name}]
        let wishlistData = null;  // full wishlist response
        let activeGroupId = null; // currently viewed group in wishlist tab
        let allSamplesCache = []; // for detail modal

        /* ---- PAGE SWITCHING ---- */
        function switchPage(page, el) {
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelectorAll('.page-section').forEach(p => p.classList.remove('active'));
            document.getElementById('page-' + page).classList.add('active');
            if (el) el.classList.add('active');
            if (page === 'data' && !window._dataLoaded) loadAllSamples();
            if (page === 'wishlist') loadWishlist();
        }

        /* ---- CARD BUILDER ---- */
        function buildSampleCard(sample, rankInfo) {
            let html = '<div class="sample-card" id="card-' + sample.sample_no + '" onclick="openModal(' + sample.sample_no + ')">';
            if (rankInfo) {
                html += '<span class="rank-badge ' + rankInfo.cls + '">#' + rankInfo.rank + '</span>';
                html += '<span class="rank-label">' + rankInfo.label + '</span>';
            }
            html += '<img class="sample-card-img" src="/sample-image/' + sample.sample_no + '" alt="Sample ' + sample.sample_no + '" onerror="this.style.background=\'#ddd\';this.style.height=\'140px\'">';
            html += '<div class="sample-card-body">';
            html += '<div class="sample-card-header">';
            html += '<span class="sample-card-no">' + sample.sample_no + '</span>';
            html += '<span class="sample-card-article">' + sample.article + '</span>';
            html += '</div>';
            html += '<div class="sample-card-props">';
            html += prop('Product', sample.product);
            html += prop('Yarn', sample.yarn);
            html += prop('Count', sample.count);
            html += prop('GSM', sample.gsm);
            html += prop('Blend', sample.blend);
            html += prop('Weave', sample.weave);
            html += prop('Finish', sample.finish);
            html += '</div></div></div>';
            return html;
        }

        function prop(label, value) {
            return '<div class="sample-prop"><div class="sample-prop-label">' + label + '</div><div class="sample-prop-value">' + value + '</div></div>';
        }

        /* ============ SAMPLE DETAIL MODAL ============ */
        function openModal(sampleNo) {
            const sample = findSample(sampleNo);
            if (!sample) return;
            document.getElementById('modalImg').src = '/sample-image/' + sample.sample_no;
            document.getElementById('modalSampleNo').textContent = 'Sample ' + sample.sample_no;
            document.getElementById('modalArticle').textContent = sample.article;
            const props = [
                ['Product', sample.product], ['Yarn', sample.yarn], ['Count', sample.count],
                ['Construction', sample.construction || '-'], ['Blend', sample.blend], ['Weave', sample.weave],
                ['Finish', sample.finish], ['GSM', sample.gsm], ['Count Avg', sample.count_avg || '-']
            ];
            let ph = '';
            props.forEach(function(p) {
                ph += '<div class="modal-prop"><div class="modal-prop-label">' + p[0] + '</div><div class="modal-prop-value">' + p[1] + '</div></div>';
            });
            document.getElementById('modalProps').innerHTML = ph;
            // populate group dropdown
            refreshGroupDropdown();
            document.getElementById('modalMsg').classList.remove('show');
            document.getElementById('sampleModal').dataset.sampleNo = sampleNo;
            document.getElementById('sampleModal').classList.add('show');
        }

        function closeModal() {
            document.getElementById('sampleModal').classList.remove('show');
        }

        function refreshGroupDropdown() {
            const sel = document.getElementById('modalGroupSelect');
            sel.innerHTML = '<option value="">-- Select Wishlist Group --</option>';
            allGroups.forEach(function(g) {
                sel.innerHTML += '<option value="' + g.id + '">' + g.name + '</option>';
            });
        }

        async function addFromModal() {
            const groupId = document.getElementById('modalGroupSelect').value;
            const sampleNo = document.getElementById('sampleModal').dataset.sampleNo;
            if (!groupId) { alert('Please select a wishlist group first'); return; }
            await fetch('/api/wishlist/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sample_no: parseInt(sampleNo), group_id: parseInt(groupId)})
            });
            const msg = document.getElementById('modalMsg');
            const groupName = allGroups.find(g => g.id == groupId).name;
            msg.textContent = 'Added to "' + groupName + '" wishlist!';
            msg.classList.add('show');
            setTimeout(function(){ msg.classList.remove('show'); }, 2000);
            loadWishlistBadge();
        }

        // click outside modal to close
        document.getElementById('sampleModal').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        function findSample(sampleNo) {
            if (allSamplesCache.length > 0) {
                const found = allSamplesCache.find(s => s.sample_no == sampleNo);
                if (found) return found;
            }
            // try search results
            const cards = document.querySelectorAll('.sample-card');
            // fallback: fetch sync is not ideal, but we cache on first data/search load
            return null;
        }

        /* ============ WISHLIST GROUPS ============ */
        function openGroupModal() {
            document.getElementById('groupNameInput').value = '';
            document.getElementById('groupModal').classList.add('show');
        }
        function closeGroupModal() {
            document.getElementById('groupModal').classList.remove('show');
        }

        async function saveNewGroup() {
            const name = document.getElementById('groupNameInput').value.trim();
            if (!name) return;
            const res = await fetch('/api/wishlist/groups/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name})
            });
            const data = await res.json();
            if (data.error) { alert(data.error); return; }
            closeGroupModal();
            await loadGroupsList();
            loadWishlist();
        }

        async function deleteGroup(groupId, e) {
            e.stopPropagation();
            if (!confirm('Delete this group and all its items?')) return;
            await fetch('/api/wishlist/groups/delete', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({group_id: groupId})
            });
            await loadGroupsList();
            activeGroupId = null;
            loadWishlist();
        }

        async function loadGroupsList() {
            const res = await fetch('/api/wishlist/groups');
            const data = await res.json();
            allGroups = data.groups;
        }

        function renderGroupBar(groups, activeId) {
            const bar = document.getElementById('groupBar');
            let html = '';
            groups.forEach(function(g) {
                const cls = g.id === activeId ? 'group-chip active' : 'group-chip';
                html += '<div class="' + cls + '" onclick="selectGroup(' + g.id + ')">';
                html += '<span>' + g.name + '</span>';
                html += '<span class="delete-group" onclick="deleteGroup(' + g.id + ', event)" title="Delete group">&times;</span>';
                html += '</div>';
            });
            html += '<button class="add-group-btn" onclick="openGroupModal()">+ New Group</button>';
            bar.innerHTML = html;
        }

        function selectGroup(groupId) {
            activeGroupId = groupId;
            renderWishlistContent();
        }

        async function loadWishlist() {
            await loadGroupsList();
            const res = await fetch('/api/wishlist');
            wishlistData = await res.json();
            // cache samples
            wishlistData.groups.forEach(function(g) {
                g.samples.forEach(function(s) {
                    if (!allSamplesCache.find(x => x.sample_no === s.sample_no)) allSamplesCache.push(s);
                });
            });
            updateWishlistBadge();
            document.getElementById('wishlistCount').textContent = wishlistData.total_count + ' samples';
            if (allGroups.length > 0 && !activeGroupId) activeGroupId = allGroups[0].id;
            renderGroupBar(allGroups, activeGroupId);
            renderWishlistContent();
        }

        function renderWishlistContent() {
            renderGroupBar(allGroups, activeGroupId);
            const container = document.getElementById('wishlistContent');
            if (!wishlistData || allGroups.length === 0) {
                container.innerHTML = '<div class="empty-state"><div class="empty-icon">&#10084;</div><p>No groups yet</p><p class="sub">Click "+ New Group" to create a wishlist group</p></div>';
                return;
            }
            const grp = wishlistData.groups.find(g => g.group_id === activeGroupId);
            if (!grp || grp.samples.length === 0) {
                container.innerHTML = '<div class="empty-state"><div class="empty-icon">&#128203;</div><p>This group is empty</p><p class="sub">Click on any sample card to add it here</p></div>';
                return;
            }
            let html = '<div class="samples-grid">';
            grp.samples.forEach(function(s) {
                html += buildSampleCard(s, null);
                // add remove button overlay
                html = html.slice(0, -6); // remove last </div>
                html += '<div style="padding:0.5rem 1.1rem 1rem;text-align:right;">';
                html += '<button style="padding:0.4rem 1rem;border-radius:6px;border:1.5px solid #ef5350;background:white;color:#ef5350;font-weight:600;font-size:0.8rem;cursor:pointer;" onclick="event.stopPropagation();removeFromGroup(' + s.sample_no + ',' + activeGroupId + ')">Remove</button>';
                html += '</div></div>';
            });
            html += '</div>';
            container.innerHTML = html;
        }

        async function removeFromGroup(sampleNo, groupId) {
            await fetch('/api/wishlist/remove', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sample_no: sampleNo, group_id: groupId})
            });
            loadWishlist();
        }

        function updateWishlistBadge() {
            const cnt = wishlistData ? wishlistData.total_count : 0;
            document.getElementById('wishlistBadge').textContent = cnt;
        }

        async function loadWishlistBadge() {
            const res = await fetch('/api/wishlist');
            wishlistData = await res.json();
            updateWishlistBadge();
        }
        loadWishlistBadge();
        loadGroupsList();

        /* ============ SEARCH ============ */
        document.getElementById("searchForm").addEventListener("submit", async function(e) {
            e.preventDefault();
            const loading = document.getElementById("loading");
            const resultsSection = document.getElementById("resultsSection");
            const errorMessage = document.getElementById("errorMessage");
            loading.classList.add("show");
            resultsSection.classList.remove("show");
            errorMessage.classList.remove("show");
            try {
                const response = await fetch("/search", { method: "POST", body: new FormData(this) });
                const data = await response.json();
                loading.classList.remove("show");
                // cache for modal
                data.results.forEach(function(s) {
                    if (!allSamplesCache.find(x => x.sample_no === s.sample_no)) allSamplesCache.push(s);
                });
                displayResults(data);
                resultsSection.classList.add("show");
            } catch (error) {
                loading.classList.remove("show");
                errorMessage.textContent = "Error performing search. Please try again.";
                errorMessage.classList.add("show");
            }
        });

        function displayResults(data) {
            document.getElementById("resultCount").textContent = data.total_count;
            const termsDisplay = document.getElementById("termsDisplay");
            const resultsContent = document.getElementById("resultsContent");
            if (data.standard_terms.length > 0) {
                const tags = data.standard_terms.map(t => '<span class="tag">' + t + '</span>').join("");
                termsDisplay.innerHTML = '<p style="margin-top:0.5rem;font-weight:500;">Detected Properties:</p><div class="tags">' + tags + '</div>' +
                    '<p style="margin-top:0.5rem;font-size:0.88rem;color:#556b2f;">Sorted by best match — top recommendations first</p>';
            } else { termsDisplay.innerHTML = ""; }
            if (data.results.length === 0) {
                resultsContent.innerHTML = '<div class="no-results" style="grid-column:1/-1;"><p>No samples matched your requirements.</p></div>';
                return;
            }
            const hasRank = data.standard_terms.length > 0;
            let html = '';
            data.results.forEach(function(sample, index) {
                let rankInfo = null;
                if (hasRank) {
                    const rank = sample.rank || (index + 1);
                    let cls = 'rank-normal', label = 'Match';
                    if (rank === 1) { cls = 'rank-top'; label = 'Best Match'; }
                    else if (rank <= 3) { cls = 'rank-top'; label = 'Top Pick'; }
                    else if (rank <= Math.ceil(data.total_count * 0.4)) { cls = 'rank-mid'; label = 'Good Match'; }
                    rankInfo = { rank: rank, cls: cls, label: label };
                }
                html += buildSampleCard(sample, rankInfo);
            });
            resultsContent.innerHTML = html;
        }

        /* ============ DATA PAGE ============ */
        async function loadAllSamples() {
            try {
                const response = await fetch("/api/samples");
                const data = await response.json();
                document.getElementById("dataLoading").classList.remove("show");
                document.getElementById("dataCount").textContent = data.total_count + " samples";
                allSamplesCache = data.samples;
                let html = '';
                data.samples.forEach(function(sample) { html += buildSampleCard(sample, null); });
                document.getElementById("dataGrid").innerHTML = html;
                window._dataLoaded = true;
            } catch (error) {
                document.getElementById("dataLoading").innerHTML = '<p style="color:#c62828;">Failed to load samples.</p>';
            }
        }
    </script>
</body>
</html>
"""

seed_database()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
