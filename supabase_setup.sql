-- =============================================================
-- Run this SQL in Supabase Dashboard → SQL Editor
-- =============================================================

-- 1) SAMPLES TABLE
CREATE TABLE IF NOT EXISTS samples (
    id          SERIAL PRIMARY KEY,
    sample_no   INTEGER UNIQUE NOT NULL,
    article     TEXT,
    product     TEXT,
    yarn        TEXT,
    count       TEXT,
    count_avg   INTEGER,
    construction TEXT,
    construction_total INTEGER,
    blend       TEXT,
    weave       TEXT,
    finish      TEXT,
    gsm         INTEGER
);

-- 2) WISHLIST GROUPS TABLE
CREATE TABLE IF NOT EXISTS wishlist_groups (
    id       SERIAL PRIMARY KEY,
    user_id  UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name     TEXT NOT NULL,
    UNIQUE(user_id, name)
);

-- 3) WISHLISTS TABLE
CREATE TABLE IF NOT EXISTS wishlists (
    id         SERIAL PRIMARY KEY,
    user_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    group_id   INTEGER NOT NULL REFERENCES wishlist_groups(id) ON DELETE CASCADE,
    sample_no  INTEGER NOT NULL,
    UNIQUE(user_id, group_id, sample_no)
);

-- 4) DISABLE ROW LEVEL SECURITY (server-side Flask app handles auth)
ALTER TABLE samples ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON samples FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE wishlist_groups ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON wishlist_groups FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE wishlists ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON wishlists FOR ALL USING (true) WITH CHECK (true);

-- =============================================================
-- SUPABASE STORAGE SETUP (do manually in Dashboard):
-- 1) Go to Storage → New Bucket → Name: "sample-images" → Public: ON
-- 2) Upload images from "SAMPLE IMAGES" folder (1001.jpeg - 1050.jpeg)
-- =============================================================

-- =============================================================
-- SUPABASE AUTH SETUP (do manually in Dashboard):
-- 1) Go to Authentication → Providers → Email
-- 2) Disable "Confirm email" for development/testing
-- =============================================================
