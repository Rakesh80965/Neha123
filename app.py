import re
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ============================================================================
# SAMPLES DATABASE
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
        "blend": {"values": ["cotton", "modal", "viscose", "tencel", "giz"], "priority": "HIGH"},
        "blend_exclude": ["linen", "lenin"],
        "finish": {"values": ["soft touch", "brushed", "peach fin hand", "normal soft fin", "soft fin touch", "cotton soft fin", "chemical soft fin", "calender", "easy to iron", "anti microbial"], "priority": "HIGH"},
        "yarn_exclude": [],
        "negative_cross": [
            {"blend": "100% cotton", "finish": ["anti microbial", "easy to iron"], "finish_override": ["soft touch", "brushed", "peach fin hand", "soft fin touch", "cotton soft fin"]}
        ],
    },
    "Good Drape": {
        "yarn": {"values": ["compact", "tfo", "combed", "slub"], "priority": "HIGH"},
        "blend": {"values": ["viscose", "modal", "tencel", "giz"], "priority": "HIGH"},
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
        "blend": {"values": ["tencel", "viscose", "modal", "cotton"], "priority": "HIGH"},
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
        "blend": {"values": ["linen", "lenin"], "exact_values": ["100% cotton"], "priority": "HIGH"},
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

        # Sort by blend-values order first, then by score descending
        results.sort(key=lambda s: (
            get_blend_order_index(s, standard_terms),
            -sample_scores.get(s["sample_no"], 0)
        ))

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
