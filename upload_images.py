"""
Upload all sample images from 'SAMPLE IMAGES' folder to Supabase Storage.

Prerequisites:
1. Create a PUBLIC bucket named 'sample-images' in Supabase Dashboard → Storage
2. Run this script once to upload all 50 images
"""
import os
import httpx

SUPABASE_URL = "https://gscxycvoeprxmkzfvnks.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdzY3h5Y3ZvZXByeG1remZ2bmtzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzNjA0OTAsImV4cCI6MjA4OTkzNjQ5MH0.CVqLTwGfTCdA2EeSu2ayEv3ID4P68STHgm8XM0c-rus"

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "SAMPLE IMAGES")
BUCKET = "Neha"

client = httpx.Client(timeout=30.0)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

uploaded = 0
failed = 0

for filename in sorted(os.listdir(IMAGES_DIR)):
    if not filename.lower().endswith((".jpeg", ".jpg")):
        continue
    filepath = os.path.join(IMAGES_DIR, filename)
    with open(filepath, "rb") as f:
        file_data = f.read()
    try:
        r = client.post(
            f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{filename}",
            content=file_data,
            headers={**headers, "Content-Type": "image/jpeg"},
        )
        if r.status_code in (200, 201):
            uploaded += 1
            print(f"  Uploaded: {filename}")
        elif r.status_code == 409:
            print(f"  Already exists: {filename}")
            uploaded += 1
        else:
            failed += 1
            print(f"  FAILED ({r.status_code}): {filename} - {r.text}")
    except Exception as e:
        failed += 1
        print(f"  ERROR: {filename} - {e}")

print(f"\nDone: {uploaded} uploaded, {failed} failed")
