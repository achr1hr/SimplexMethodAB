from tabulate import tabulate


class SimplexTablePrinter:
    def __init__(self, f_list, tab, basis, cj_arr, deltarr):
        self.out_hed = ['Cj', ''] + f_list + ['']
        self.out_tab = []
        for i in tab:
            self.out_tab.append(i.copy())
        sec_row = ['', 'Bx'] + list([f'A{i}' for i in range(len(tab[0]))]) + ['Q']
        self.out_tab.insert(0, sec_row)
        for i in range(1, len(tab) + 1):
            self.out_tab[i].insert(0, f'x{basis[i - 1]}')
            self.out_tab[i].insert(0, cj_arr[i - 1])
            self.out_tab[i].append('-')
        self.out_tab.append(['', 'del'] + deltarr)

    def print(self, tab, basis, cj_arr, delarr, qarr):
        self.update(tab, basis, cj_arr, delarr, qarr)
        print(tabulate(self.out_tab, headers=self.out_hed, tablefmt='grid'))

    def rounderarr(self, arr):
        arr_out = arr.copy()
        for i in range(len(arr_out)):
            num = round(arr_out[i], 4)
            num = int(num) if num-int(num)==0 else num
            arr_out[i]=num
        return arr_out

    def rounder(self, number):
        if number!='-':
            num = round(number, 4)
            return int(num) if num - int(num) == 0 else num
        return number

    def update(self, tab, basis, cj_arr, delarr, qarr):
        for i in range(1, len(tab) + 1):
            self.out_tab[i][1] = f'x{basis[i - 1]}'
            self.out_tab[i][0] = cj_arr[i - 1]
            self.out_tab[i][2:-1] = self.rounderarr(tab[i - 1])
            self.out_tab[i][-1] = self.rounder(qarr[i - 1])
        self.out_tab[-1][2:] = self.rounderarr(delarr)
