import random
import time
import psycopg2  # Requires `pip install psycopg2`
from vector_battleship_create import make_ship_shape_from_anchorXY  # Replace with actual module or inline

''' 
This class provides the behavior of an automated player who:
1. picks a quadrant at random
2. picks a ship type at random
3. picks an anchor point at random
4. checks for collision between ship at anchor point in quadrant and ships in vector database
5. prints out result
6. sleeps for 3 seconds 
'''

class AutomatedPlayer:
    def __init__(self, db_config):
        self.db_config = db_config
        self.ship_types = ['submarine', 'destroyer', 'aircraft_carrier', 'skiff']
        self.quadrants = [1, 2, 3, 4]

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def run(self):
        while True:
            ship_type = random.choice(self.ship_types)
            quadrant = random.choice(self.quadrants)
            anchor_x = random.randint(1, 10)
            anchor_y = random.randint(1, 10)

            print(f"\n📡 Attempting to place a '{ship_type}' in quadrant {quadrant} at anchor ({anchor_x}, {anchor_y})")

            vector = make_ship_shape_from_anchorXY(anchor_x, anchor_y, ship_type)
            vector_string = "[" + ", ".join(map(str, vector)) + "]"

            query = f"""
            WITH target_vector AS (
                SELECT '{vector_string}'::vector AS v
            )
            SELECT battleship_class, pk, anchorpoint,
                ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100, 2) AS "Percent Match"
            FROM battleship, target_vector 
            WHERE quadrant = {quadrant}
              AND (coordinates_embedding <-> v) <= 4
            ORDER BY "Percent Match" DESC
            LIMIT 2;
            """

            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute(query)
                        results = cur.fetchall()
                        if results:
                            print("🚨 Potential collision detected:")
                            for row in results:
                                print(f"  - Class: {row[0]}, Match: {row[3]}%, Anchor: {row[2]}")
                        else:
                            print("✅ No collisions — placement is clear.")
            except Exception as e:
                print(f"❌ Error during DB query: {e}")

            time.sleep(3)

# --- Example usage ---
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'port': 26257,
        'dbname': 'bank',
        'user': 'your_user',
        'password': 'your_password',
        'sslmode': 'require',
        'sslrootcert': '/path/to/your/ca.crt'
    }

    player = AutomatedPlayer(db_config)
    player.run()
