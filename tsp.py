#!/usr/bin/env python

from ortools.linear_solver import pywraplp


def solve_tsp(distances):
    num_nodes = len(distances)
    # Create a solver instance and define the variables.
    solver = pywraplp.Solver('solve_tsp', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x = {}
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')
            x[j, i] = x[i, j]

    # Define the objective function.
    solver.Minimize(solver.Sum([x[i, j] * distances[i][j] for i in range(num_nodes) for j in range(i + 1, num_nodes)]))

    # Add constraints to ensure that every node is visited exactly once.
    for i in range(num_nodes):
        solver.Add(solver.Sum([x[j, i] for j in range(num_nodes) if j != i]) == 1)
        solver.Add(solver.Sum([x[i, j] for j in range(num_nodes) if j != i]) == 1)

    status = solver.Solve()
    print(status)
    if status == pywraplp.Solver.OPTIMAL:
        # Extract the solution.
        solution = []
        node = 0
        while len(solution) < num_nodes:
            solution.append(node)
            for j in range(num_nodes):
                if x[node, j].solution_value() > 0:
                    node = j
                    break
        return solution
    else:
        return None


distances = [
  [0, 5, 6],
  [5,0,9],
  [6,9, 0]
]
sol = solve_tsp(distances)
print(sol)
