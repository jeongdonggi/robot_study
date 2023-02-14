import cv2 as cv
import numpy as np

def mouse_callback(event, x, y, flags, param):
    if event == 1:
        print('B: ', param[y][x][0], '\nG: ', param[y][x][1], '\nR: ', param[y][x][2]) # RGB 표현
        print('=================================')


Path = 'Data/'
Name = 'rabong.jpg'
FullName = Path + Name

# 이미지 읽기
img = cv.imread(FullName)

img1 = img.copy()
#
#
# 여기에 소스코드 작성
# 0 < B < 50 150 >G> 100
# 230 > R > 190
list = [0,0,0,0]
max = 0
num = 0
for y in range(img1.shape[0]):
    for x in range(img1.shape[1]):
        if (img1[y][x][0] >= 0) and (img1[y][x][1] >= 60) and (img1[y][x][2] >= 90):
            img1[y][x][2] = 255
            img1[y][x][1] = 0
            img1[y][x][0] = 0
            if y >= 0 and y < 256 and x > 256 and x < 512: # 1사분면
                list[0] += 1
            elif y >= 0 and y < 256 and x >= 0 and x < 256: # 2사분면
                list[1] += 1
            elif y > 256 and y < 512 and x >= 0 and x < 256: # 3사분면
                list[2] += 1
            elif y > 256 and y < 512 and x > 256 and x < 512: # 4사분면
                list[3] += 1

for i in range(4):
    if list[i] > max:
        max = list[i]
        num = i+1

print(num)
# 이미지 출력
cv.imshow('img', img1)
#cv.imshow('gray1', gray1)
#cv.imshow('gray', gray)
#cv.imshow('blur', blur)


while cv.waitKey(33) <= 0:
    cv.setMouseCallback('img', mouse_callback, img1)

cv.waitKey(0)
