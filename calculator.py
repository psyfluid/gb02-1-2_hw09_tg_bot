import re
from math import *


def isnumber(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def get_result(ex):
    try:
        if re.search(r"[a-zA-Z]+", ex):
            return eval(ex)
        else:
            return calc_expr(ex)
    except Exception as e:
        print(e)
        return 'Error'


def calc_expr(ex):
    lpar = rpar = 0
    l_id, r_id = -1, len(ex)
    for i, char in enumerate(ex):
        if lpar and rpar:
            lpar -= 1
            rpar -= 1
            return calc_expr(f'{ex[:l_id]}{calc_expr(ex[l_id + 1:r_id])}{ex[r_id + 1:]}')
        if char == '(':
            lpar += 1
            l_id = i
        elif char == ')':
            rpar += 1
            r_id = i

    if lpar:
        return calc_expr(f'{ex[:l_id]}{calc_expr(ex[l_id + 1:r_id])}{ex[r_id + 1:]}')
    else:
        return calc_inside(ex[l_id + 1:r_id])


def calc_inside(ex):
    if not ex:
        return ''
    elif isnumber(ex):
        return float(ex)
    elif (i := ex.find('+')) > 0:
        return calc_inside(ex[:i]) + calc_inside(ex[i + 1:])
    elif (i := ex.find('-', 1)) > 0:
        if ex[i - 1] in ('*', '/'):
            return -1 * calc_inside(f'{calc_inside(ex[:i - 1])}{ex[i - 1]}{calc_inside(ex[i + 1:])}')
        elif ex[i - 1] == '+':
            return calc_inside(ex[:i - 1]) - calc_inside(ex[i + 1:])
        elif ex[i - 1] == '-':
            return calc_inside(ex[:i - 1]) + calc_inside(ex[i + 1:])
        else:
            return calc_inside(ex[:i]) - calc_inside(ex[i + 1:])
    elif (i := ex.find('*')) > 0:
        return calc_inside(ex[:i]) * calc_inside(ex[i + 1:])
    elif (i := ex.find('/')) > 0:
        return calc_inside(ex[:i]) / calc_inside(ex[i + 1:])


def main():
    expr = input('Введите выражение: ')
    expr = expr.replace(' ', '')
    expr = expr.replace(',', '.')
    print(f"{expr} = {get_result(expr)}")


if __name__ == '__main__':
    main()
