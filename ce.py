import struct
import ctypes
import random
import os
import time
import sys

ceResultFilePath = os.path.join(os.path.dirname(__file__), 'ceResult.txt')
ceBinExePath = os.path.join(os.path.dirname(__file__), "ce", "ce.exe")
ceTrainerPath = os.path.join(os.path.dirname(__file__), "trainer.CETRAINER")
ceServer = r'\\.\pipe\something9'

class CEClient:
    name: str

    def __init__(this, name) -> None:
        this.name = name
        this.evalFileScript(os.path.join(
            os.path.dirname(__file__), 'celua\\auto.lua'))
        this.evalScript('\n'.join([
            "ceResultPath = \"{}\"".format(ceResultFilePath)
            .replace('\\', '\\\\'),
        ]))
        pass

    def readCurrentContent(this):
        if not os.path.exists(ceResultFilePath):
            return ""
        f = open(ceResultFilePath, 'r')
        result = ''.join(f.readlines())
        f.close()
        this.clearContentTxt(False)
        return result

    def clearContentTxt(this, isCheck=True):
        if isCheck and not os.path.exists(ceResultFilePath):
            return
        os.remove(ceResultFilePath)
        return

    def waitContent(this):
        while (not os.path.exists(ceResultFilePath)):
            time.sleep(0.1)
        return this.readCurrentContent()

    def getServer(this):
        try:
            return open(ceServer, 'wb')
        except:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", ceBinExePath, ceTrainerPath, None, 1)
            while True:
                try:
                    return open(ceServer, 'wb')
                except:
                    continue

    def evalFileScript(this, filePath: str):
        if not os.path.exists(filePath):
            print('file not exists:', filePath)
            return ""
        f = open(filePath, 'r')
        content = ''.join(f.readlines())
        f.close()
        this.evalScript(content)
        return

    def evalScript(this, script: str):
        f = this.getServer()
        lua = script.encode()
        csz = len(lua)
        tosend = struct.pack("<bi"+str(csz)+"sq", 1, csz, lua, 0)
        f.write(tosend)
        f.flush()
        f.close()
        time.sleep(0.1)

# openLuaServer('something9')
