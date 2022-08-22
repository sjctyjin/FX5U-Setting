import pyautogui
import time
import keyboard
#目前滑鼠坐標
pyautogui.position()
print(pyautogui.position())
#目前螢幕解析度
pyautogui.size()
#(x,y)是否在螢幕上
# moveToX, moveToY = 1550, 434
moveToX, moveToY = 1744, 447 #click

x,y = 10,10
# print(pyautogui.onScreen(x, y))
num_seconds = 1.2
#
#


# cx, cy = -300, 300
# pyautogui.moveTo(cx, cy, duration=num_seconds)
# pyautogui.moveTo(moveToX, moveToY, duration=num_seconds)
#
# # pyautogui.moveRel(xOffset, xOffset, duration=num_seconds)
# pyautogui.doubleClick(x=xOffset, y=yOffset)
# pyautogui.leftClick(x=cx, y=cy)
def Reborn(xOffset,yOffset):
    AvatarX, AvatarY = 1014, 297

    pyautogui.doubleClick(AvatarX, AvatarY, duration=num_seconds)
    rebornX, rebornY = 1050, 875 #reborn
    CrebornX, CrebornY = 1430, 718 #reborn confirm

    pyautogui.moveTo(xOffset, yOffset, duration=num_seconds)

    for i in range(50):
        pyautogui.scroll(-29999)
    pyautogui.doubleClick(rebornX, rebornY, duration=num_seconds)
    # pyautogui.leftClick(rebornX, rebornY, duration=num_seconds)
    time.sleep(1)

    pyautogui.doubleClick(CrebornX, CrebornY, duration=num_seconds)
    pyautogui.doubleClick(CrebornX, CrebornY, duration=num_seconds)
    # time.sleep(10)
    pyautogui.scroll(122000)

# pyautogui.scroll(2200)


def Touch(tachx,taxhy):

    while(True):

        # tachx,taxhy = -684,550
        # pyautogui.moveTo(tachx, taxhy, duration=num_seconds)
        pyautogui.doubleClick(x=tachx, y=taxhy)
        if pyautogui.position().x != tachx:
            print("退出連點")
            break
        if keyboard.is_pressed("q"):
            print("You pressed q")
            break
def Hero():
    HeroX, HeroY = 1119, 292
    AvatarX, AvatarY = -1073, 231
    cx, cy = -300, 300
    # AvatarX, AvatarY = -905, 330
    # pyautogui.leftClick(cx, cy, duration=num_seconds)
    time.sleep(1)
    # pyautogui.doubleClick(AvatarX, AvatarY, duration=num_seconds)
    pyautogui.doubleClick(HeroX, HeroY, duration=num_seconds)
    pyautogui.moveTo(HeroX, 400, duration=num_seconds)
    pyautogui.scroll(1000000)
    UpgradX = [[1020, 488],[1020, 637],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793],[1020, 793]]
    for i in range(len(UpgradX)):
        # if i == 4:
        #     break
        if keyboard.is_pressed("q"):
            print("You pressed q")
            break
        if i > 2 :
            break
            #pyautogui.scroll(-450)

            # pyautogui.scroll(-445-(i*3))


        for x in range(20):
            pyautogui.doubleClick(x=UpgradX[i][0], y=UpgradX[i][1])
            print(f"英雄{i}_升級{x*100}")
            if keyboard.is_pressed("q"):
                print("You pressed q")
                break



    pyautogui.leftClick(cx, cy, duration=num_seconds)
