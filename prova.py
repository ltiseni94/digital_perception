import sys
import os
import cv2

print(sys.path)
print(os.getcwd())

print("Hello World!")
a = 2 + 3
b = 4


def calc(c, d):
    return c*d, c+d


k = calc
print([k(a, a+1) for a in range(10)])

'''
Some useful opencv commands
cv2.line()
cv2.rectangle()
cv2.circle()
cv2.ellipse()
cv2.polylines()
cv2.putText()

Exercise
x^2 + 2x - 6 p(a)=b p(b)=a'''

sols = [(a, b,)
        for a in range(-1000, 1001) for b in range(-1000, 1001)
        if (((a**2 + 2*a - 6) is b) and ((b**2 + 2*b - 6) is a))]
