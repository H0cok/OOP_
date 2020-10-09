import re
import numpy
def floatinput(a):
    while not (re.match('^([ +-]{0,1}[0-9,]{1,10}[.]{0,1}[,0-9]{0,10}){0,}$',a)):
        a = input('введіть тільки дійсні числа розділяючи їх комою \n')
    return a
def matrix():
    count = 1
    matr1x=[]
    a = floatinput(input('Введіть рядок матриці розділяючи елементи комою\n'))
    matr1x.append(re.split(',',a))
    print('Матриця - ' , numpy.array(matr1x))
    lens = len(re.split(',', a))
    while not count == lens:
        lens = len(re.split(',',a))
        a = floatinput(input('Введіть рядок матриці розділяючи елементи комою\n'))
        while not (len(re.split(',',a)) == lens) :
            a = input('введіть правильну кількість елементів\n')
        matr1x.append(re.split(',',a))
        print('Ваша матриця\n' , numpy.array(matr1x))
        count+=1
    return matr1x
def determinant(list):
    if len(list) == 1:
        det = (list[0])[0]
        return det
    if len(list) == 3:
            det = float((list[0])[0]) * float((list[1])[1])*float((list[2])[2]) + float((list[0])[1]) * float((list[1])[2])* float((list[2])[0])+  float((list[0])[2])* float((list[1])[0])* float((list[2])[1]) -  float((list[0])[2])* float((list[1])[1])* float((list[2])[0])- float((list[0])[1])* float((list[1])[0])* float((list[2])[2])- float((list[0])[0])* float((list[2])[1])* float((list[1])[2])
            return det
    det = 0
    for ind in range(0, len(list[0])):
        list1 = []
        num = float((list[0])[ind])
        for i in list:
            p = i[0:ind]
            m = i[ind + 1:]
            for i in m:
                p.append(i)
            list1.append(p)
        del list1[0]
        p = list1
        det =det +((-1)**(ind+2))*num * float(determinant(p))
    return det
def choice():
    answer = input('Якщо ви хочете продовжити роботу натисніть Y, якщо ні, натисніть N \n')
    if answer == 'Y':
        a = matrix()
        print(determinant(a))
        choice()
    if answer == 'N':
        print('До побаченя')
    else:
        choice()
a = matrix()
print('Визначник матриці - ' , determinant(a))
choice()

