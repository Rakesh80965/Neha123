from app import filter_samples

results, terms = filter_samples('ALL','','','','ALL','ALL','soft feel')
print(f"Found {len(results)} samples for 'soft feel':")
print(f"Detected terms: {terms}")
print()
for r in results:
    print(f"  Rank #{r['rank']:2d} | Sample {r['sample_no']} | Yarn: {r['yarn']:15s} | Count: {r['count']:6s} | Blend: {r['blend']:20s} | Finish: {r['finish']:30s} | Score: {r['priority_score']}")

print()
print("--- Testing 'shiny' ---")
results2, terms2 = filter_samples('ALL','','','','ALL','ALL','shiny')
print(f"Found {len(results2)} samples for 'shiny':")
for r in results2:
    print(f"  Rank #{r['rank']:2d} | Sample {r['sample_no']} | Yarn: {r['yarn']:15s} | Blend: {r['blend']:20s} | Weave: {r['weave']:15s} | Finish: {r['finish']:30s} | Score: {r['priority_score']}")
