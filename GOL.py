from turtle import *
from time import sleep

# Schowanie żółwia, przyspieszenie rysowania i włączenie potrzeby update'owania
ht(); tracer(0); speed(0); delay(0)

# Rysowanie pojedynczej komórki
# dim = [x, y] - szerokość (x) i wysokość (y) komórki
# state = boolean - czy wypełnić komórkę czarnym kolorem
def cell(dim = [10,10], state = False):
    if state==True: fillcolor("black"); begin_fill()
    for i in range(2): fd(dim[0]); lt(90); fd(dim[1]); lt(90)
    if state==True: end_fill()

# Rysowanie żywych (czarnych) komórek i opcjonalnie siatki
# dimensions = [x, y] - szerokość (x) i wysokość (y) całego obszaru gry
# cell_dim = [x, y] - szerokość (x) i wysokość (y) pojedynczych komórek
# live_cells = list - lista miejsc w formacie [[x1, y1], [x2, y2], [x3, y3], ...] gdzie
#                     wskazywane są miejsca "żywych" komórek (czarnych pikseli)
# grid = boolean - określenie czy rysować siatkę, czy nie
def magic_area(dimensions = [200,200], cell_dim = [10,10], live_cells = [], grid = True):
    reset()
    
    x_amo = dimensions[0]/cell_dim[0]
    y_amo = dimensions[1]/cell_dim[1]

    pu(); goto(dimensions[0]/-2, dimensions[1]/-2); pd()

    #grid
    if grid:
        for i in range(int(y_amo+1)):
            posit = pos()
            fd(dimensions[0]); pu(); goto(posit[0], posit[1] + cell_dim[1]); pd()
        pu(); goto(dimensions[0]/-2, dimensions[1]/-2); lt(90); pd()
        for i in range(int(x_amo)+1):
            posit = pos()
            fd(dimensions[1]); pu(); goto(posit[0] + cell_dim[0], posit[1]); pd()
        rt(90)
        
        pu(); goto(dimensions[0]/-2, dimensions[1]/-2); pd()

    if live_cells!=None:
        posit = pos()
        for c in live_cells:
            pu(); goto(posit[0] + c[0] * cell_dim[0], posit[1] + c[1] * cell_dim[1]); pd()
            cell(cell_dim, True)

# Określenie nowego ustawienia "żywych" komórek na podstawie aktualnego ustawienia tych komórek
# dimensions = [x, y] - szerokość (x) i wysokość (y) całego obszaru gry
# cell_dim = [x, y] - szerokość (x) i wysokość (y) pojedynczych komórek
# live_cells = list - lista miejsc w formacie [[x1, y1], [x2, y2], [x3, y3], ...] gdzie
#                     wskazywane są miejsca "żywych" komórek (czarnych pikseli)
# rules = {"alive" : [], "dead" : []} - słownik z listami ilości żywych komórek wokół danej
#                                       komórki (żywej bądź martwej), dla których ma powstać
#                                       na jej miejscu nowa żywa komórka
def gof(dimensions = [200,200], cell_dim = [10,10], live_cells = [], 
            rules = {"alive" : [2,3], "dead" : [3]}):
    
    x_amo = dimensions[0]/cell_dim[0]
    y_amo = dimensions[1]/cell_dim[1]

    new_cells = []
    dead_cells = []

    temp_cells = []
    for subject in live_cells:
        around = [
            [subject[0] - 1, subject[1] + 1],
            [subject[0], subject[1] + 1],
            [subject[0] + 1, subject[1] + 1],
            [subject[0] - 1, subject[1]],
            [subject[0] + 1, subject[1]],
            [subject[0] - 1, subject[1] - 1],
            [subject[0], subject[1] - 1],
            [subject[0] + 1, subject[1] - 1]
        ]
        temp_cells.extend(around)

        temp_cells = [i for i in temp_cells if i[0] >= 0 and i[0] < x_amo and i[1] >= 0 and i[1] < y_amo]
        
        amount = len( [c for c in around if c in live_cells] )

        #check if cell survives
        if amount in rules["alive"]: new_cells.append(subject)

    
    dead_cells = []
    [dead_cells.append(i) for i in temp_cells if i not in dead_cells]
    dead_cells = [c for c in dead_cells if c not in live_cells]
    dead_cells.sort()

    for subject in dead_cells:
        around = [
            [subject[0] - 1, subject[1] + 1],
            [subject[0], subject[1] + 1],
            [subject[0] + 1, subject[1] + 1],
            [subject[0] - 1, subject[1]],
            [subject[0] + 1, subject[1]],
            [subject[0] - 1, subject[1] - 1],
            [subject[0], subject[1] - 1],
            [subject[0] + 1, subject[1] - 1]
        ]

        amount = len( [c for c in around if c in live_cells] )
        
        #check if cell can be born
        if amount in rules["dead"]: new_cells.append(subject)

    return [live_cells, dead_cells, new_cells]

