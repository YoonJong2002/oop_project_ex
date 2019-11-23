import pygame
import numpy as np

srf_h = 700
srf_w = 500
srf = pygame.display.set_mode((srf_h, srf_w))

coin_size = 30
coin_img = pygame.image.load("coin.png")
coin_img_set = pygame.transform.scale(coin_img, (coin_size, coin_size))

bucket_w = 100
bucket_h = 80
bucket_img = pygame.image.load("bucket.png")
bucket_img_set = pygame.transform.scale(bucket_img, (bucket_h, bucket_w))

dt = 0.05
t = 0
v = 0
x = 30 * np.pi / 180    # x는 rad 단위
pen_fm = 0.01
pen_m = 0.1
pen_l = 100 * 0.01
pen_J = 0.02
pen_g = 9.8
gndCenterX = 350
gndCenterY = 20
penLength = pen_l * 100 * 2
updatedX = updatedY = 0


def keyboard():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 1
        if event.type == pygame.KEYDOWN:
            return 2


def calcODEFunc(tVal, xVal, vVal):
    return -pen_fm / (pen_m * pen_l * pen_l + pen_J) * vVal - pen_m * pen_g * pen_l / (
                pen_m * pen_l * pen_l + pen_J) * xVal


# Runge Kutta 미방 함수 구현하기
def solveODEusingRK4(t, x, v):
    kx1 = v
    kv1 = calcODEFunc(t, x, v)

    kx2 = v + dt * kv1 / 2
    kv2 = calcODEFunc(t + dt / 2, x + dt * kx1 / 2, v + dt * kv1 / 2)

    kx3 = v + dt * kv2 / 2
    kv3 = calcODEFunc(t + dt / 2, x + dt * kx2 / 2, v + dt * kv2 / 2)

    kx4 = v + dt * kv3
    kv4 = calcODEFunc(t + dt, x + dt * kx3, v + dt * kv3)

    dx = dt * (kx1 + 2 * kx2 + 2 * kx3 + kx4) / 6
    dv = dt * (kv1 + 2 * kv2 + 2 * kv3 + kv4) / 6

    return x + dx, v + dv


class BasicCoin:
    def __init__(self, cost, level):
        self.cost = cost
        self.level = level

    def coin_swing(self, screen, stringlength):
        """
            실이 잘리기 전 동전의 진자운동을 구현
            :param screen: 출력에 사용할 스크린
            :return: 없음(?????) 혹은 동전의 다음 x좌표, y좌표????
        """
        global loopFlag, bucketX, bucket_v, dX, t, x, v, updatedX, updatedY
        while loopFlag:
            if keyboard() == 2:
                loopFlag = False

            srf.fill((255, 255, 255))

            [bucketX, bucket_v, dX] = bucket_moves(bucketX, bucket_v, dX)  # bucket 의 이동.

            t = t + dt
            [x, v] = solveODEusingRK4(t, x, v)  # x 는 각변위
            updatedX = gndCenterX + penLength * np.sin(x)
            updatedY = gndCenterY + penLength * np.cos(x)

            pygame.draw.line(srf, (0, 0, 0), (10, 20), (700, 20), 10)  # 줄이 매달린 천장
            pygame.draw.line(srf, (100, 100, 100), (gndCenterX, gndCenterY), (updatedX, updatedY), 2)  # 줄
            srf.blit(coin_img_set, (int(updatedX) - 15, int(updatedY) - 15))  # 동전
            pygame.draw.line(srf, (100, 0, 100), (int(updatedX), int(updatedY)),
                             (int(updatedX + penLength * v * np.cos(-x)), int(updatedY + penLength * v * np.sin(-x))),
                             2)  # 속도 벡터 표시

            pygame.display.update()  # 동전은 image, update 를 해야 보임
            pygame.time.delay(40)
            pygame.display.flip()


    def coin_fall(self, screen):
        """
            실이 잘린 후 동전의 포물선 운동을 구현
            :param screen: 출력에 사용할 스크린 # 필요에 따라 매개변수 추가 부탁!!!!
            :return: bucket과의 교점의 x좌표, y좌표(?????????) -> 충돌했는지 판단은 did_coin_enter
        """
        global neworiginY, neworiginX, bucketX, bucket_w, bucket_v, updatedX, updatedY, loopFlag, v_x, v_y, t, dX
        while loopFlag:
            if keyboard() == 2:
                loopFlag = False

            if neworiginY + updatedY >= srf_h - bucket_h:  # neworiginY + updatedY : 코인 중심의 Y, srf_h - bucket_h : 버킷 윗면의 높이
                if abs((int(updatedX + neworiginX)) - (
                        bucketX + bucket_w / 2)) <= bucket_w / 2:  # updatedX+neworiginX : 코인의 중심 X , bucketX + bucket_w/2 : bucket 중심 X
                    print('yay')
                else:
                    print('aww')
                break

            srf.fill((255, 255, 255))
            t = t + dt
            updatedX = v_x * t
            updatedY = v_y * t + 0.5 * 700 * t ** 2
            srf.blit(coin_img_set, (int(updatedX + neworiginX) - 15, int(updatedY + neworiginY) - 15))  # 날라가는 동전
            [bucketX, bucket_v, dX] = bucket_moves(bucketX, bucket_v, dX)  # bucket

            pygame.time.delay(40)
            pygame.display.flip()


    def did_coin_enter(self):
        """
            coin_fall 메서드에서 받은 매개변수를 이용하여 동전을 획득했는지 판단
            :param ?????????: 동전 획득 여부를 판단하니 위한 매개변수
            :return: 동전을 획득한 경우 True, 획득하지 못한 경우 False를 반환
        """
        if abs((int(updatedX + neworiginX)) - (
                bucketX + bucket_w / 2)) <= bucket_w / 2:  # updatedX+neworiginX : 코인의 중심 X , bucketX + bucket_w/2 : bucket 중심 X
            print('yay')
        else:
            print('aww')


class EasyCoin(BasicCoin):
    def __init__(self, cost):
        self.cost = cost
        self.stringlength = 10  # 코드 돌려보면서 적절히 쉬운 길이로 조절 부탁!
        # self.image = # 이미지 파일 삽입하는 방법 등..?


class MediumCoin(BasicCoin):
    def __init__(self, cost, level):
        self.cost = cost
        self.level = level
        self.stringlength = 10 - level  # 코드 돌려보면서 적절히 길이 조절 부탁!
        # self.image = # 이미지 파일 삽입하는 방법 등..?


class HardCoin(BasicCoin):
    def __init__(self, cost, level):
        self.cost = cost
        self.level = level
        self.stringlength = 10 - level*2  # 얘도 코드 돌려보면서 길이 조절 부탁!
        # self.image = # 이미지 파일 삽입?