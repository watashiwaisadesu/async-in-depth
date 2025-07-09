

def gen(name: str):
    for i in name:
        yield i


def gen2(n: int):
    for i in range(n):
        yield i

g1 = gen('Isa')
g2 = gen2(7)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)
    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass

