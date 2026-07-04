import sqlite3
import json

DB = "C:/Users/GG/.local/share/mimocode/mimocode.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Get later user messages from ses_10e66564cffeSruJPzu7YdToH2 (after offset 15)
c.execute("""
    SELECT substr(json_extract(p.data, '$.text'), 1, 500) as text,
           m.time_created
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE m.session_id = 'ses_10e66564cffeSruJPzu7YdToH2'
      AND json_extract(m.data, '$.role') = 'user'
      AND json_extract(p.data, '$.type') = 'text'
      AND length(json_extract(p.data, '$.text')) > 5
    ORDER BY m.time_created
""", ())
all_msgs = c.fetchall()
# Print from index 15 onwards (skip the ones we already saw)
for i, row in enumerate(all_msgs):
    if i >= 15 and i < 60:
        text = row[0] if row[0] else ""
        if text.strip() and '<system-reminder>' not in text and 'You are one of several' not in text and 'Read one source' not in text:
            print(f"  [{i}] {text[:400]}")

# Also look at the TZ upload message and the 3 design rejections
print("\n=== KEY DECISIONS IN ses_10e66564cffeSruJPzu7YdToH2 ===")
c.execute("""
    SELECT substr(json_extract(p.data, '$.text'), 1, 800) as text,
           m.time_created
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE m.session_id = 'ses_10e66564cffeSruJPzu7YdToH2'
      AND json_extract(m.data, '$.role') = 'user'
      AND json_extract(p.data, '$.type') = 'text'
      AND (
        LOWER(json_extract(p.data, '$.text')) LIKE '%не нрав%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%не похож%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%просто обычн%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%netflix%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%загрузил новое тз%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%не подходит%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%сделай норм%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%верни%'
        OR LOWER(json_extract(p.data, '$.text')) LIKE '%удал%'
      )
    ORDER BY m.time_created
""", ())
for row in c.fetchall():
    text = row[0] if row[0] else ""
    print(f"  {text[:500]}")
    print()

conn.close()
