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
'''
from graphics import *
height=500
width=500
anchorpoint=Point(width/2,height/2)
win = GraphWin("map_display_window", width, height)
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

p=[0,0]
v=[0,0]
a=[0,0]
aer=[0,0]

def main():
    globals()
    global v,p,a,aer
    for channel in range(1, 9):
        Script.SendRC(channel, 1500, True)

    print('Running main')
    lasttime=time.time()
    aer=[cs.ax,cs.ay]
    method=1
    while (running):
        time.sleep(.01)
        dt=(time.time()-lasttime)

        if(method==1):#Method 1
            fa = [cs.ax-aer[0], cs.ay-aer[1]] # Subtracts error from before takeoff
            if (cs.armed):
                vn=[0,0];
                for i in range(2):
                    a[i]=(a[i]*.5+fa[i]*1.5)/2 # Slightly weighted to preventing rapid changes
                    vn[i]=v[i]+dt*a[i] # Current calculated velocity
                    p[i]=p[i]+dt*(v[i]+vn[i])/2 # Calculates average velocity over delta and uses that to compute pos
                    v[i]=vn[i] # sets old speed as new speed
                speed=sqrt(v[0]*v[0]+v[1]*v[1]) # Calculated velocity
                measuredspeed=cs.airspeed # Measured Velocity
                # If we can get speed and measured speed in the same units,
                # we can then scale down the calculated speed so they have the same magnitude

            else: # Runs when not flying, measures current error
                aer[0]=(aer[0]+.1*cs.ax)/1.1
                aer[1]=(aer[0]+.1*cs.ax)/1.1
                print("error = "+str(aer[0])+", "+str(aer[1]))



        print (cs.messages)
        lasttime=time.time()
        if (keyboard.is_pressed('up')):
            takeoff()
        if (keyboard.is_pressed('down')):
            land()
    land()


main()