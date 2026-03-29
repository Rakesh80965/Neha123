from app import SAMPLES, check_sample_against_rule

check = {1018: "IN", 1034: "IN", 1041: "IN", 1050: "OUT"}
for s in SAMPLES:
    if s['sample_no'] in check:
        p, sc = check_sample_against_rule(s, 'Shiny')
        expected = check[s['sample_no']]
        ok = (p and expected == "IN") or (not p and expected == "OUT")
        print(f"{s['sample_no']} {s['article']}: {'PASS' if ok else 'FAIL'} (shiny={p}, expected={expected}) weave={s['weave']} finish={s['finish']}")
