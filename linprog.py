from scipy.optimize import linprog

class BranchAndBoundCLP:
    def __init__(self, c, A, b, bounds):
        self.c = c
        self.A = A
        self.b = b
        self.bounds = bounds
        self.best_solution = None
        self.best_value = float('inf')

    def solve(self):
        self._branch_and_bound(self.c, self.A, self.b, self.bounds)
        return self.best_solution, self.best_value

    def _is_close(self, a, b):
        return a-b==0

    def _branch_and_bound(self, c, A, b, bounds):
        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if not result.success:
            return

        x = result.x
        value = result.fun

        if all(self._is_close(x_i, int(x_i)) for x_i in x):
            if value < self.best_value:
                self.best_solution = [int(x_i) for x_i in x]
                self.best_value = value
            return

        for i, x_i in enumerate(x):
            if not self._is_close(x_i, int(x_i)):
                break

        floor_bound = bounds.copy()
        ceil_bound = bounds.copy()

        floor_bound[i] = (bounds[i][0], int(x[i]))
        ceil_bound[i] = (int(x[i]) + 1, bounds[i][1])

        self._branch_and_bound(c, A, b, floor_bound)
        self._branch_and_bound(c, A, b, ceil_bound)
# Пример использования
if __name__ == "__main__":
    c = [1, 1, 1]
    A = [[0, -36, -8], [-4 ,0, -3]]
    b = [-40, -33]
    bounds = [(0, None), (0, None), (0, None)]

    solver = BranchAndBoundCLP(c, A, b, bounds)
    solution, value = solver.solve()

    print("Лучшее решение:", solution)
    print("Значение целевой функции:", -value)
