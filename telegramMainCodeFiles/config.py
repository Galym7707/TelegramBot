am = int(input())
listok = list()
while am != 0:
    n = map(int, input().split())
    am -= 1
    listok.extend(n)
print(listok.reversed())