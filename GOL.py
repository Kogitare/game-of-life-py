from turtle import *
from time import sleep

ht(); tracer(0); speed(0); delay(0)

def cell(dim = [10,10], state = False):
    if state==True: fillcolor("black"); begin_fill()
    for i in range(2): fd(dim[0]); rt(90); fd(dim[1]); rt(90)
    if state==True: end_fill()

def make_numbered_2d_array(dimensions = [200,200], cell_dim = [10,10]):
    number = 0
    x_amo = dimensions[0]/cell_dim[0]
    y_amo = dimensions[1]/cell_dim[1]
    #for i in range()

def cell_positions(dimensions = [200,200], cell_dim = [10,10], live_cells = []):
    cell_pos = []
    x_amo = dimensions[0]/cell_dim[0]
    y_amo = dimensions[1]/cell_dim[1]
    for c in live_cells:
        place = [0,0]


#Draws a grid with alive cells (black squares)
def magic_area(dimensions = [200,200], cell_dim = [10,10], live_cells = []):
    reset()
    #Check if dimensions are ok (if cell dimensions divide grid dimensions evenly)
    if dimensions[0] % cell_dim[0] != 0 or dimensions[1] % cell_dim[1] != 0: print ("ERROR - wrong dimensions"); return
    
    x_amo = dimensions[0]/cell_dim[0]
    y_amo = dimensions[1]/cell_dim[1]

    pu(); goto(dimensions[0]/-2, dimensions[1]/-2); pd()

    #grid
    for i in range(int(y_amo+1)):
        posit = pos()
        fd(dimensions[0]); pu(); goto(posit[0], posit[1] + cell_dim[1]); pd()
    pu(); goto(dimensions[0]/-2, dimensions[1]/-2); lt(90); pd()
    for i in range(int(x_amo)+1):
        posit = pos()
        fd(dimensions[1]); pu(); goto(posit[0] + cell_dim[0], posit[1]); pd()
    rt(90)
    
    pu(); goto(dimensions[0]/-2, dimensions[1]/2); pd()

    #live cells
    cell_num = 0
    for i in range(int(y_amo)):
        for j in range(int(x_amo)):
            if cell_num in live_cells: cell(cell_dim, True)
            cell_num += 1
            pu(); fd(cell_dim[0]); pd()
        posit = pos()
        pu(); goto(posit[0] - dimensions[0], posit[1] - cell_dim[1]); pd()


def gof(live_cells = [], dimensions = [200,200], cell_dim = [10,10], 
            rules = {"alive" : [2,3], "dead" : [3]}):
    
    x_amo = dimensions[0]/cell_dim[0]
    y_amo = dimensions[1]/cell_dim[1]

    new_cells = []
    dead_cells = []

    temp_cells = []
    for subject in live_cells:
        around = [
            subject - (x_amo+1),
            subject - x_amo,
            subject - (x_amo-1),
            subject - 1,
            subject + 1,
            subject + (x_amo - 1),
            subject + x_amo,
            subject + (x_amo + 1)
        ]
        temp_cells.extend(around)

        if set(around) & set(live_cells): amount = len(set(around) & set(live_cells))
        else: amount = 0

        #check if cell survives
        if amount in rules["alive"]: new_cells.append(subject)

    
    dead_cells = []
    [dead_cells.append(i) for i in temp_cells if i not in dead_cells and i > 0 and i < (x_amo * y_amo) - 1]
    dead_cells = list(set(dead_cells) - set(live_cells))
    dead_cells.sort()

    for subject in dead_cells:
        around = [
            subject - (x_amo+1),
            subject - x_amo,
            subject - (x_amo-1),
            subject - 1,
            subject + 1,
            subject + (x_amo - 1),
            subject + x_amo,
            subject + (x_amo + 1)
        ]

        if set(around) & set(dead_cells): amount = len(set(around) & set(live_cells))
        else: amount = 0
        
        #check if cell can be born
        if amount in rules["dead"]: new_cells.append(subject)

    return [live_cells, dead_cells, new_cells]


#main loop
i = 0
live_cells = [
    265, 
    303, 305,
    333, 334, 341, 342, 355, 356,
    372, 376, 381, 382, 395, 396,
    401, 402, 411, 417, 421, 422,
    441, 442, 451, 455, 457, 458, 463, 465,
    491, 497, 505,
    532, 536,
    573, 574
]
dim = [400,400]

#turtle.mainloop()

while True:
    #sleep(0.5)
    magic_area(dimensions = dim, live_cells = live_cells)
    update()
    info = gof(dimensions = dim, live_cells = live_cells)
    live_cells = info[2]
    print("Iteration number: " + str(i))
    #exitonclick()
    i += 1

#mainloop()

#NAPRAWIĆ BŁAD PRZY GRANICACH