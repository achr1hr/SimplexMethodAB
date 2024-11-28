from Mincost import Mincost

print('Введите количество запасов у каждого поставщика через пробел:')
supps = list(map(int,input().split(' ')))
print('Введите количество спроса у каждого потребителя через пробел')
cons = list(map(int,input().split(' ')))
print(f'Введите стоимость поставки {len(supps)} раз')
table=list()
for i in range(len(supps)):
    table.append(list(map(int, input().split(' '))))
mc = Mincost(supps,cons,table)
mc.solve()