from Simplex import ArtificialSimplex
from BaBSimplexAB import BranchAndBound

print('Симплекс метод (0) или метод ветвей и границ? (1)')
flag = int(input())
print('Введите количество переменных в целевой функции:')
con = int(input())
print('Введите коэффициенты целевой функции через пробел:')
func_list=list(map(int,input().split(' ')))
print('Необходимо найти максимальное или минимальное значение целевой функции? (max/min)')
if input() == 'max':
    maxmin = 'max'
else:
    maxmin = 'min'
table = list()
print('Введите количество условий:')
crit = int(input())
print(f'Введите коэффициенты системы, знак и свободный член {crit} раз')
for i in range(crit):
    table.append(list(map(str, input().split(' '))))

if flag:
    sim = BranchAndBound(func_list,maxmin,table)
    sim.solve()
else:
    sim = ArtificialSimplex(func_list, maxmin, table)
    sim.solve_simplex()
