import random,sys
import psycopg 
from vector_battleship_create import make_ship_shape_from_anchorXY

class Populator:
    def __init__(self, db_config, number_of_objects):
        self.db_config = db_config
        self.ship_types = ['submarine', 'destroyer', 'aircraft_carrier', 'skiff', 'flotsam']
        self.quadrants = [1, 2, 3, 4]
        self.number_of_objects = number_of_objects

    def get_connection(self):
        return psycopg.connect(**self.db_config)

    def run(self):
        current_quadrant = random.randint(1,4)
        ship_type = random.choice(self.ship_types)
        pop_counter=1
        pop_counter_exceeded=False #based on number_of_objects
        while pop_counter_exceeded==False:
            quadrant = (current_quadrant %4)+1
            current_quadrant = current_quadrant+1
            ship_type=self.ship_types[pop_counter%5] # cycle through the ship_types
            pop_counter=pop_counter+1
            if(pop_counter>self.number_of_objects):
                pop_counter_exceeded=True        
            if ship_type=='flotsam':
                anchor_x = 1
                anchor_y = 1
            if ship_type=='skiff':
                anchor_x = random.randint(1,10)
                anchor_y = random.randint(1,7)
            if ship_type=='destroyer':
                anchor_x = random.randint(2,9)
                anchor_y = random.randint(1,4)
            if ship_type=='aircraft_carrier':
                anchor_x = random.randint(1,2)
                anchor_y = random.randint(1,7)
            if ship_type=='submarine':
                anchor_x = random.randint(1,10)
                anchor_y = random.randint(1,5)

            print(f"\nAttempting to place a '{ship_type}' in quadrant {quadrant} at anchor ({anchor_x}, {anchor_y})")

            vector = make_ship_shape_from_anchorXY(anchor_x, anchor_y, ship_type)
            vector_string = "[" + ", ".join(map(str, vector)) + "]"

            query = f"""
            INSERT into battleship (battleship_class,quadrant,anchorpoint,coordinates_embedding)
            VALUES (%s,%s,%s,%s);
            """
            coordinates_embedding =  f'{vector_string}'
            args = (ship_type, quadrant, anchor_x+((anchor_y*10)-10),coordinates_embedding) 
            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute(query,args)
            except Exception as e:
                print(f"❌ Error during INSERTION of {ship_type} in quadrant {quadrant}: {e}")

# --- Example usage ---
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'port': 26257,
        'dbname': 'vb',
        'user': 'root'
    }

    pop = Populator(db_config,float(sys.argv[1]))
    pop.run()
