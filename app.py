import re
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ============================================================================
# SAMPLES DATABASE
# ============================================================================
SAMPLES = [
    {"sample_no": 1001, "article": "Decent", "product": "YD + PRINT", "yarn": "COMBED", "count": "30*30", "count_avg": 30, "construction": "088*072", "construction_total": 160, "blend": "100% COTTON", "weave": "TWILL", "finish": "SOFT TOUCH", "gsm": 132},
    {"sample_no": 1002, "article": "HBS DOT PRINT", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "110*070", "construction_total": 180, "blend": "100% COTTON", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 113},
    {"sample_no": 1003, "article": "BELLE MEADE", "product": "DYED", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "140*076", "construction_total": 216, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "CSF", "gsm": 135},
    {"sample_no": 1004, "article": "GLENDALE", "product": "WHITE + PRINT", "yarn": "COMPACT", "count": "50*50", "count_avg": 50, "construction": "132*084", "construction_total": 216, "blend": "100% COTTON", "weave": "DOBBY", "finish": "SOFT TOUCH", "gsm": 109},
    {"sample_no": 1005, "article": "NAVY PEACOAT", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "104*072", "construction_total": 176, "blend": "100% COTTON", "weave": "PLAIN", "finish": "PFH", "gsm": 111},
    {"sample_no": 1006, "article": "MSHR84 CHAVAL", "product": "WHITE + PRINT", "yarn": "CARDED", "count": "40*40", "count_avg": 40, "construction": "104*072", "construction_total": 176, "blend": "100% COTTON", "weave": "PLAIN", "finish": "CSF", "gsm": 111},
    {"sample_no": 1007, "article": "GARY", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "21*21", "count_avg": 21, "construction": "054*048", "construction_total": 102, "blend": "COTTON:LINEN", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 122},
    {"sample_no": 1008, "article": "BELLE MEADE", "product": "DYED", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "140*076", "construction_total": 216, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "CSF", "gsm": 135},
    {"sample_no": 1009, "article": "24P5 BL", "product": "WHITE + PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "148*106", "construction_total": 254, "blend": "100% COTTON", "weave": "PLAIN", "finish": "SFT", "gsm": 106},
    {"sample_no": 1010, "article": "f323 091", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "50*50", "count_avg": 50, "construction": "130*084", "construction_total": 214, "blend": "COTTON:LYCRA", "weave": "TWILL", "finish": "SFT", "gsm": 108},
    {"sample_no": 1011, "article": "ALMETA", "product": "WHITE + PRINT", "yarn": "COMPACT YARN", "count": "40*40", "count_avg": 40, "construction": "116*080", "construction_total": 196, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "PFH", "gsm": 123},
    {"sample_no": 1012, "article": "LUMBERTON", "product": "CHECKS", "yarn": "SLUB", "count": "40*30", "count_avg": 35, "construction": "080*054", "construction_total": 134, "blend": "100% COTTON", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 119},
    {"sample_no": 1013, "article": "A37900DA", "product": "CHECKS", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "094*080", "construction_total": 174, "blend": "100% COTTON", "weave": "DOBBY", "finish": "ETI+SOFT TOUCH", "gsm": 144},
    {"sample_no": 1014, "article": "A37055PA", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "128*066", "construction_total": 194, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "PFH", "gsm": 121},
    {"sample_no": 1015, "article": "SANGARIA BASE", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "50*60", "count_avg": 55, "construction": "144*104", "construction_total": 248, "blend": "COTTON:MODAL", "weave": "TWILL", "finish": "ETI", "gsm": 118},
    {"sample_no": 1016, "article": "AG-2220", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "132*072", "construction_total": 204, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "SOFT TOUCH", "gsm": 123},
    {"sample_no": 1017, "article": "61606V", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "116*080", "construction_total": 196, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "PFH", "gsm": 123},
    {"sample_no": 1018, "article": "AW24-DBCH", "product": "DYED", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "195*104", "construction_total": 299, "blend": "100% COTTON", "weave": "DOBBY-SATIN", "finish": "CSF", "gsm": 123},
    {"sample_no": 1019, "article": "AW24-WBST", "product": "DYED + PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "104*072", "construction_total": 176, "blend": "100%VISCOSE", "weave": "TWILL", "finish": "SFT", "gsm": 147},
    {"sample_no": 1020, "article": "CRECK", "product": "PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "104*072", "construction_total": 176, "blend": "100%VISCOSE", "weave": "TWILL", "finish": "SFT", "gsm": 147},
    {"sample_no": 1021, "article": "BARBOUR", "product": "CHECKS", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "064*054", "construction_total": 118, "blend": "COTTON:TENCEL", "weave": "TWILL", "finish": "BRUSHED", "gsm": 196},
    {"sample_no": 1022, "article": "MOUNTAIN - E", "product": "DYED", "yarn": "TFO", "count": "60*30", "count_avg": 45, "construction": "200*128", "construction_total": 328, "blend": "COTTON:LYCRA", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 273},
    {"sample_no": 1023, "article": "A29600PC", "product": "DYED", "yarn": "TFO", "count": "20*20", "count_avg": 20, "construction": "064*054", "construction_total": 118, "blend": "100% COTTON", "weave": "TWILL", "finish": "NORMAL SOFT FIN", "gsm": 294},
    {"sample_no": 1024, "article": "A37864PB", "product": "YD+PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "138*096", "construction_total": 234, "blend": "100% COTTON", "weave": "TWILL", "finish": "NORMAL SOFT FIN", "gsm": 97},
    {"sample_no": 1025, "article": "A37342PA", "product": "YD+PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "062*056", "construction_total": 118, "blend": "100% VISCOSE", "weave": "TWILL", "finish": "BRUSHED", "gsm": 147},
    {"sample_no": 1026, "article": "COTTON VISCOSE PRI", "product": "DYED +PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "180*104", "construction_total": 284, "blend": "COTTON:MODAL", "weave": "SATIN", "finish": "ETI+CALENDER", "gsm": 118},
    {"sample_no": 1027, "article": "BLUE SNOW FLAKES", "product": "DYED +PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "110*076", "construction_total": 186, "blend": "COTTON:VISCOSE", "weave": "TWILL", "finish": "BRUSHED", "gsm": 117},
    {"sample_no": 1028, "article": "A37238RA", "product": "PRINT", "yarn": "COMPACT", "count": "30*30", "count_avg": 30, "construction": "096*060", "construction_total": 156, "blend": "COTTON:VISCOSE", "weave": "TWILL", "finish": "BRUSHED", "gsm": 131},
    {"sample_no": 1029, "article": "F326PJSH", "product": "PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "180*104", "construction_total": 284, "blend": "COTTON:MODAL", "weave": "SATIN", "finish": "ETI+CALENDER", "gsm": 118},
    {"sample_no": 1030, "article": "47F003G", "product": "STRIPES", "yarn": "SLUB", "count": "20*20", "count_avg": 20, "construction": "072*062", "construction_total": 134, "blend": "100% COTTON", "weave": "DOBBY", "finish": "NORMAL SOFT FIN", "gsm": 167},
    {"sample_no": 1031, "article": "62068", "product": "DYED", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "128*080", "construction_total": 208, "blend": "COTTON:LINEN", "weave": "PLAIN", "finish": "SFT", "gsm": 130},
    {"sample_no": 1032, "article": "HARLAN", "product": "WHITE+PRINT", "yarn": "COMPACT", "count": "50*50", "count_avg": 50, "construction": "144*092", "construction_total": 236, "blend": "100% COTTON", "weave": "DOBBY", "finish": "SOFT TOUCH", "gsm": 119},
    {"sample_no": 1033, "article": "MS12-375", "product": "YD+PRINT", "yarn": "COMPACT", "count": "40*30", "count_avg": 35, "construction": "120*066", "construction_total": 186, "blend": "100% COTTON", "weave": "TWILL", "finish": "CSF", "gsm": 131},
    {"sample_no": 1034, "article": "MFS-15346", "product": "DYED", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "194*104", "construction_total": 298, "blend": "100% COTTON", "weave": "DOBBY*SATIN", "finish": "SFT", "gsm": 124},
    {"sample_no": 1035, "article": "MFS_16730", "product": "PRINT", "yarn": "COMPACT", "count": "50*60", "count_avg": 55, "construction": "144*104", "construction_total": 248, "blend": "COTTON:MODAL", "weave": "COTTON:MODAL", "finish": "CSF", "gsm": 116},
    {"sample_no": 1036, "article": "MIDLAND", "product": "CHECKS", "yarn": "COMPACT", "count": "60*20", "count_avg": 40, "construction": "124*064", "construction_total": 188, "blend": "COTTON:LINEN", "weave": "COTTON:LINEN", "finish": "SOFT TOUCH", "gsm": 128},
    {"sample_no": 1037, "article": "A38235PA", "product": "PRINT", "yarn": "COMPACT", "count": "60*60", "count_avg": 60, "construction": "154*096", "construction_total": 250, "blend": "100%MODAL", "weave": "PLAIN", "finish": "NORMAL SOFT FIN", "gsm": 112},
    {"sample_no": 1038, "article": "A5680", "product": "DYED + PRINT", "yarn": "COMPACT*SLUB", "count": "50*30", "count_avg": 40, "construction": "104*088", "construction_total": 192, "blend": "100% COTTON", "weave": "TWILLHBT", "finish": "SOFT TOUCH", "gsm": 121},
    {"sample_no": 1039, "article": "MOUNTAIN-B", "product": "DYED", "yarn": "TFO", "count": "20*20", "count_avg": 20, "construction": "064*054", "construction_total": 118, "blend": "100% COTTON", "weave": "DOBBY", "finish": "NORMAL SOFT FIN", "gsm": 294},
    {"sample_no": 1040, "article": "YD+PIGMENT PRINT", "product": "YD+PIGMENT PRINT", "yarn": "COMPACT", "count": "40*40", "count_avg": 40, "construction": "104*088", "construction_total": 192, "blend": "COTTON:TENCEL", "weave": "TWILLHBT", "finish": "SOFT TOUCH", "gsm": 120},
]

# ============================================================================
# FEEL TERMS DICTIONARY
# ============================================================================
FEEL_DICTIONARY = {
    "Soft Feel": ["soft handfeel", "soft touch", "silky touch", "smooth feel", "peach finish", "soft fleece", "soft", "silky", "smooth", "peach"],
    "Premium Look": ["premium", "luxe", "luxury", "rich look", "high-end", "superior look"],
    "Shiny": ["high shine", "lustrous", "glossy", "sheen", "bright surface", "satin look", "shiny", "shine", "gloss", "lustre"],
    "Breathable": ["breathable", "airy", "ventilated", "summer friendly", "cool wearing", "cool", "breathe"],
    "Lightweight": ["lightweight", "light weight", "feather feel", "low weight", "ultra light", "light"],
    "Crisp look": ["crisp", "stiff", "paper touch", "structured feel", "firm hand", "firm"],
    "Textured": ["textured", "grainy", "slub look", "uneven surface", "raw texture", "texture", "slub"],
    "Drape": ["drapey", "drapy", "good fall", "flowy", "fluid", "elegant fall", "drape", "flow"],
    "Dense": ["durable", "strong", "long life", "sturdy", "dense", "thick", "heavy"],
    "Stretchable": ["stretchable", "stretch", "elastic", "lycra", "flex", "flexible", "spandex"],
    "Easy Care": ["easy care", "easy iron", "wrinkle free", "wrinkle resistant", "low maintenance", "wrinkle", "easy"],
}

# ============================================================================
# RULE TABLE
# ============================================================================
RULE_TABLE = {
    "Soft Feel": {
        "yarn": {"values": ["compact", "combed", "slub", "tfo"], "priority": "HIGH"},
        "count": {"min": 30, "priority": "HIGH"},
        "blend": {"values": ["cotton", "modal", "viscose", "tencel", "giza"], "priority": "HIGH"},
        "weave": {"values": ["plain", "dobby", "twill", "satin"], "priority": "LOW"},
        "finish": {"values": ["soft touch", "brushed", "peach finish", "normal soft fin", "csf", "sft", "pfh"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [
            {"blend": "100% cotton", "finish": ["anti microbial", "eti"]}
        ],
    },
    "Drape": {
        "yarn": {"values": ["combed", "compact", "tfo", "slub"], "priority": "HIGH"},
        "blend": {"values": ["viscose", "modal", "tencel", "cotton"], "priority": "HIGH"},
        "blend_exclude": ["100% cotton", "lycra"],
        "weave": {"values": ["dobby", "twill", "satin"], "priority": "HIGH"},
        "gsm": {"max": 170, "priority": "HIGH"},
        "yarn_exclude": ["carded"],
        "negative_cross": [],
    },
    "Shiny": {
        "yarn": {"values": ["compact", "tfo"], "priority": "HIGH"},
        "count": {"min": 30, "priority": "HIGH"},
        "blend": {"values": ["cotton", "modal", "viscose", "tencel", "giza"], "priority": "HIGH"},
        "blend_exclude": ["linen"],
        "weave": {"values": ["twill", "satin", "dobby"], "priority": "HIGH"},
        "finish": {"values": ["silky finish", "calendar", "calender", "eti"], "priority": "LOW"},
        "yarn_exclude": [],
        "negative_cross": [
            {"blend": "100% cotton", "weave": ["plain", "dobby"]}
        ],
    },
    "Crisp look": {
        "blend": {"values": ["linen"], "exact_values": ["100% cotton"], "priority": "HIGH"},
        "weave": {"values": ["plain"], "priority": "LOW"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Stretchable": {
        "blend": {"values": ["lycra", "viscose", "cotton viscose", "modal"], "priority": "HIGH"},
        "weave": {"values": ["plain", "dobby", "twill", "satin"], "priority": "LOW"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Easy Care": {
        "yarn": {"values": ["compact", "carded", "slub", "tfo", "combed"], "priority": "LOW"},
        "blend": {"values": ["viscose", "modal", "tencel", "cotton", "linen"], "priority": "LOW"},
        "weave": {"values": ["plain", "dobby", "twill", "satin"], "priority": "LOW"},
        "finish": {"values": ["eti", "resin", "csf"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Textured": {
        "combo_mode": True,
        "positive_combos": [
            # High positive (score 2)
            {"score": 2, "yarn": ["slub"], "weave": ["plain", "twill", "dobby", "satin", "hbt"]},
            {"score": 2, "yarn": ["carded"], "weave": ["dobby"]},
            {"score": 2, "blend": ["linen"], "weave": ["dobby", "plain", "twill"]},
            # Medium positive (score 1)
            {"score": 1, "yarn": ["carded"], "weave": ["plain", "twill"]},
            {"score": 1, "weave": ["dobby"]},
        ],
        "finish_bonus": ["brushed"],
    },
    "Dense": {
        "weave": {"values": ["twill", "matt", "plain"], "priority": "LOW"},
        "gsm": {"min": 170, "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Lightweight": {
        "gsm": {"max": 130, "priority": "HIGH"},
        "yarn": {"values": ["compact", "combed"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Breathable": {
        "blend": {"values": ["cotton", "linen", "tencel"], "priority": "HIGH"},
        "weave": {"values": ["plain"], "priority": "HIGH"},
        "gsm": {"max": 160, "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [],
    },
    "Premium Look": {
        "count": {"min": 30, "priority": "HIGH"},
        "blend": {"values": ["cotton", "modal", "viscose", "tencel", "giza"], "priority": "HIGH"},
        "finish": {"values": ["soft touch", "brushed", "calendar", "calender", "eti"], "priority": "HIGH"},
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

    # Check blend_exclude (always hard reject)
    if rule.get("blend_exclude"):
        if contains_any(sample["blend"], rule["blend_exclude"]):
            return False, 0

    # Check negative cross-attribute rules (always hard reject)
    for neg in rule.get("negative_cross", []):
        all_match = True
        for attr, condition in neg.items():
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
    results = list(SAMPLES)

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
        # Track cumulative LOW-priority scores per sample
        sample_scores = {s["sample_no"]: 0 for s in results}

        for standard_term in standard_terms:
            filtered = []
            for s in results:
                passes, score = check_sample_against_rule(s, standard_term)
                if passes:
                    sample_scores[s["sample_no"]] = sample_scores.get(s["sample_no"], 0) + score
                    filtered.append(s)
            results = filtered

        # Sort by score descending — samples matching more LOW-priority conditions first
        results.sort(key=lambda s: sample_scores.get(s["sample_no"], 0), reverse=True)

    if not has_filters:
        return [], standard_terms

    return results, standard_terms

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/search", methods=["POST"])
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

# ============================================================================
# HTML TEMPLATE
# ============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fabric Sample Selection Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }

        .header {
            background-color: #1a2740;
            color: white;
            padding: 2rem 1rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .container {
            max-width: 900px;
            margin: 2rem auto;
            padding: 0 1rem;
        }

        .card {
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        @media (max-width: 600px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #1a2740;
            font-size: 0.95rem;
        }

        input[type="text"],
        input[type="number"],
        select {
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
            font-family: inherit;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus,
        input[type="number"]:focus,
        select:focus {
            outline: none;
            border-color: #0097a7;
            box-shadow: 0 0 0 2px rgba(0, 151, 167, 0.1);
        }

        .button-group {
            display: flex;
            gap: 1rem;
            justify-content: flex-end;
            margin-top: 1.5rem;
        }

        button {
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-search {
            background-color: #0097a7;
            color: white;
        }

        .btn-search:hover {
            background-color: #00838f;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 151, 167, 0.3);
        }

        .btn-reset {
            background-color: #f0f0f0;
            color: #333;
        }

        .btn-reset:hover {
            background-color: #e0e0e0;
        }

        .results-section {
            display: none;
        }

        .results-section.show {
            display: block;
        }

        .results-info {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 4px;
        }

        .results-info h3 {
            color: #2e7d32;
            margin-bottom: 0.5rem;
        }

        .results-info p {
            color: #556b2f;
            font-size: 0.95rem;
        }

        .no-results {
            text-align: center;
            padding: 3rem 1rem;
            color: #999;
        }

        .no-results p {
            font-size: 1.2rem;
            font-weight: 500;
        }

        .table-wrapper {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }

        th {
            background-color: #1a2740;
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
        }

        td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #eee;
            font-size: 0.9rem;
        }

        tr:hover {
            background-color: #f9f9f9;
        }

        tr:nth-child(even) {
            background-color: #f5f5f5;
        }

        tr:nth-child(even):hover {
            background-color: #efefef;
        }

        .sample-no {
            font-weight: 600;
            color: #0097a7;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 2rem;
            color: #0097a7;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #0097a7;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }

        .tag {
            background-color: #e0f2f1;
            color: #00796b;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .error-message {
            background: #ffebee;
            border-left: 4px solid #f44336;
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 4px;
            color: #c62828;
            display: none;
        }

        .error-message.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Fabric Sample Selection Tool</h1>
        <p>Smart Search by Buyer Requirements</p>
    </div>

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
                            <option value="SOLID">SOLID</option>
                            <option value="PRINT">PRINT</option>
                            <option value="CHECKS">CHECKS</option>
                            <option value="STRIPES">STRIPES</option>
                            <option value="YD+PRINT">YD+PRINT</option>
                            <option value="WHITE+PRINT">WHITE+PRINT</option>
                            <option value="DYED+PRINT">DYED+PRINT</option>
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
                        <label for="gsm_min">GSM Range (Min)</label>
                        <input type="number" id="gsm_min" name="gsm_min" placeholder="e.g., 100" min="0">
                    </div>

                    <div class="form-group">
                        <label for="gsm_max">GSM Range (Max)</label>
                        <input type="number" id="gsm_max" name="gsm_max" placeholder="e.g., 200" min="0">
                    </div>
                </div>

                <div class="form-group" style="grid-column: 1 / -1;">
                    <label for="feel_terms">Performance/Feel Terms</label>
                    <input type="text" id="feel_terms" name="feel_terms" placeholder="e.g., soft feel, breathable, shiny" style="min-height: 60px;">
                </div>

                <div class="button-group">
                    <button type="reset" class="btn-reset">Clear</button>
                    <button type="submit" class="btn-search">Search Samples</button>
                </div>
            </form>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Searching samples...</p>
        </div>

        <div class="error-message" id="errorMessage"></div>

        <div class="results-section" id="resultsSection">
            <div class="card">
                <div class="results-info">
                    <h3><span id="resultCount">0</span> samples found</h3>
                    <div id="termsDisplay"></div>
                </div>

                <div id="resultsContent"></div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById("searchForm").addEventListener("submit", async function(e) {
            e.preventDefault();

            const loading = document.getElementById("loading");
            const resultsSection = document.getElementById("resultsSection");
            const errorMessage = document.getElementById("errorMessage");

            loading.classList.add("show");
            resultsSection.classList.remove("show");
            errorMessage.classList.remove("show");

            const formData = new FormData(this);

            try {
                const response = await fetch("/search", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();
                loading.classList.remove("show");

                displayResults(data);
                resultsSection.classList.add("show");

            } catch (error) {
                loading.classList.remove("show");
                errorMessage.textContent = "Error performing search. Please try again.";
                errorMessage.classList.add("show");
                console.error("Search error:", error);
            }
        });

        function displayResults(data) {
            const resultCount = document.getElementById("resultCount");
            const termsDisplay = document.getElementById("termsDisplay");
            const resultsContent = document.getElementById("resultsContent");

            resultCount.textContent = data.total_count;

            if (data.standard_terms.length > 0) {
                const tags = data.standard_terms.map(t => '<span class="tag">' + t + '</span>').join("");
                termsDisplay.innerHTML = '<p style="margin-top: 0.5rem; font-weight: 500;">Detected Properties:</p><div class="tags">' + tags + '</div>';
            } else {
                termsDisplay.innerHTML = "";
            }

            if (data.results.length === 0) {
                resultsContent.innerHTML = '<div class="no-results"><p>No samples matched your requirements.</p></div>';
            } else {
                let tableHTML = '<div class="table-wrapper"><table><thead><tr>';
                tableHTML += '<th>Sample No</th><th>Article</th><th>Product</th><th>Yarn</th><th>Count</th><th>GSM</th><th>Blend</th><th>Weave</th><th>Finish</th>';
                tableHTML += '</tr></thead><tbody>';

                data.results.forEach(function(sample) {
                    tableHTML += '<tr>';
                    tableHTML += '<td class="sample-no">' + sample.sample_no + '</td>';
                    tableHTML += '<td>' + sample.article + '</td>';
                    tableHTML += '<td>' + sample.product + '</td>';
                    tableHTML += '<td>' + sample.yarn + '</td>';
                    tableHTML += '<td>' + sample.count + '</td>';
                    tableHTML += '<td>' + sample.gsm + '</td>';
                    tableHTML += '<td>' + sample.blend + '</td>';
                    tableHTML += '<td>' + sample.weave + '</td>';
                    tableHTML += '<td>' + sample.finish + '</td>';
                    tableHTML += '</tr>';
                });

                tableHTML += '</tbody></table></div>';
                resultsContent.innerHTML = tableHTML;
            }
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