#q
def AutoFight(s):
    AvatarX, AvatarY = 1014, 297
    while(True):
        s  +=1
        if s < 2300:
            pyautogui.doubleClick(x=moveToX, y=moveToY)
            pyautogui.doubleClick(x=moveToX, y=moveToY)
            print(s)
            if s < 1500:
                if s % 100 == 0:
                    # time.sleep(1)
                    pyautogui.moveTo(AvatarX, AvatarY, duration=0.5)
                    pyautogui.doubleClick(AvatarX, AvatarY, duration=0.5)
                    pyautogui.moveTo(AvatarX, yOffset + 10)
                    pyautogui.scroll(2250)
                    pyautogui.doubleClick(x=xOffset, y=yOffset)
                    print("升級100")
                    # pyautogui.leftClick(x=cx, y=cy)
            elif  s > 1500 and s < 1800:
                if s % 10 == 0:
                    # time.sleep(1)
                    pyautogui.moveTo(AvatarX, AvatarY, duration=0.1)
                    pyautogui.doubleClick(AvatarX, AvatarY, duration=0.1)
                    pyautogui.moveTo(AvatarX, yOffset+10)
                    pyautogui.scroll(2250)
                    pyautogui.doubleClick(x=(xOffset+100), y=yOffset)
                    print("升級10")
                    # pyautogui.leftClick(x=cx, y=cy)
                if  s % 15 == 0:
                    pyautogui.moveTo(AvatarX, AvatarY, duration=0.1)
                    pyautogui.doubleClick(AvatarX, AvatarY, duration=0.1)
                    pyautogui.moveTo(AvatarX, yOffset + 10)
                    pyautogui.scroll(2250)
                    pyautogui.doubleClick(x=(xOffset + 200), y=yOffset)
                    # pyautogui.leftClick(x=cx, y=cy)
                    print("升級1")

        elif s > 2300:
            # time.sleep(25)
            # DX, DY = -300, 300
            # pyautogui.leftClick(DX, DY, duration=num_seconds)
            Hero()
            Reborn(xOffset, yOffset)
            s = 0
        # if pyautogui.position().x != moveToX:
        #     print("退出連點")
        #     break
        if keyboard.is_pressed("q"):
            print("You pressed q")
            break
        if keyboard.is_pressed("a"):#切換BOSS
            DX0, DY0 = 1782, 360
            pyautogui.leftClick(DX0, DY0)
            print("You pressed a")
        if keyboard.is_pressed("z"):
            DX1, DY1 = -1003, 581
            pyautogui.doubleClick(DX1, DY1)
            print("You pressed z")
        if keyboard.is_pressed("x"):
            DX2, DY2 = -1003, 738
            pyautogui.doubleClick(DX2, DY2)
            print("You pressed x")


if __name__ == '__main__':
    xOffset, yOffset = 1012, 513  # upgrade
    s = 1580

    # while (True):
    #     print("X座標:", pyautogui.position().x)
    #     print("Y座標:", pyautogui.position().y)
    #     print("=" * 30)
    #     time.sleep(1)

    AvatarX, AvatarY = 1014, 297
    x = input("請輸入代碼")
    # time.sleep(3)
    # AvatarX, AvatarY = -301, 300
    # pyautogui.leftClick(AvatarX, AvatarY, duration=0.5)
    # pyautogui.scroll(-350)
    # time.sleep(3)ㄆ
    # pyautogui.scroll(-350)

    # time.sleep(3)
    # pyautogui.scroll(-350)
    # time.sleep(3)
    # pyautogui.scroll(-350)
    # time.sleep(3)
    # print(pyautogui.position().x,pyautogui.positiㄆon().y)

    if x == "q":
        time.sleep(3)
        Touch(pyautogui.position().x,pyautogui.position().y)
        print("開始連點")
    if x == "w":
        AutoFight(s)
        print("開始自動攻擊")
    if x == "e":
        Hero()
        print("英雄升級")
    if x == "r":
        Reborn(xOffset, yOffset)
        print("重生")
    # time.sleep(3)
    # Touch(pyautogui.position().x,pyautogui.position().y)
    # AutoFight(s)
    # Hero()
    # Reborn(xOffset, yOffset)
    # AvatarX, AvatarY = -905, 330
    # pyautogui.leftClick(AvatarX, AvatarY, duration=num_seconds)
    # Reborn(xOffset,yOffset)

# #     # time.sleep(2)
#
