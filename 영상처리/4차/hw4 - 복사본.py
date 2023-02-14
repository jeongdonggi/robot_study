import math
import cv2 as cv
import numpy as np

# =============================== 데이터 불러오기 ====================================#

file = 'Data/drive.mp4'
cap = cv.VideoCapture(file)
Nframe = 0  # frame 수

# ================================== 메인 루틴 =====================================#

def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅
    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지
    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1
    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv.fillPoly(mask, vertices, color)
    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv.bitwise_and(img, mask)
    return ROI_image

while cap.isOpened():
    ret, frame = cap.read()

    if ret:  # 비디오 프레임을 읽기 성공했으면 진행
        frame = cv.resize(frame, (1000, 562))
    else:
        break

    Nframe += 1
    origin = np.copy(frame)

# ================================== 코드 짜기 =====================================#
# 1. 가우시안 블러
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray_img, (0, 0), 1)

# 2. 캐니 추출
    canny = cv.Canny(gaussian, 17, 20, 3)

# 3. ROI 추출
    point = np.array([[400, 200], [600, 200], [1000, 500], [0, 500]])
    ROI = region_of_interest(canny, [point])

# 4. 허프 변환
    lines = cv.HoughLines(ROI, 1, np.pi / 180, 270) # 이미지, r값의 범위 (0~1), Theta값의 범위(0~180), 임계치

    if lines is not None: # 현재 프레임에서 직선이 검출 되었을 때
        for i in range(0, len(lines)):
            r = lines[i][0][0] # 검출된 부분 R
            theta = lines[i][0][1] # 검출된 부분 Theta

            # 극좌표계 직선의 방정식 계산
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * r
            y0 = b * r

            # 직선을 그릴 기준 점 2개 좌표 계산 (화면 밖 범위의 점으로 하는 것)
            # 직선 방정식으로 그리기 위한 시작점, 끝점 계산
            pt1 = (int(x0 + 2000 * (-b)), (int(y0 + 2000 * a)))  # 2000은 임시 R: 길이를 최대로 해줌
            pt2 = (int(x0 - 2000 * (-b)), (int(y0 - 2000 * a)))
            cv.line(frame, pt1, pt2, (255, 0, 0), 2, cv.LINE_AA)

# ===================================================================================#
    cv.imshow('original', ROI)  # 원본영상
    cv.imshow('result', frame)

    if cv.waitKey(1) & 0xff == ord('q'):  # 'q'누르면 영상 종료
        break

print("Number of Frame: ", Nframe)  # 영상의 frame 수 출력

cap.release()
cv.destroyAllWindows()
