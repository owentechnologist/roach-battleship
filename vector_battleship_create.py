import sys,random

# with one hot encoding for type and additional area_measure --> vector is now 105 dimensions
# accepts ship_type of 'submarine', 'destroyer','aircraft_carrier','skiff'
def make_ship_shape_from_anchorXY(anchorX,anchorY,ship_type):
    anchorX=int(anchorX)
    anchorY=int(anchorY)
    #print(f'ORIGINAL anchorX = {anchorX}  anchorY = {anchorY}')
    # make sure ship fits in our small grid 10x10:

    # NB: The position of X=0, Y=0 is the top left corner (not the bottom left)
    # make the ship cigar-shaped first by increasing the X distance 
    # between each pointXY1 and pointXY2 before doing the opposite
     
    # picture a grid w/ 100 squares (10x10) <-- this is a quadrant
    
    # for each square in a quadrant, place a zero if the ship does not overlap it
    # ^ place a 1 if the ship overlaps that square
    # the grid is flattened to a single array of 100 elements
    # x=2, y=2 would live at element (x)+((y*10)-10)  or: 12
    # x=9, y=4 would live at element (x)+(y*10)  or: 49
    # starting from that anchor point - mark other occupied squares 
    # All ships must fit in a quadrant

    if ship_type == 'destroyer':
        # if ship_type == destroyer (default):

        # anchor values for y must be lower than 4
        # anchor values for x must be between 2 and 8
        # 1 square wide at their anchor point and 2 more on the Y axis 
        # 3 squares wide from the 3rd through the 5th on the y axis
        # 1 square wide for 2 more squares on the y axis
        #           []        <-- anchor_point 
        #           []        <-- anchor_point + 10
        #         [][][]      <-- anchor_point + 19,20,21
        #         [][][]      <-- anchor_point + 29,30,31
        #         [][][]      <-- anchor_point + 39,40,41
        #           []        <-- anchor_point + 50
        #           []        <-- anchor_point + 60
        if anchorX<2:
            anchorX = 2
        if anchorX>9:
            anchorX = 9
        if anchorY<1:
            anchorY = 1
        if anchorY>4:
            anchorY = 4
        anchor_point=anchorX+((anchorY*10)-10)
        #print(f'CORRECTED anchorX = {anchorX}  anchorY = {anchorY} anchor_point = {anchor_point}')

        ship_points=[anchor_point,anchor_point+10,anchor_point+19,
                    anchor_point+20,anchor_point+21,anchor_point+29,
                    anchor_point+30,anchor_point+31,anchor_point+39,
                    anchor_point+40,anchor_point+41,anchor_point+50,
                    anchor_point+60]
        
    if ship_type == 'submarine':
        # if ship_type == submarine:
        # anchor values for y must be lower than 6
        # anchor values for x must be between 1 and 10
        #           .        <-- anchor_point 
        #           .        <-- anchor_point + 10
        #           .        <-- anchor_point + 20
        #           .        <-- anchor_point + 30
        #           .        <-- anchor_point + 40
        if anchorX <= 0:
            anchorX = 1
        if anchorX > 10:
            anchorX = 10
        if anchorY<1:
            anchorY = 1
        if anchorY>5:
            anchorY = 5
        anchor_point=anchorX+((anchorY*10)-10)
        #print(f'CORRECTED anchorX = {anchorX}  anchorY = {anchorY} anchor_point = {anchor_point}')
        
        ship_points=[anchor_point,anchor_point+10,
                    anchor_point+20,anchor_point+30,
                    anchor_point+40,anchor_point+50]

    if ship_type == 'skiff':
        # if ship_type == skiff:
        # anchor values for y must be lower than 7
        # anchor values for x must be between 1 and 10
        #           | |        <-- anchor_point 
        #           | |       <-- anchor_point + 10
        #           | |       <-- anchor_point + 20
        if anchorX <= 0:
            anchorX = 1
        if anchorX > 10:
            anchorX = 10
        if anchorY<1:
            anchorY = 1
        if anchorY>7:
            anchorY = 7
        anchor_point=anchorX+((anchorY*10)-10)
        #print(f'CORRECTED anchorX = {anchorX}  anchorY = {anchorY} anchor_point = {anchor_point}')
        
        ship_points=[anchor_point,anchor_point+10,
                    anchor_point+20,anchor_point+30]

    if ship_type == 'aircraft_carrier':
        # if ship_type == aircraft_carrier (default):

        # arbitrarily, aircraft_carriers are placed horizontally
        # anchor values for y must be between 1 and 7
        # anchor values for x must be between 1 and 2
        # | anchor point is an empty space
        # | 
        # V
        #   [][][][][][]
        # [][][][][][][][][]
        # [][][][][][][][][]
        #   [][][][][][]
        if anchorX>2:
            anchorX = 2
        if anchorY<1:
            anchorY = 1
        if anchorY>7:
            anchorY = 7
        anchor_point=anchorX+((anchorY*10)-10)
        #print(f'CORRECTED anchorX = {anchorX}  anchorY = {anchorY} anchor_point = {anchor_point}')

        ship_points=[anchor_point+1,anchor_point+2,anchor_point+3,
                     anchor_point+4,anchor_point+5,anchor_point+6,
                     anchor_point+10,anchor_point+11,anchor_point+12,
                     anchor_point+13,anchor_point+14,anchor_point+15,
                     anchor_point+16,anchor_point+17,anchor_point+18,
                     anchor_point+20,anchor_point+21,anchor_point+22,
                     anchor_point+23,anchor_point+24,anchor_point+25,
                     anchor_point+26,anchor_point+27,anchor_point+28,
                     anchor_point+31,anchor_point+32,anchor_point+33,
                     anchor_point+34,anchor_point+35,anchor_point+36]

    if ship_type == 'flotsam':
        # if ship_type == flotsam:
        # this is not a ship it is garbage/white noise
        # anchor values are ignored each point is assigned a random value
        # result may be something like this:
        # []\ \[][][][] . [][]
        #   . [][]| |[] . [][][]
        #   [] . [][][][]
        anchorX = 1
        anchorY = 3
        anchor_point=30    
        ship_points=[anchor_point,anchor_point+2,anchor_point+3,
                     anchor_point+11,anchor_point+14,anchor_point+15,
                     anchor_point+20,anchor_point+22,anchor_point+24,anchor_point+26,
                     anchor_point+30,anchor_point+31,anchor_point+34,anchor_point+35,anchor_point+36,anchor_point+37]

    print(f' Target generated {ship_type} has anchor_point of {anchorX+((anchorY*10)-10)}')
    ship_list=[]
    ship_area_counter=0
    ship_one_hot=[0,0,0,0] # [0,0,0,1]==sub, [0,0,1,0]==skiff, [0,1,0,0]==destroyer, [1,0,0,0]==aircraft_carrier
    for point in range(1,101):
        if point in ship_points:
            ship_area_counter=ship_area_counter+.1 ## to help differentiate size of vessels
            if ship_type == 'submarine':
                ship_list.append((point/1300)+.01) #.001
                #ship_list.append(.05)
                ship_one_hot=[0,0,0,1]
            elif ship_type == 'skiff':
                ship_list.append((point/1300)+.015) #.015
                #ship_list.append(.05)
                ship_one_hot=[0,0,1,0]
            elif ship_type == 'destroyer':
                ship_list.append((point/1300)+.02) #.002
                #ship_list.append(.05)
                ship_one_hot=[0,1,0,0]
            elif ship_type == 'flotsam':
                ship_list.append(random.uniform(0, .009)) ## scattered junk
                ship_one_hot=[0,0,0,0]
            else:
                ship_list.append((point/1300)+.005) ## .0025 aircraft_carrier
                #ship_list.append(.05)
                ship_one_hot=[1,0,0,0]
        else:
            ship_list.append(0.0)

    print_ship(ship_list,ship_type)
    ## add one-shot encode ship_type and area of the ships to make total vector dimensions = 104
    ship_list.append(ship_area_counter)
    ship_list.extend(ship_one_hot)
    print('\n\n')
    print(ship_list)
    return (ship_list)

def print_ship(ship_list,ship_type):
    for y in range(0,10):
        print("|",end="")
        for x in range(0,10):
            if ship_list[x+(y*10)]!=0:
                if ship_type=='submarine': # submerged
                    print(' . ',end="")
                elif ship_type=='skiff':  # small skiff
                    print('| |',end="")
                elif ship_type=='destroyer' or ship_type=='aircraft_carrier': # surface
                    print('[ ]',end="")
                elif ship_type=='flotsam': ## garbage
                    print('#',end="")
            else: # nothing there, print a wave ~
                print(' ~ ',end="")
        print(" |")

if __name__ == "__main__":
    x=sys.argv[1]
    y=sys.argv[2]
    ship_type=sys.argv[3]
    make_ship_shape_from_anchorXY(x,y,ship_type)
    print(f'The ship was created using {x}, {y}')
