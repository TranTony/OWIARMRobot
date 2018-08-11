#import the USB and Time librarys into Python
import usb.core, usb.util, time
import pyxhook
import motor
 
#Allocate the name 'RoboArm' to the USB device
ShoulderKey = "Shoulder"
ElbowKey = "Elbow"
WristKey = "Wrist"
GripKey = "Grip"
BaseKey = "Base"
LED = "LED"

Motor = None


#Allocate key on keyboard for controlling kinds of motor

default_For_Finish_Program = "default_For_Finish_Program"
default_For_Down_Right_Close = "default_For_Down_Right_Close"
default_For_Up_Left_Open = "default_For_Up_Left_Open"
typeOfMovement = {
    default_For_Finish_Program: 96, #` for escape from program
    default_For_Down_Right_Close: 111, #Downwards Arrow for Down/Right/Close of movement
    default_For_Up_Left_Open: 116, #Upwards Arrow for Up/Left/Open of movement
}
    
def KeyBoardListener():
    new_hook=pyxhook.HookManager()
    #listen to all keystrokes
    new_hook.KeyDown=eventDownChecker
    new_hook.KeyUp=eventUpChecker
    #hook the keyboard
    new_hook.HookKeyboard()
    #start the session
    new_hook.start()
    
    return new_hook
    
def eventDownChecker(event):
    global Motor
    if event.Ascii is 115:
        Motor = motor.Motor(ShoulderKey)
        print("Initialize Motor on Shoulder")
    if event.Ascii is 101:
        Motor = motor.Motor(ElbowKey)
        print("Initialize Motor on Elbow")
    if event.Ascii is 119:
        Motor = motor.Motor(WristKey)
        print("Initialize Motor on Wrist")
    if event.Ascii is 103:
        Motor = motor.Motor(GripKey)
        print("Initialize Motor on Grip")
    if event.Ascii is 98:
        Motor = motor.Motor(BaseKey)
        print("Initialize Motor on Base")
    if event.Ascii is 108:
        if Motor is None:
            print("Please initialize Motor before control LED")
        else:
            Motor.turnFlash()
    if event.ScanCode is typeOfMovement[default_For_Down_Right_Close]:
        if Motor is None:
            print("Please initialize Motor before control")
        else:
            Motor.turnClockWise()
    if event.ScanCode is typeOfMovement[default_For_Up_Left_Open]:
        if Motor is None:
            print("Please initialize Motor before control")
        else:
            Motor.turnCounterClockWise()
    if event.Ascii is typeOfMovement[default_For_Finish_Program]:
        print("My mission is complated, I'm out")      
        new_hook.cancel()
        
def eventUpChecker(event):
    if event.ScanCode is typeOfMovement[default_For_Down_Right_Close]:
        Motor.turnSteady()
    if event.ScanCode is typeOfMovement[default_For_Up_Left_Open]:
        Motor.turnSteady()

new_hook = KeyBoardListener()
