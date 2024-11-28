from traceback import print_tb, print_stack

from tabulate import tabulate


class Mincost:
    def __init__(self, supps, cons, tab):
        self._tab = []
        for i in tab:
            self._tab.append(i)
        self._supps = supps.copy()
        self._cons = cons.copy()
        self._cost_dict = {}
        sumsup = sum(supps)
        sumcon = sum(cons)
        if sumsup != sumcon:
            if sumsup < sumcon:
                self._supps.append(sumcon - sumsup)
                print(f'Запас меньше спроса на {sumcon - sumsup}. Добавляем фиктивный запас.')
                self._tab.append([0] * len(cons))
                for i in self._tab:
                    i.append(0)
            else:
                self._cons.append(sumsup - sumcon)
                print(f'Спрос меньше запаса на {sumsup - sumcon}. Добавляем фиктивный спрос')
                for i in self._tab:
                    i.append(0)
        self._plan = []
        for i in range(len(self._supps)):
            self._plan.append([0] * len(self._cons))

    def solve(self):
        difsup = self._supps.copy()
        difcon = self._cons.copy()
        for i in range(len(self._tab)):
            for j in range(len(self._tab[i])):
                if self._tab[i][j] not in self._cost_dict:
                    self._cost_dict[self._tab[i][j]] = []
                self._cost_dict[self._tab[i][j]].append([i, j])
        self._cost_dict = dict(sorted(self._cost_dict.items()))
        for k, i in self._cost_dict.items():
            if k == 0:
                continue
            for j in range(len(i)):
                if difsup[i[j][0]] != 0 and difcon[i[j][1]] != 0:
                    minim = min(difsup[i[j][0]], difcon[i[j][1]])
                    difsup[i[j][0]] -= minim
                    difcon[i[j][1]] -= minim
                    self._plan[i[j][0]][i[j][1]] = minim
        if 0 in self._cost_dict:
            for i in self._cost_dict[0]:
                if difsup[i[0]] != 0 and difcon[i[1]] != 0:
                    minim = min(difsup[i[0]], difcon[i[1]])
                    difsup[i[0]] -= minim
                    difcon[i[1]] -= minim
                    self._plan[i[0]][i[1]] = minim
        print("Опорный план:")
        self._printer()

    def _printer(self):
        summa = 0
        count = 0
        printab = []
        for i in range(len(self._supps) + 2):
            printab.append([0] * (len(self._cons) + 2))
        for i in range(1, len(printab)):
            printab[i][0] = f'A{i}'
            if i == len(printab) - 1:
                printab[i][0] = 'Запас'
        for i in range(len(self._tab)):
            printab[i + 1][-1] = self._supps[i]
            for j in range(len(self._tab[i])):
                if printab[-1][j + 1] == 0:
                    printab[-1][j + 1] = self._cons[j]
                printab[i + 1][j + 1] = f'{self._tab[i][j]}|{self._plan[i][j]}'
                summa += self._tab[i][j] * self._plan[i][j]
        for i in range(1, len(printab[0])):
            printab[0][i] = f'B{i}'
            if i == len(printab[0]) - 1:
                printab[0][i] = 'Спрос'
        printab[0][0] = ' '
        printab[-1][-1] = ' '
        print(tabulate(printab, tablefmt="grid"))
        print(f'Стоимость перевозки грузов равна {summa}')

