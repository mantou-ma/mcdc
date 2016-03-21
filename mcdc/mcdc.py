__author__ = 'mantou'

import sys
param_num = 9

def fun(param):
    return (param[0] & (param[1] | param[2])) | ((param[3] | param[4]) & (param[5] | (param[6] & param[7]) | (param[8] & (1 - param[1]))))

"""
imput length = 4, 2^4

(a&(b|c))|((d|e)&(f|(g&h)|(i&j))

1 0 1 0 F
1 1 1 0 T
0 1 1 0 F
0 1 1 1 T
0 1 0 1 F

"""

ex = set([])
class step():
    def __init__(self, param, num):
        self.param = param
        self.num = num

def generate_param(i):
    param = []
    while i > 0:
        param.append(i % 2)
        i = i >> 1

    while len(param) < param_num:
        param.append(0)
    return param

def get_num(param):
    num = 0
    for i in range(0, len(param)):
        if param[i] > 0:
            num = num + 2 ** i
    return num

def pruning(bad_steps):
    for step in bad_steps:
        ex.add(step.num)

def search_forward(steps, chenged, res):
    current_step = steps[-1]
    num = current_step.num
    param = current_step.param
    next_change = []
    search_resList = list(steps)

    if len(steps) == param_num + 1:
        return steps

    for i in range(0, param_num):
        if i in chenged:
            continue
        next_param = list(param)
        next_param[i] = 1 - param[i]
        next_num = get_num(next_param)
        if next_num == 0:
            continue
        if next_num in ex:
            continue

        if fun(next_param) == res:
            next_change.append(i)

    for index in next_change:
        next_param = list(param)
        next_param[index] = 1 - param[index]
        next_num = get_num(next_param)
        next_step = step(next_param, next_num)
        temp_steps = list(steps)
        temp_steps.append(next_step)
        temp_changed = list(chenged)
        temp_changed.append(index)
        temp_res = search_forward(temp_steps, temp_changed, 1 - res)
        if len(temp_res) > len(search_resList):
            search_resList = temp_res
    return search_resList

for i in range(1, 2**param_num):
    param = generate_param(i)
    steps = []
    first_step = step(param, i)
    steps.append(first_step)
    res = fun(param)
    res_steps = search_forward(steps, [], 1-res)
    if len(res_steps) == param_num + 1:
        for item in res_steps:
            print item.param, fun(item.param)
        break