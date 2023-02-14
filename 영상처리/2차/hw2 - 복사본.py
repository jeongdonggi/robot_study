import cv2 as cv
import numpy as np

Path = 'Data/'
Name = 'lenna.tif'
src = Path + Name

color_img = cv.imread(src)
image = cv.imread(src, cv.IMREAD_GRAYSCALE) # 에지 검출을 위해 그레이 스케일로 바꿈

#로버츠: 공식이 간단하여 계산 속도가 빠름, 사선 경계 검출 효과를 높이지만 노이즈에 민감하다는 단점이 있다.
#=====================================================================================
#img = image.copy()
# # 1. 로버츠 커널 생성
# gx_kernel = np.array([[1,0], [0,-1]])
# gy_kernel = np.array([[0, 1],[-1,0]])
# # 2. 커널 적용, 두개를 구해서 더함
# edge_gx = cv.filter2D(img, -1, gx_kernel)
# edge_gy = cv.filter2D(img, -1, gy_kernel)
# edge = edge_gy + edge_gx
# # 3. 결과 출력
# # merged = np.hstack((img, edge_gx, edge_gy, edge_gx+edge_gy)) # hstack 배열 가로 결합, vstack 배열 세로 결합
# cv.imshow('roberts', edge)
# cv.waitKey(0)
# cv.destroyAllWindows()
#=====================================================================================

#프리윗: 소벨보다 간단하여 속도가 빠르지만 로버츠보다 더 좋은 에지를 검출 할 수 있음, x축과 y축의 각 방향으로 차분을 세 번 계산 하여 경계를 검출하는 필터, 상하/좌우는 뚜렷하게 검출하지만 대각선 검출에 약함
#=====================================================================================
#img = image.copy()
# # 1. 프리윗 커널 생성
# gx_k = np.array([[-1,0,1], [-1,0,1],[-1,0,1]])
# gy_k = np.array([[-1,-1,-1],[0,0,0], [1,1,1]])
#
# # 2. 프리윗 커널 필터 적용
# edge_gx = cv.filter2D(img, -1, gx_k)
# edge_gy = cv.filter2D(img, -1, gy_k)
# edge = edge_gy + edge_gx
#
# # 3. 결과 출력
# cv.imshow('prewitt', edge)
# cv.waitKey(0)
# cv.destroyAllWindows()
#=====================================================================================

#소벨: 매우 뚜렷한 에지 검출, 중심 픽셀의 차분 비중을 두배로 준 필터라 다방면으로 강함(가우시안 처럼 가운데 값이 높다)
# 소벨 필터 함수: cv2.Sobel(입력 영상, 출력 영상의 데이터 타입, 미분 차수, 커널 크기, 미분에 사용할 계수, 연산 결과에 가산할 값)
# 미분 크기는 0,1,2 중 선택, 커널 크기는 1,3,5,7 중 선택
#=====================================================================================
img = image.copy()
# 1. 소벨 커널 생성
gx_k = np.array([[-1,0,1], [-2,0,2],[-1,0,1]])
gy_k = np.array([[-1,-2,-1],[0,0,0], [1,2,1]])

# 2-1. 소벨 필터 적용
edge_gx = cv.filter2D(img, -1, gx_k)
edge_gy = cv.filter2D(img, -1, gy_k)
edge = edge_gy + edge_gx

# 2-2. 소벨 함수 적용
sobelx = cv.Sobel(img, -1, 1, 0, ksize=3)
sobely = cv.Sobel(img, -1, 0, 1, ksize=3)
sobel = sobely + sobelx
# 3. 결과 출력
merged = np.concatenate((edge, sobel), 1) # 0이면 세로 1이면 가로
cv.imshow("sobel", merged)
cv.waitKey(0)
cv.destroyAllWindows()
#=====================================================================================