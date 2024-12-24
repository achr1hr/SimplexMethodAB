from printmaster import SimplexTablePrinter

inf = 999999


class ArtificialSimplex:
    def __init__(self, f_list, mmin, tab):
        self.leng = len(tab)
        self.tab = []
        for i in range(len(tab)):
            self.tab.append([])
        for i in range(len(tab)):
            self.tab[i].append(int(tab[i][-1]))
            for j in range(len(tab[i]) - 2):
                self.tab[i].append(float(tab[i][j]))
        self.columns = len(self.tab[0])-1
        self.f_list = [0] + f_list
        self.Cj_arr = [0] * self.leng
        self.basis = [0] * self.leng
        self.mmin = mmin
        self.addbasis(tab)
        self.addartbasis(tab)
        self.deltarr = ['-'] * len(self.tab[0])
        self.qarr = ['-'] * self.leng
        self.iter = 1
        self.out_tab = SimplexTablePrinter(self.f_list, self.tab, self.basis, self.Cj_arr,
                                           self.deltarr)
        self.flag = False
        self._showsteps = True

    def get_solution(self):
        self._showsteps = False
        self.solve_simplex()
        basis_solut = [0] * (len(self.tab[0]) - 1)
        for i in range(len(self.basis)):
            basis_solut[self.basis[i] - 1] = self.out_tab.rounder(self.tab[i][0])
        basis_solut = basis_solut[:self.columns]
        return basis_solut, self.out_tab.rounder(self.deltarr[0]), not self.flag

    def solve_simplex(self):
        while self.iteration() is not True:
            continue
        if self._showsteps:
            print('Итоговая сиплекс-таблица:')
            self.out_tab.print(self.tab, self.basis, self.Cj_arr, self.deltarr, self.qarr)
        if self.flag is not True and self._showsteps:
            self.out_tab.print_solution(self.tab, self.basis, self.f_list, self.deltarr)

    def iteration(self):
        if self._showsteps:
            print(f'Итерация {self.iter}:')
        for i in range(len(self.tab[0])):
            self.deltarr[i] = sum(
                self.tab[j][i] * self.f_list[self.basis[j]] for j in range(len(self.basis))) - \
                              self.f_list[i]
        if self.mmin == 'max':
            ind, val = min(enumerate(self.deltarr[1:]), key=lambda pair: pair[1])
            if val >= 0:
                if self._showsteps:
                    print("План оптимален, так как все дельты положительные\n")
                return True
            if self._showsteps:
                print(f'План не оптимален, так как del{ind + 1} = {val} отрицательна')
        else:
            ind, val = max(enumerate(self.deltarr[1:]), key=lambda pair: pair[1])
            if val <= 0:
                if self._showsteps:
                    print("План оптимален, так как все дельты отрицательные\n")
                return True
            if self._showsteps:
                print(f'План не оптимален, так как del{ind + 1} = {val} положительна')

        for i in range(self.leng):
            if (self.tab[i][ind + 1] > 0):
                self.qarr[i] = self.tab[i][0] / self.tab[i][ind + 1]
            else:
                self.qarr[i] = inf

        qind, qval = min(enumerate(self.qarr), key=lambda pair: pair[1])
        if qval == inf:
            if self._showsteps:
                print('Задача не может быть решена, так как все члены разрешающего столбца '
                  'отрицательные')
            self.flag = True
            return True
        if self._showsteps:
            self.out_tab.print(self.tab, self.basis, self.Cj_arr, self.deltarr, self.qarr)
        self.Cj_arr[qind] = self.f_list[ind + 1]
        if self._showsteps:
            print(f"Вектор A{self.basis[qind]} покидает базис")
            print(f"Вектор A{ind + 1} вводится в новый базис")
        self.basis[qind] = ind + 1
        if self._showsteps:
            print(f'Новый базис:(', *list(f'A{i}' for i in self.basis), ')')
            print('\n')
        self.rework_tab(qind, ind + 1)
        self.iter += 1
        return False

    def rework_tab(self, row, col):
        el_one = self.tab[row][col]
        for i in range(len(self.tab[row])):
            self.tab[row][i] = self.tab[row][i] / el_one
        for i in range(len(self.tab)):
            val_row = self.tab[i][col]
            if i == row:
                continue
            for j in range(len(self.tab[i])):
                self.tab[i][j] = self.tab[i][j] - self.tab[row][j] * val_row

    def addbasis(self, tab):
        for i in range(len(tab)):
            if tab[i][-2] != '=':
                self.f_list.append(0)
                for j in self.tab:
                    j.append(0)
                if tab[i][-2] == '>=':
                    self.tab[i][-1] = -1
                else:
                    self.tab[i][-1] = 1
                    self.basis[i] = len(self.tab[i]) - 1

    def addartbasis(self, tab):
        for i in range(len(tab)):
            if tab[i][-2] != '<=':
                if self.mmin == 'max':
                    self.f_list.append(-inf)
                else:
                    self.f_list.append(inf)
                for j in self.tab:
                    j.append(0)
                self.tab[i][-1] = 1
                self.basis[i] = len(self.tab[i]) - 1
