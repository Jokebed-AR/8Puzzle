from simpleai.search \
    import astar, SearchProblem

#Se definen los valores a los que se quiere llegar
GOAL = '''1-2-3
8-0-4
7-6-5'''

#Se definen los valores con los que se inicia
INITIAL = '''4-5-1
8-3-7
0-6-2'''

def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])

def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]

def find_location(rows, element_to_find):   #Encuentra la direccion de la ficha buscada
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic               #Devuelve la  fila y la columna

# Se guarda la posicion fnal de cada ficha
goal_positions = {}
rows_goal = string_to_list(GOAL)
for number in '123804765':
    goal_positions[number] = find_location(rows_goal, number)

class PuzzleProblem(SearchProblem):
    def actions(self, state):           #Regresa una lista de las piezas que podemos mover a un espacio vacio
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, '0')

        actions = []                    #Dependiendo de la posición del 0 evalúa las opciones que tiene para moverse
        if row_e > 0:
            actions.append(rows[row_e - 1][col_e])
        if row_e < 2:
            actions.append(rows[row_e + 1][col_e])
        if col_e > 0:
            actions.append(rows[row_e][col_e - 1])
        if col_e < 2:
            actions.append(rows[row_e][col_e + 1])

        return actions

    def result(self, state, action):        #Regresa el estado actual despues de mover una ficha
        rows = string_to_list(state)        #La accion parameter contiene la ficha a mover
        row_e, col_e = find_location(rows, '0')
        row_n, col_n = find_location(rows, action)

        rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]

        return list_to_string(rows)

    def is_goal(self, state):
        return state == GOAL        #Devuelve true si el estado actual es el estado deseado

    def heuristic(self, state):     #Regresa una estimacion de la distancia al estado deseado
        rows = string_to_list(state)
        distance = 1
        for number in '123804765':
            row_n, col_n = find_location(rows, number)
            row_n_goal, col_n_goal = goal_positions[number]
            distance += abs(row_n - row_n_goal) + abs(col_n - col_n_goal)
        return distance

result = astar(PuzzleProblem(INITIAL))

for action, state in result.path():
    print('-----')
    print(state)
