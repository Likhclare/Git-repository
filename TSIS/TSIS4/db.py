import psycopg2
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"DB Error: {e}")

    def save_result(self, username, score, level):
        if not self.cursor: return
        try:
            self.cursor.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
            self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
            p_id = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", (p_id, score, level))
            self.conn.commit()
        except: pass

    def get_personal_best(self, username):
        if not self.cursor: return 0
        self.cursor.execute("SELECT MAX(score) FROM game_sessions gs JOIN players p ON gs.player_id = p.id WHERE p.username = %s", (username,))
        res = self.cursor.fetchone()[0]
        return res if res else 0

    def get_top_10(self):
        if not self.cursor: return []
        self.cursor.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at::date 
            FROM game_sessions gs JOIN players p ON gs.player_id = p.id 
            ORDER BY gs.score DESC LIMIT 10
        """)
        return self.cursor.fetchall()