def return_clicked_cell(x, y, dimensions = [200,200], cell_dim = [10,10]):
    x_amo = dimensions[0]/cell_dim[0]
    y_amo = dimensions[1]/cell_dim[1]

    cell_place = [[0, 0]]

    for col, i in zip(range(int(x_amo)), range(int(dimensions[0]/-2) + cell_dim[0], int(dimensions[0]/2) + cell_dim[0] + 1, cell_dim[0])):
        print("!c",col, i)
        if x < col:
            print("?")
            cell_place[0][0] = i
            break
    for lin, i in zip(range(int(y_amo)), range(int(dimensions[1]/-2) + cell_dim[1], int(dimensions[1]/2) + cell_dim[1] + 1, cell_dim[1])):
        print("!l",lin,i)
        if y < lin:
            print("??")
            cell_place[0][1] = i
            break
    
    print(cell_place, x, y)
    magic_area(dimensions = dimensions, cell_dim = cell_dim, live_cells = cell_place, grid = True)



'''
r = [0, 70]
live_cells = [
    [r[0]+12, r[1]], [r[0]+13, r[1]], 
    [r[0]+11, r[1]+1], [r[0]+15, r[1]+1],
    [r[0]+10, r[1]+2], [r[0]+16, r[1]+2], [r[0]+24, r[1]+2],
    [r[0], r[1]+3], [r[0]+1, r[1]+3], [r[0]+10, r[1]+3], [r[0]+14, r[1]+3], [r[0]+16, r[1]+3], [r[0]+17, r[1]+3], [r[0]+22, r[1]+3], [r[0]+24, r[1]+3],
    [r[0], r[1]+4], [r[0]+1, r[1]+4], [r[0]+10, r[1]+4], [r[0]+16, r[1]+4], [r[0]+20, r[1]+4], [r[0]+21, r[1]+4],
    [r[0]+11, r[1]+5], [r[0]+15, r[1]+5], [r[0]+20, r[1]+5], [r[0]+21, r[1]+5], [r[0]+34, r[1]+5], [r[0]+35, r[1]+5],
    [r[0]+12, r[1]+6], [r[0]+13, r[1]+6], [r[0]+20, r[1]+6], [r[0]+21, r[1]+6], [r[0]+34, r[1]+6], [r[0]+35, r[1]+6],
    [r[0]+22, r[1]+7], [r[0]+24, r[1]+7],
    [r[0]+24, r[1]+8]
]
'''
dim = [100,100]
c_dim = [20,20]
canvas = getcanvas()
live = []
'''
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))
'''
def click(x,y):
    return_clicked_cell(x, y, dimensions=dim, cell_dim=c_dim)

canvas = getcanvas()
onscreenclick (click)

'''
while True:
    #canvas = getcanvas()
    #x, y = canvas.winfo_pointerxy()
    #live = [return_clicked_cell(x,y)]
    magic_area(dimensions = dim, cell_dim = c_dim, live_cells = live, grid = True)
    print(live)
'''

mainloop()

'''
# main loop
while True:
    magic_area(dimensions = dim, cell_dim = c_dim, live_cells = live_cells, grid = True)
    update()
    sleep(0.05)
    info = gof(dimensions = dim, cell_dim = c_dim, live_cells = live_cells)
    live_cells = info[2]
'''