from simpleai.search import astar, SearchProblem

class PuzzleSolver(SearchProblem):
    def actions(self, cur_state):
        # Convert current state string to list representation
        rows = string_to_list(cur_state)
        
        # Find the location of the empty space ('e')
        row_empty, col_empty = get_location(rows, 'e')
        
        # Generate possible actions (moves) based on the empty space position
        actions = []
        if row_empty > 0:
            actions.append(rows[row_empty - 1][col_empty])
        if row_empty < 2:
            actions.append(rows[row_empty + 1][col_empty])
        if col_empty > 0:
            actions.append(rows[row_empty][col_empty - 1])
        if col_empty < 2:
            actions.append(rows[row_empty][col_empty + 1])
        
        return actions

    def result(self, state, action):
        # Convert state string to list representation
        rows = string_to_list(state)
        
        # Find the location of the empty space ('e') and the tile to be moved
        row_empty, col_empty = get_location(rows, 'e')
        row_new, col_new = get_location(rows, action)
        
        # Swap the positions of the empty space and the tile
        rows[row_empty][col_empty], rows[row_new][col_new] = \
            rows[row_new][col_new], rows[row_empty][col_empty]
        
        # Convert the updated list representation back to a string
        return list_to_string(rows)

    def is_goal(self, state):
        # Check if the state matches the goal state
        return state == GOAL

    def heuristic(self, state):
        # Calculate the Manhattan distance heuristic
        rows = string_to_list(state)
        distance = 0
        for number in '12345678e':
            row_new, col_new = get_location(rows, number)
            row_new_goal, col_new_goal = goal_positions[number]
            distance += abs(row_new - row_new_goal) + abs(col_new - col_new_goal)
        return distance

def list_to_string(input_list):
    # Convert list representation to string
    return '\n'.join(['-'.join(x) for x in input_list])

def string_to_list(input_string):
    # Convert string representation to list
    return [x.split('-') for x in input_string.split('\n')]

def get_location(rows, input_element):
    # Find the location of a specific element in the grid
    for i, row in enumerate(rows):
        for j, item in enumerate(row):
            if item == input_element:
                return i, j

# Define initial and goal states
GOAL = '''1-2-3
4-5-6
7-8-e'''
INITIAL = '''1-e-2
6-3-4
7-5-8'''

# Define positions of each number in the goal state
goal_positions = {}
rows_goal = string_to_list(GOAL)
for number in '12345678e':
    goal_positions[number] = get_location(rows_goal, number)

# Run A* search algorithm
result = astar(PuzzleSolver(INITIAL))

# Print results
for i, (action, state) in enumerate(result.path()):
    print()
    if action == None:
        print('Initial configuration')
    elif i == len(result.path()) - 1:
        print('After moving', action, 'into the empty space. Goal achieved!')
    else:
        print('After moving', action, 'into the empty space')
    print(state)