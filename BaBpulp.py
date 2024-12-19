from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, value

class BranchAndBoundSolver:
    def __init__(self, objective_coeffs, constraints, bounds):
        self.objective_coeffs = objective_coeffs
        self.constraints = constraints
        self.bounds = bounds
        self.solution = None
        self.objective_value = None

    def solve(self):
        problem = LpProblem("BranchAndBound", LpMaximize)
        variables = [LpVariable(f"x{i}", lowBound=bound[0], upBound=bound[1], cat="Integer") for i, bound in enumerate(self.bounds)]

        problem += sum(coef * var for coef, var in zip(self.objective_coeffs, variables)), "Objective"

        for coeffs, sign, rhs in self.constraints:
            expr = sum(c * v for c, v in zip(coeffs, variables))
            if sign == "<=":
                problem += expr <= rhs
            elif sign == ">=":
                problem += expr >= rhs
            elif sign == "=":
                problem += expr == rhs

        problem.solve()

        if LpStatus[problem.status] == "Optimal":
            self.solution = [value(var) for var in variables]
            self.objective_value = value(problem.objective)
        else:
            self.solution = None
            self.objective_value = None

        return self.solution, self.objective_value


if __name__ == "__main__":
    objective = [-1, -1, -1]
    constraints = [
        ([0, 36, 8], ">=", 40),
        ([4, 0, 3], ">=", 33)
    ]  # Ограничения
    bounds = [(0, None), (0, None), (0, None)]

    solver = BranchAndBoundSolver(objective, constraints, bounds)
    solution, objective_value = solver.solve()

    if solution is not None:
        print(f"Оптимальное решение: {solution}")
        print(f"Значение целевой функции: {objective_value}")
    else:
        print("Решение не найдено.")
