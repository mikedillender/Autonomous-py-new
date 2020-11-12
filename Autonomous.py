import clr
import sys
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
sys.path.append(r"c:\Users\liter\Desktop\engr100\Autonomous-py-new\Lib")
sys.path.append(r"c:\Users\liter\Desktop\engr100\Autonomous-py-new")
sys.path.append(r"c:\Users\Mike\CLionProjects\Autonomous-py-new\Lib")
sys.path.append(r"c:\Users\Mike\CLionProjects\Autonomous-py-new")


import time
from System.Drawing import Point
from System.Windows import Forms
import keyboard
#from graphics import *

'''
height=500
width=500
anchorpoint=Point(width/2,height/2)
#win = GraphWin("map_display_window", width, height)
image=Image(anchorpoint, height, width)

def draw():
    globals()
    rect=Rectangle(Point(0,0),Point(width,height))
    rect.setFill("white")
    rect.draw(win)
    for p in pos:
        c=Circle(Point(p[0],p[1]),2)
        c.setFill("red")
        #c.draw(win)
'''

def takeoff():
    if cs.armed:
        print ('Motors already armed')
    else:
        print('Arming motors')
        Script.ChangeMode('Autonomous')
        MAV.doARM(True)
        Script.Sleep(5000)

        print ('Initiating take-off')
        Script.SendRC(3, 1500 + Script.GetParam('THR_DZ'), True)
        Script.Sleep(10)
        Script.SendRC(3, 1500, True)

def land():
    if not cs.armed:
        print('Already landed')
    else:
        print('Landing')
        Script.ChangeMode('Land')

def disarm():
    if not cs.armed:
        print ('Motors already disarmed')
    else:
        print('Disarming motors')
        MAV.doARM(False)

# Main loop

running=True

def stop():
    global running
    disarm()
    running=False

keyboard.add_hotkey('esc', lambda: stop())
velx=0
vely=0
px=0
py=0

def main():
    globals()
    global velx,vely,px,py
    for channel in range(1, 9):
        Script.SendRC(channel, 1500, True)

    print('Running main')
    drawtime=0
    lasttime=time.time()
    while (running):
        drawtime+=1
        time.sleep(.01)
        dt=(time.time()-lasttime)/1000000.0
        velx=cs.ax*dt
        vely=cs.ay*dt
        px=velx*dt
        py=vely*dt
        print(str(px)+", "+str(py));
        lasttime=time.time()
        if (keyboard.is_pressed('shift')):
            print('SHIFTED')
        if (keyboard.is_pressed('up')):
            print('up')
        if (keyboard.is_pressed('down')):
            print('down')
        if(drawtime>20):
            #draw()
            drawtime=0
    land()


main()