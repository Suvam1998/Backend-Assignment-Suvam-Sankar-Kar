from app.models import get_conn
from datetime import datetime

def insert_message(msg):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?)
        """, (
            msg["message_id"],
            msg["from"],
            msg["to"],
            msg["ts"],
            msg.get("text"),
            datetime.utcnow().isoformat() + "Z"
        ))
        conn.commit()
        return "created"
    except:
        return "duplicate"
    finally:
        conn.close()
