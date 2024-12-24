from Simplex import ArtificialSimplex

inf = 999999

class BranchAndBound:
    def __init__(self, f_list, mmin, tab):
        self.f_list = f_list
        self.tab = []
        for i in range(len(tab)):
            self.tab.append([])
            self.tab[i]=tab[i].copy()
        self.mmin = mmin
        self.opt_f_res = -inf if mmin == "max" else inf
        self.optimal = False

    def _isint(self, a, b):
        return a-b==0

    def solve(self):
        self._get_solution(self.f_list, self.tab)
        return self.opt_f_res, self.opt_basis, self.optimal

    def _get_solution(self, f_list, tab):
        simplex = ArtificialSimplex(f_list, self.mmin, tab)
        basis, f_res,  optim = simplex.get_solution()
        if not optim:
            return
        if all(self._isint(x, int(x)) for x in basis):
            if self.mmin=="max":
                if f_res > self.opt_f_res:
                    self.opt_f_res = f_res
                    self.opt_basis = basis.copy()
            else:
                if f_res < self.opt_f_res:
                    self.opt_f_res = f_res
                    self.opt_basis = basis.copy()
            self.optimal=True
            return

        for i_x, x in enumerate(basis):
            if not self._isint(x, int(x)):
                break

        left_tab = []
        right_tab = []
        for i in range(len(tab)):
            left_tab.append([])
            right_tab.append([])
            left_tab[i]=tab[i].copy()
            right_tab[i]=tab[i].copy()
        left_cond = ['0'] * len(self.f_list)
        left_cond.append('<=')
        left_cond.append(str(int(x)))
        left_cond[i_x] = '1'
        left_tab.append(left_cond)
        right_cond = left_cond.copy()
        right_cond[-2]='>='
        right_cond[-1]=(str(int(x+1)))
        right_tab.append(right_cond)
        self._get_solution(f_list,left_tab)
        self._get_solution(f_list,right_tab)




