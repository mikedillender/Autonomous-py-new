import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point
from System.Windows import Forms

# GUI window

class CommandBox(Forms.Form):
    def __init__(self):
        self.Text = "Command Box"

        self.Width = 350
        self.Height = 100

        self.takeoff_button = Forms.Button()
        self.takeoff_button.Text = 'Take-off'
        self.takeoff_button.Location = Point(20, 20)
        self.takeoff_button.Height = 25
        self.takeoff_button.Width = 80
        self.takeoff_button.Click += self.takeoff_click
        
        self.land_button = Forms.Button()
        self.land_button.Text = 'Land'
        self.land_button.Location = Point(110, 20)
        self.land_button.Height = 25
        self.land_button.Width = 80
        self.land_button.Click += self.land_click
        
        self.panic_button = Forms.Button()
        self.panic_button.Text = 'Panic!'
        self.panic_button.Location = Point(230, 20)
        self.panic_button.Height = 25
        self.panic_button.Width = 80
        self.panic_button.Click += self.panic_click

        self.CancelButton = self.panic_button

        self.Controls.Add(self.takeoff_button)
        self.Controls.Add(self.land_button)
        self.Controls.Add(self.panic_button)

    def takeoff_click(self, sender, event):
        takeoff()
    
    def land_click(self, sender, event):
        land()
    
    def panic_click(self, sender, event):
        disarm()

# Commands

def takeoff():
    if cs.armed:
        print 'Motors already armed'
    else:
        print('Arming motors')
        Script.ChangeMode('Autonomous')
        MAV.doARM(True)
        Script.Sleep(5000)

        print 'Initiating take-off'
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
        print 'Motors already disarmed'
    else:
        print('Disarming motors')
        MAV.doARM(False)

# Main loop

def main():
    for channel in range(1, 9):
        Script.SendRC(channel, 1500, True)
    print('Running main')
    form = CommandBox()
    Forms.Application.Run(form)
    land()

main()