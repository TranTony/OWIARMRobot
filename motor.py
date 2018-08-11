#import the USB and Time librarys into Python
import usb.core, usb.util, time

ShoulderKey = "Shoulder"
ElbowKey = "Elbow"
WristKey = "Wrist"
GripKey = "Grip"
BaseKey = "Base"

#Motor class
class Status():
    def __init__(self):
        self.status = self.setStatusToIdle()
        
    def setStatusToIdle(self):
        self.status = 0
        return self.status
        
    def setStatusToRestricted(self):
        self.status = -1
        return self.status
        
    def setStatusToBusy(self):
        self.status = 1
        return self.status

class Motor():
    def __init__(self, typeOfMotor):
        global RoboArm
        RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x001)
        self.Flash = False
        if typeOfMotor is ShoulderKey:
            self.MotorType = ShoulderKey
            self.ClockWise = 0x40
            self.CounterClockWise = 0x80
            self.Stop = 0x00
            self.OrderOfByte = 0
            self.TriggerKey = 115 #s key
            self.status = Status()
        if typeOfMotor is ElbowKey:
            self.MotorType = ElbowKey
            self.ClockWise = 0x20 
            self.CounterClockWise = 0x10
            self.Stop = 0x00
            self.OrderOfByte = 0
            self.TriggerKey = 101 #e key
            self.status = Status()
        if typeOfMotor is WristKey:
            self.MotorType = WristKey
            self.ClockWise = 0x08 
            self.CounterClockWise = 0x04
            self.Stop = 0x00
            self.OrderOfByte = 0
            self.TriggerKey = 119 #w key
            self.status = Status()
        if typeOfMotor is GripKey:
            self.MotorType = GripKey
            self.ClockWise = 0x02
            self.CounterClockWise = 0x01
            self.Stop = 0x00
            self.OrderOfByte = 0
            self.TriggerKey = 103 #g key
            self.status = Status()
        if typeOfMotor is BaseKey:
            self.MotorType = BaseKey
            self.ClockWise = 0x02
            self.CounterClockWise = 0x01
            self.Stop = 0x00
            self.OrderOfByte = 1
            self.TriggerKey = 98 #b key
            self.status = Status()
            
        if RoboArm is None:
            raise ValueError("Arm not found")
        
    def whoIAm(self):
        print(self.MotorType)
        print(self.ClockWise)
        print(self.CounterClockWise)
        print(self.Stop)
        print(self.OrderOfByte)
        print(self.TriggerKey)
        print(self.status)
        print(self.Flash)
            
    def turnClockWise(self):
        self.MoveArm(self.ClockWise, self.OrderOfByte)
        self.status.setStatusToBusy()
        
    def turnCounterClockWise(self):
        self.MoveArm(self.CounterClockWise, self.OrderOfByte)
        self.status.setStatusToBusy()
        
    def turnSteady(self):
        self.MoveArm(self.Stop, None)
        self.status.setStatusToIdle()
    
    def turnFlash(self):
        self.Flash = not self.Flash
        self.MoveArm(self.Flash, 2)
        
    #global MoveArm
    def MoveArm(self, Cmd, OrderOfByte):
        ArmCMD = [0, 0, self.Flash]
        if OrderOfByte is None:
            RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCMD,3)
            print(ArmCMD)
        else:
            for x in range(len(ArmCMD)):
                if x is OrderOfByte:
                    ArmCMD[x] = Cmd
            print(ArmCMD)
            RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCMD,3)