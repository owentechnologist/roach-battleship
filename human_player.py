import time,sys
import psycopg 
from vector_battleship_create import make_ship_shape_from_anchorXY  

# invoke this program like this:
# python human_player.py <match_percentage_threshold> <max_attempts>
# python human_player.py 55 20

class HumanPlayer:
    def __init__(self, db_config, match_percentage_threshold, max_attempts):
        self.db_config = db_config
        self.ship_types = ['submarine', 'destroyer', 'aircraft_carrier', 'skiff']
        self.quadrants = [1, 2, 3, 4]
        self.match_percentage_threshold = match_percentage_threshold
        self.max_attempts=max_attempts

    def get_connection(self):
        return psycopg.connect(**self.db_config)

    def run(self):
        attempt_counter=1
        while attempt_counter<=self.max_attempts:
            usr_input=''
            while usr_input=='':
                usr_input=input('enter a number between 1 and 4 for the quadrant ')
                if usr_input=='end':
                    sys.exit(0)
                quadrant=int(usr_input)
            ship_type_num=''
            while ship_type_num=='':
                ship_type_num=input('Enter a number corresponding to a ship type: 1 (destroyer) 2 (skiff) 3 (submarine) 4 (aircraft_carrier)  ')
                if ship_type_num=='end':
                    sys.exit(0)
            if ship_type_num=='1':
                ship_type='destroyer'
            elif ship_type_num=='2':
                ship_type='skiff'
            elif ship_type_num=='3':
                ship_type='submarine'
            elif ship_type_num=='4':
                ship_type='aircraft_carrier'
            anchor_y=int(input('enter a number between 1 and 10 for the y (down) coordinate '))
            anchor_x=int(input('enter a number between 1 and 10 for the x (over) coordinate '))
            print(f"\nTargeting a '{ship_type}' in quadrant {quadrant} at anchor ({anchor_y} , {anchor_x})")
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
                            print(f"\nAt least one ship detected in quadrant {quadrant}:")
                            for row in results:
                                val=row[0]
                                val = val.strip()
                                print(f"  - Detected_Ship_Class: {val}, Match_Percentage: {row[3]}%")
                                    
                                if(row[3]>99):
                                    print(f"\n\n\t<****> AFTER {attempt_counter} ATTEMPTS <****> \n\n\t\tPERFECT HIT -- EXITING PROGRAM")
                                    self.blast_ship_out_of_existence(row[1]) # passing the pk to the function for deletion
                                    sys.exit(0)
                        else:
                            print("No simlar and/or nearby ships detected in quadrant.")
                        attempt_counter=attempt_counter+1
            except Exception as e:
                print(f"❌ Error during processing: {e}")

        ## end of condition check for attempt_counter<max_attempts
        print('\n\n\t<****> You have used up all your attempts, Exiting...\n')
        sys.exit(0)


    def explain_game_play(self):
        explain_string = """Welcome to battleship!
        Battleships live in 1 of 4 quadrants
        Battleships have anchor points defined as an X,Y coordinate
        X values can be between 1 and 10
        Y values can be between 1 and 10

        You play by guessing the ship_type, anchor location of a battleship, and its quadrant.
        To target a battleship, you provide an X,Y coordinate and a quadrant
        You will be prompted to enter each value on a separate line:
        Quadrant
        ship_type
        Y
        X

        Good LucK!  Now, go sink a Battleship!"""
        print(explain_string)
        input('\nHit enter to continue...')

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

    player = HumanPlayer(db_config,float(sys.argv[1]),int(sys.argv[2]))
    player.explain_game_play()
    player.run()
