import serial
import numpy as np

INT16_MIN = -32768
INT16_MAX = 32767
UINT16_MIN = 0
UINT16_MAX = 65535


class SerialHandler:
    header = 0xaa

    # TODO

    def send(self, data):
        data.insert(0, self.header)
        chksum = sum(data) % 65536

        data.append((chksum >> 8) & 0xff)
        data.append(chksum & 0xff)

        # TODO these checks might slow down the process but for now they are important
        if len(data) != 12 or max(data) > 255 or min(data) < 0:
            print("error, invalid data")
            return
        print(data)


class MotorDriver:
    serialHandler = SerialHandler()
    deviceID = 0x0c
    directMovements = [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17]
    directMovementsActivated = False

    # def __init__(self):
    #     self.positionRatio = None
    #     self.velocityRatio = None
    #     self.powerRatio = None
    #
    # def setPositionRatio(self, positionRatio):
    #     self.positionRatio = positionRatio
    #
    # def setVelocityRatio(self, velocityRatio):
    #     self.velocityRatio = velocityRatio
    #
    # def setPowerRatio(self, powerRatio):
    #     self.powerRatio = powerRatio

    def driveMotors(self, MovementIDs: list[int], MovementRatioModifiers: list[float], positionRatio: int,
                    velocityRatio,
                    powerRatio, options: int):

        if len(MovementIDs) != len(MovementRatioModifiers):
            print("some movement IDs have no ratios")
            return
        # create package(s)
        for i in range(len(MovementIDs)):

            # if it's a direct movement request, send 0x10 once before sending packages
            if MovementIDs[i] in self.directMovements:
                if not self.directMovementsActivated:
                    self.directMovementsActivated = True
                    data = [0 for tmp in range(9)]
                    data[0] = self.deviceID
                    data[1] = 0x10
                    self.serialHandler.send(data)
            else:
                self.directMovementsActivated = False

            # transform ratios to whatever Dávid asks
            # apply modifiers
            newPositionRatio = round(positionRatio * MovementRatioModifiers[i])
            newVelocityRatio = abs(round(velocityRatio * MovementRatioModifiers[i]))  # absolute value because UINT
            newPowerRatio = abs(round(powerRatio * MovementRatioModifiers[i]))  # absolute value because UINT

            # limit in the usable range
            newPositionRatio = min(max(newPositionRatio, INT16_MIN), INT16_MAX)
            newVelocityRatio = min(max(newVelocityRatio, UINT16_MIN), UINT16_MAX)
            newPowerRatio = min(max(newPowerRatio, UINT16_MIN), UINT16_MAX)

            # overwrite position for now TODO delete this if possible
            newPositionRatio = INT16_MAX if newPowerRatio > (UINT16_MIN + UINT16_MAX) / 2 else INT16_MIN

            data = [self.deviceID,
                    MovementIDs[i],
                    options,
                    (newPositionRatio >> 8) & 0xff,
                    newPositionRatio & 0xff,
                    (newVelocityRatio >> 8) & 0xff,
                    newVelocityRatio & 0xff,
                    (newPowerRatio >> 8) & 0xff,
                    newPowerRatio & 0xff,
                    ]
            self.serialHandler.send(data)
