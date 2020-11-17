import clr
import sys

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
#sys.path.append(r"c:\Users\liter\Desktop\engr100\Autonomous-py-new\Lib")
#sys.path.append(r"c:\Users\liter\Desktop\engr100\Autonomous-py-new")
sys.path.append(r"c:\Users\Mike\CLionProjects\Autonomous-py-new\Lib")
sys.path.append(r"c:\Users\Mike\CLionProjects\Autonomous-py-new\Lib\site-packages")
sys.path.append(r"c:\Users\Mike\CLionProjects\Autonomous-py-new")
sys.path.append(r"c:\users\mike\appdata\local\programs\python\python37-32\lib\site-packages")

#import numpy as np
import time
import math as m
from System.Drawing import Point
from System.Windows import Forms
import keyboard

p = [0, 0]
v = [0, 0]
vr = [0, 0]
a = [0, 0]
aer = [0, 0]
past = []
lid = []


def exportPast():
    #name = str(time.time()) + ".csv"
    for i in past:
        str1=""
        for d in i:
            str1=str1+str(d)+", "
        print(str1)
    #np.savetxt(name, past, delimiter=", ", fmt='% s')
    #p = [0, 0]


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
        print('Finished Takeoff Method')


def land():
    if not cs.armed:
        print('Already landed')
    else:
        print('Landing')
        Script.ChangeMode('Land')
    exportPast()


def disarm():
    if not cs.armed:
        print ('Motors already disarmed')
    else:
        print('Disarming motors')
        MAV.doARM(False)
    exportPast()


# Main loop

running = True


def stop():
    global running
    disarm()
    running = False
    exportPast()


keyboard.add_hotkey('esc', lambda: stop())


def updateLidar(lidset):
    lidset.append(time.time())
    lid.append(lidset)


def getLidarRates(num):
    globals()
    s = len(lid)
    rates = [0, 0, 0, 0]
    for l in range(4):
        samples = min(s - 1, num)
        for i in range(samples):
            rates[l] += (lid[s - i][l] - lid[s - i - 1][l]) / (lid[s - i][4] - lid[s - i - 1][4])
        rates[l] = rates[l] / samples
    return rates

def findRotDir():
    globals()
    orient=m.atan2([-cs.pitch,cs.roll])-(cs.yaw*3.14159/180)
    return orient

def main():
    globals()
    global v, p, a, aer, vr
    for channel in range(1, 9):
        Script.SendRC(channel, 1500, True)
    print('Running main')
    lasttime = time.time()
    aer = [cs.ax, cs.ay]
    method = 1
    while (running):
        time.sleep(.01)
        dt = (time.time() - lasttime)
        if (not cs.armed):
            for i in range(2):
                v[i] = 0
                vr[i] = 0
                a[i] = 0
            aer[0] = (aer[0] + .1 * cs.ax) / 1.1
            aer[1] = (aer[1] + .1 * cs.ay) / 1.1
        data=[dt, cs.ax, cs.ay, cs.pitch, cs.roll, cs.yaw, cs.airspeed, cs.groundspeed, cs.alt, aer[0], aer[1]]
        past.append(data)

        '''
        #flydir
        orient = 3.14159 * cs.yaw / 180
        if (method == 1):  # Method 1
            fa = [(cs.ax - aer[0])/100.0 * m.cos(orient),
                  (cs.ay - aer[1])/100.0 * m.cos(orient)]  # Subtracts error from before takeoff
            if (cs.armed):
                vn=[v[0], v[1]]
                for i in range(2):
                    a[i] = (a[i] * .5 + fa[i] * 1.5) / 2  # Slightly weighted to preventing rapid changes
                    vr[i] = v[i] + dt * a[i]  # Current calculated velocity

                speed = m.sqrt(vn[0] * vn[0] + vn[1] * vn[1])  # Calculated velocity
                scale = 0 if speed == 0 else cs.airspeed / speed
                vnr = [vn[0] * scale, vn[1] * scale]

                for i in range(2):
                    p[i] = p[i] + dt * (vr[i] + vnr[
                        i]) / 2  # Calculates average velocity over delta and uses that to compute pos
                    v[i] = vn[i]  # sets old speed as new speed
                    vr[i] = vnr[i]  # sets old real speed as new speed

                past.append([p[0], p[1]])

            else:  # Runs when not flying, measures current error
                for i in range(2):
                    v[i] = 0
                    vr[i] = 0
                    a[i] = 0
                aer[0] = (aer[0] + .1 * cs.ax) / 1.1
                aer[1] = (aer[1] + .1 * cs.ay) / 1.1
                #print("error = " + str(aer[0]) + ", " + str(aer[1]))
        #elif(method==2):
        '''
        '''TODO: Other possible approaches:
            -Measure rate of change of lidar to estimate velocity
            -use current orientation to determine flight direction
        '''
        if(keyboard.is_pressed('p')):
            print (cs.messages)
        lasttime = time.time()
        if (keyboard.is_pressed('up')):
            takeoff()
        if (keyboard.is_pressed('down')):
            land()
    land()


main()
