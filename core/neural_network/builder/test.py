import copy
import inspect

funcs = []
for i in range(9):

    def func(x=i):
        print(x)
    f = func
    funcs.append(f)

for func in funcs:
    func()
    # print(inspect.getsource(func))