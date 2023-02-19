CREATE TABLE IF NOT EXISTS picks (
    user_id integer,
    pick_url text,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
)