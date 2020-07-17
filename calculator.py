import re
from itertools import chain
from pythonds.basic.stack import Stack
from collections import deque


def check_the_sign(numbers_arr):
    for i in range(1, len(numbers_arr), 2):
        if len(numbers_arr[i]) > 1:
            if numbers_arr[i][0] == '-':
                if len(numbers_arr[i]) % 2 != 0:
                    numbers_arr[i] = '-'
                else:
                    numbers_arr[i] = '+'
            else:
                numbers_arr[i] = '+'

    return numbers_arr


def convert_positive_num(user_input):
    input_arr = user_input.split(' ')
    for i, el in enumerate(input_arr):
        if el[0] == '+':
            input_arr[i] = el[1:]

    return user_input


def check_if_input_correct(user_input):
    if user_input[0] == '/' and (user_input != '/help' and user_input != '/exit'):
        print('Unknown command')
        return False

    input_arr = convery_to_array_2(user_input)

    op = ['^', '+', '-', '*', '/']
    count_p_l = 0
    count_p_r = 0
    for i, el in enumerate(input_arr):
        if i < len(input_arr)-1:
            if el in op and input_arr[i+1] in op and ((el != '+' and input_arr[i+1] != '+') or(el != '-' and input_arr[i+1] != '-')):
                print('Invalid expression')
                return False
            elif el == '(' and input_arr[i+1] == ')':
                print('Invalid expression')
                return False
            elif el == ')' and input_arr[i+1] == '(':
                print('Invalid expression')
                return False
            elif input_arr[len(input_arr) -1] in op:
                print('Invalid expression')
                return False

        if el == '(':
            count_p_l += 1
        elif el == ')':
            count_p_r += 1

    if count_p_l != count_p_r:
        print('Invalid expression')
        return False


    pattern_num = '[0-9]+'
    pattern_letter = '[A-Za-z]+'
    output = True

    if '=' in user_input:
        return True

    for count, el in enumerate(input_arr):

        if re.match(pattern_num, el):
            if el[len(el) - 1] == '+' or el[len(el) - 1] == '-':
                output = False
                return output
        elif re.match(pattern_num, el):
            if count < len(input_arr) - 1 and re.match(pattern_num, input_arr[count + 1]):
                output = False
                return output

    return output


def change_input_to_arr(user_input):
    input_arr = re.split('\s+', user_input)

    for i, el in enumerate(input_arr):
        if len(el) > 1:
            input_arr[i] = list(el)

    return list(chain.from_iterable(input_arr))


def check_input_correctness(input_arr, variables):

    equal_sign = 0
    if '=' in input_arr:
        for el in input_arr:
            if el == '=':
                equal_sign += 1
                if equal_sign > 1:
                    print('Invalid assignment')
                    return False

    if equal_sign == 1:
        equal_s_index = input_arr.index('=')
        first_part = ''.join(input_arr[:equal_s_index])
        last_part = ''.join(input_arr[equal_s_index + 1:])
        variable = ''.join(first_part)

        if re.match('^[a-zA-Z]+$', variable):
            if re.match('^[0-9]+$', ''.join(last_part)):
                value = int(''.join(last_part))
                variables[variable] = value
            elif re.match('^[a-zA-Z]+$', ''.join(last_part)):
                key = ''.join(last_part)
                if key in variables:
                    variables[variable] = variables[key]
                else:
                    print('Unknown variable')
                    return False
            elif re.match('^[a-zA-Z0-9]+$', ''.join(last_part)):
                print('Invalid assignment')
                return False
        elif re.match('^[a-zA-Z0-9]+$', ''.join(first_part)):
            print('Invalid identifier')
            return False


def display_var_value(user_input, variables):
    if user_input in variables:
        print(variables[user_input])
    else:
        print('Unknown variable')


def counvert_variable_to_number(input_arr, variables):
    for i, el in enumerate(input_arr):
        if el in variables:
            input_arr[i] = int(variables[el])
        elif not el.isdigit() and el not in ['^', '+', '-', '*', '/', '(', ')']:
            print('Unknown variable')
            break
    return input_arr


def convery_to_array_2(str):
    op = ['^', '+', '-', '*', '/', '(', ')']
    index = 0
    res = []
    for i in range(len(str)):
        if str[i] in op:
            res.append(str[index: i])
            res.append(str[i])
            index = i + 1
    res.append(str[index:len(str)])

    res = [x.strip() for x in res if x.strip() != '']

    return res


def infixToPostfix(infixexpr_arr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr_arr

    for token in tokenList:
        token = token.strip() # '33 ' -> '33'
        if re.match('^[a-zA-Z]+$', token) or re.match('^[0-9]+$', token):
            postfixList.append(token)
        elif re.match('^[a-zA-Z0-9]+$', token): # 'a22'
            print('Invalid identifier')
            break
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return postfixList


def calculate_result(postfix):
    op = ['^', '+', '-', '*', '/']
    equation = deque()

    for el in postfix:
        equation.append(el)

    for i, el in enumerate(equation):
        if el not in op:
            equation[i] = int(el)

    que_helper = deque()
    result = 0

    if len(equation) == 1:
        result = equation.pop()
    else:
        while len(equation) > 0:
            x = equation.popleft()
            if x not in op:
                que_helper.appendleft(x)
            else:
                b = que_helper.popleft()
                a = que_helper.popleft()
                if x == '^':
                    result = a ** b
                elif x == '*':
                    result = a * b
                elif x == '/':
                    result = a / b
                elif x == '+':
                    result = a + b
                elif x == '-':
                    result = a - b
                que_helper.appendleft(result)

    print(int(result))
    return result


###########################################
variables = {}
while True:

    user_input = input().strip()

    if user_input != '':
        if user_input[0] == '+':
            user_input = convert_positive_num(user_input)

        if check_if_input_correct(user_input):
            if user_input == '/exit':
                print('Bye!')
                break

            elif user_input == '/help':
                print('You can use +. -, /, *, ^ and define variables in this calculator')

            elif len(user_input) > 0:
                if '=' in user_input:
                    input_arr = change_input_to_arr(user_input)
                    check_input_correctness(input_arr, variables)

                elif re.match('^[a-zA-Z]+$', user_input):
                    display_var_value(user_input, variables)

                elif '=' not in user_input:
                    numbers_from_user = convery_to_array_2(user_input)
                    equation = check_the_sign(numbers_from_user)
                    numbers_equation = counvert_variable_to_number(equation, variables)
                    numbers_equation = [str(x) for x in numbers_equation]
                    postfix = infixToPostfix(numbers_equation)
                    calculate_result(postfix)

        else:
            print('Invalid expression')


