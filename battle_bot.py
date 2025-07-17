import random
import time,sys
import psycopg 
from vector_battleship_create import make_ship_shape_from_anchorXY  
''' 
This class provides the behavior of an automated player who:
1. picks a quadrant at random
2. picks a ship type at random
3. picks an anchor point at random
4. checks for collision between ship at anchor point in quadrant and ships in vector database
5. prints out result
6. sleeps for 1 second when it detects ships in the same quadrant and hones in on same quadrant 
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
        suspect_quadrant = 4
        suspect_ship_type = 'submarine'
        suspect_ship_reuse_count = 0
        attempt_counter=0
        attempt_counter_exceeded=False
        suspect_ship_reuse_x_set= {0,}
        while attempt_counter_exceeded==False:
            ship_type = random.choice(self.ship_types)
            quadrant = random.choice(self.quadrants)
            anchor_x = random.randint(1, 10)
            while anchor_x in suspect_ship_reuse_x_set:
                anchor_x = random.randint(1, 14)
            suspect_ship_reuse_x_set.add(anchor_x)
            anchor_y = random.randint(1, 10)
            attempt_counter=attempt_counter+1
            if(attempt_counter>100):
                attempt_counter_exceeded=True
            if(nearby_ship==True):
                #do nearbyShip things
                quadrant = suspect_quadrant
                if(suspect_ship_reuse_count<10):
                    ship_type = suspect_ship_type
                else:
                    suspect_ship_reuse_count=0
                    suspect_ship_reuse_x_set.clear()
            else:
                #do dissimilar ship things:
                suspect_ship_reuse_x_set.clear()

            print(f"\nTargeting a '{ship_type}' in quadrant {quadrant} at anchor ({anchor_x}, {anchor_y})")

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
              AND ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100, 2) >= {self.match_percentage_threshold}
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
                                val=row[0]
                                val = val.strip()
                                print(f"  - Detected_Ship_Class: {val}, Match_Percentage: {row[3]}%, Hidden_Anchor_Point: {row[2]}")
                                if(row[3]>self.match_percentage_threshold) and (row[3]<99):
                                    print(f'\n📡 Honing in on quadrant {quadrant} with suspect_ship_type {suspect_ship_type} and suspect_ship_reuse_count {suspect_ship_reuse_count}')
                                    suspect_quadrant = quadrant
                                    suspect_ship_type = ship_type
                                    suspect_ship_reuse_count=suspect_ship_reuse_count+1
                                    nearby_ship = True
                                    time.sleep(1) ## give user a chance to notice results
                                if(row[3]>99):
                                    print(f"\n\n\t<****> AFTER {attempt_counter} ATTEMPTS <****> \n\n\t\tPERFECT HIT -- EXITING PROGRAM")
                                    self.blast_ship_out_of_existence(row[1])
                                    sys.exit(0)
                        else:
                            print("No simlar and/or nearby ships detected in quadrant.")
                            nearby_ship = False
            except Exception as e:
                print(f"❌ Error during processing: {e}")

            time.sleep(.3) #300 millis
        ## end of condition check for attempt_counter<max_attempts
        print('\n\n\t<****> The bot has used up all 100 of its attempts, Exiting...\n')
        sys.exit(0)

    def blast_ship_out_of_existence(self,pk):
        print(f'\n\n%^%^%^%^***. KABLOOEY!!!!! \n\ndeleting row with PK == {pk}')
        query = f"DELETE FROM battleship WHERE PK=%s::UUID;"
        args=(pk,)
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query,args)
        except Exception as e:
            print(f"❌ Error during deletion of ship with PK of {pk}: \n{e}")

# --- Likely entry point for the python interpretor ---
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'port': 26257,
        'dbname': 'vb',
        'user': 'root'
    }

    player = AutomatedPlayer(db_config,float(sys.argv[1]))
    player.run()
