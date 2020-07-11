from turtle import *
from time import sleep

# Schowanie żółwia, przyspieszenie rysowania i włączenie potrzeby update'owania
ht(); tracer(0); speed(0); delay(0)

class Gol:
    # ====================== INIT =======================
    # stworzenie potrzebnych zmiennych
    # ===================================================
    def __init__(self, dimensions = [200, 200], cell_dim = [10, 10], alive_cells = [], grid = True):
        self.dimensions = dimensions
        self.cell_dim = cell_dim
        self.alive_cells = alive_cells
        self.rules = {"alive" : [2,3], "dead" : [3]}
        self.grid = grid

    # ====================== LOGIC ======================
    # funkcje operujące danymi
    # ===================================================
    
    # 
    def gof_update(self):
        x_amo = self.dimensions[0]/self.cell_dim[0]
        y_amo = self.dimensions[1]/self.cell_dim[1]

        before_cells = self.alive_cells
        new_cells = []
        dead_cells = []

        temp_cells = []
        for subject in before_cells:
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
            
            amount = len( [c for c in around if c in before_cells] )

            if amount in self.rules["alive"]: new_cells.append(subject)
        
        dead_cells = []
        [dead_cells.append(i) for i in temp_cells if i not in dead_cells]
        dead_cells = [c for c in dead_cells if c not in before_cells]
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

            amount = len( [c for c in around if c in before_cells] )
            
            if amount in self.rules["dead"]: new_cells.append(subject)

        self.alive_cells = new_cells

    # 
    def return_clicked_cell(self, x, y):
        if x > self.dimensions[0]/2 or x < self.dimensions[0]/-2 or y > self.dimensions[1]/2 or y < self.dimensions[1]/-2: return None

        x_pos = 0
        y_pos = 0

        x_val = list(range(int((self.dimensions[0]/self.cell_dim[0])+1)))
        x_val = [self.dimensions[0]/-2 + i * self.cell_dim[0] for i in x_val]
        for i in range(len(x_val)-1):
            if x >= x_val[i] and x <= x_val[i+1]: x_pos = i; break
        
        y_val = list(range(int((self.dimensions[1]/self.cell_dim[1])+1)))
        y_val = [self.dimensions[1]/-2 + i * self.cell_dim[1] for i in y_val]
        for i in range(len(y_val)-1):
            if y >= y_val[i] and y <= y_val[i+1]: y_pos = i; break
    
        return [x_pos, y_pos]



    # ====================== DRAW =======================
    # funkcje rysujące
    # ===================================================

    # 
    def cell(self, state = True):
        if state==True: fillcolor("black"); begin_fill()
        for i in range(2): fd(self.cell_dim[0]); lt(90); fd(self.cell_dim[1]); lt(90)
        if state==True: end_fill()
    
    # 
    def magic_area(self):
        clear()
        
        x_amo = self.dimensions[0]/self.cell_dim[0]
        y_amo = self.dimensions[1]/self.cell_dim[1]

        pu(); goto(self.dimensions[0]/-2, self.dimensions[1]/-2); pd()

        if self.grid:
            for i in range(int(y_amo+1)):
                posit = pos()
                fd(self.dimensions[0]); pu(); goto(posit[0], posit[1] + self.cell_dim[1]); pd()
            pu(); goto(self.dimensions[0]/-2, self.dimensions[1]/-2); lt(90); pd()
            for i in range(int(x_amo)+1):
                posit = pos()
                fd(self.dimensions[1]); pu(); goto(posit[0] + self.cell_dim[0], posit[1]); pd()
            rt(90)
            
            pu(); goto(self.dimensions[0]/-2, self.dimensions[1]/-2); pd()

        if self.alive_cells != None:
            posit = pos()
            for c in self.alive_cells:
                pu(); goto(posit[0] + c[0] * self.cell_dim[0], posit[1] + c[1] * self.cell_dim[1]); pd()
                self.cell()
        
        update()



    # ==================== ON_EVENT =====================
    # funkcje używające innych (LOGIC oraz DRAW) do 
    # rysowania na podstawie tego co zrobi użytkownik
    # ===================================================

    #
    def click(self, x, y):
        clicked = self.return_clicked_cell(x, y)
        if clicked in self.alive_cells: self.alive_cells.remove(clicked)
        elif type(clicked) == list: self.alive_cells.append(clicked)
        self.magic_area()
    
    #
    def space(self):

        self.gof_update()
        self.magic_area()


game_of_life = Gol(dimensions=[500, 500], cell_dim=[10, 10], alive_cells = [], grid = True)

game_of_life.magic_area()

listen()
onscreenclick(game_of_life.click)
onkeypress(game_of_life.space, "space")
mainloop()