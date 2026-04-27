import psycopg2
from config import DB_CONFIG

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Ошибка БД: {e}")

    def save_result(self, username, score, level):
        try:
            self.cursor.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
            self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
            p_id = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                                (p_id, score, level))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def get_top_10(self):
        self.cursor.execute("""
            SELECT p.username, s.score, s.level_reached FROM game_sessions s 
            JOIN players p ON s.player_id = p.id ORDER BY s.score DESC LIMIT 10
        """)
        return self.cursor.fetchall()