import random
import time,sys
import psycopg 
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
    def __init__(self, db_config, match_percentage_threshold):
        self.db_config = db_config
        self.ship_types = ['submarine', 'destroyer', 'aircraft_carrier', 'skiff']
        self.quadrants = [1, 2, 3, 4]
        self.match_percentage_threshold = match_percentage_threshold

    def get_connection(self):
        return psycopg.connect(**self.db_config)

    def run(self):
        nearby_ship = False
        suspect_quadrant = 1
        suspect_ship_type = 'submarine'
        while True:
            ship_type = random.choice(self.ship_types)
            quadrant = random.choice(self.quadrants)
            anchor_x = random.randint(1, 10)
            anchor_y = random.randint(1, 10)
            if(nearby_ship==True):
                #do nearbyShip things
                quadrant = suspect_quadrant
                ship_type = suspect_ship_type

            print(f"\nAttempting to place a '{ship_type}' in quadrant {quadrant} at anchor ({anchor_x}, {anchor_y})")

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
                            print("\nAt least one ship detected in quadrant:")
                            for row in results:
                                print(f"  - Detected_Ship_Class: strip({row[0]}), Match_Percentage: {row[3]}%, Hidden_Anchor_Point: {row[2]}")
                                if(row[3]>self.match_percentage_threshold) and (row[3]<99):
                                    print(f'\n📡 Honing in on quadrant {quadrant}')
                                    suspect_quadrant = quadrant
                                    suspect_ship_type = ship_type
                                    nearby_ship = True
                                if(row[3]>99):
                                    print(f"\n\nPERFECT HIT -- EXITING PROGRAM")
                                    sys.exit(0)
                            time.sleep(3) ## give user a chance to see results
                            
                        else:
                            print("No ships detected in quadrant.")
                            nearby_ship = False
            except Exception as e:
                print(f"❌ Error during processing: {e}")

            time.sleep(1)

# --- Example usage ---
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'port': 26257,
        'dbname': 'vb',
        'user': 'root'
    }

    player = AutomatedPlayer(db_config,float(sys.argv[1]))
    player.run()
