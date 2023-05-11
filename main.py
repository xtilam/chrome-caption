import sys
import os
import win32process
import psutil
import pyautogui
import time
import ctypes
import subprocess
import keyboard

from typing import List

import pygetwindow
import threading
from PySide6.QtGui import QGuiApplication, QWindow
from PySide6.QtQml import QQmlApplicationEngine, QJSValue
from PySide6.QtCore import QCoreApplication, Qt, QUrl, QObject, Signal, Slot, Property
from ce import CEClient


class Actions(QObject):
    ce: CEClient
    viewWin: QJSValue = None
    win: pygetwindow.Win32Window = None
    pid: int = 0
    script: str = ""
    address = 0

    def __init__(this, parent=None):
        this.ce = CEClient("")
        this.ce.evalFileScript(ceScriptPath)
        QObject.__init__(this)

    @Slot(QJSValue, result=None)
    def setViewWin(this, win):
        this.viewWin = win

    @Slot(result=int)
    def findCaptionWindow(this):
        if this.isValidWin():
            return 1
        this.win = None
        windows: List[pygetwindow.Win32Window] = pygetwindow.getWindowsWithTitle(
            "Live Caption"
        )
        this.win = None
        print("find window")
        for w in windows:
            [tid, pid] = win32process.GetWindowThreadProcessId(w._hWnd)
            process = psutil.Process(int(pid))
            print(pid)
            if process.name() != "chrome.exe":
                continue
            this.win = w
            this.pid = pid
            this.ce.evalScript("openProcess({})".format(this.pid))
            w.moveTo(-400, -400) 
            break
        return 0 if this.win is None else 1

    @Slot(result=bool)
    def checkChrome(this):
        try:
            this.win = None
            this.viewWin.setProperty("error", "Đang tìm caption")
            app.processEvents()
            subprocess.Popen([chromePath, soundPath])
            time.sleep(4.0)
            if not this.findCaptionWindow():
                raise Exception("Không tìm thấy chrome caption")
            this.ce.clearContentTxt()
            this.ce.evalScript("scanOne()")
            countScan = int(this.ce.waitContent())
            if countScan == 0:
                raise Exception("Không tìm thấy caption phù hợp")
            subprocess.Popen([chromePath, soundContentPath])
            time.sleep(2.0)
            this.ce.evalScript("scanTwo()")
            address = int(this.ce.waitContent())
            if address == 0:
                raise Exception("Không tìm thấy caption phù hợp")
            this.viewWin.setProperty("isValidAddress", True)
            this.address = address 
            return True
        except Exception as e:
            # this.viewWin.setProperty('error')
            print(this.viewWin)
            this.viewWin.setProperty("isValidAddress", False)
            this.viewWin.setProperty("error", str(e))
            return False
    @Slot(result=None)
    def getText(this):
        try:
            if not this.isValidWin(): 
                raise Exception('invalid win') 
            
            textResult = ""
            OpenProcess = ctypes.windll.kernel32.OpenProcess
            ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory # Method 1

            PROCESS_ALL_ACCESS = 0x1F0FFF
            PROCESS_VM_READ = 0x0010
            PID = this.pid
            processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, PID) # Why is it zero
            lengthString = ctypes.c_int64(0)
            ptrString = ctypes.c_void_p(0)
            
            ReadProcessMemory(processHandle, ctypes.c_void_p(this.address), ctypes.byref(ptrString), ctypes.sizeof(ptrString), 0) # Why is it zero
            ReadProcessMemory(processHandle, ctypes.c_void_p(this.address + 8), ctypes.byref(lengthString), ctypes.sizeof(lengthString), 0) # Why is it zero
            if lengthString.value and ptrString.value: 
                string = ctypes.c_buffer(lengthString.value * 2)
                addressString = ctypes.byref(string)
                ReadProcessMemory(processHandle, ptrString, addressString, ctypes.sizeof(string), 0)
                textResult = ctypes.wstring_at(addressString, lengthString.value)
            this.viewWin.setProperty('memoryText', textResult)
        except Exception as e:
            this.win = None
            this.viewWin.setProperty("isValidAddress", False)
            this.viewWin.setProperty("error", '')
            
    @Slot(result=None)
    def showCaption(this):
        if not this.isValidWin() or not this.findCaptionWindow():
            return False
        this.win.show()
        this.win.moveTo(1, 1)
        return True
    
    @Slot(result=None)
    def hideCaption(this):
        if not this.isValidWin() or not this.findCaptionWindow():
            return False
        this.win.hide()
        this.win.moveTo(-9999, 0)
        return True
    
    def isValidWin(this):
        if this.win is None:
            return False
        win32 = win32process.GetWindowThreadProcessId(this.win._hWnd)
        if not win32[0] or not win32[1]:
            return False
        return True


def test():
    actions.checkChrome()

custom_config = "-l eng --oem 3 --psm 6"
imageCapturePath = os.path.join(os.path.dirname(__file__), "screen.png")
mainQmlPath = os.path.join(os.path.dirname(__file__), "qml/main.qml")
ceScriptPath = os.path.join(os.path.dirname(__file__), "celua/core.lua")
chromePath = os.environ["programfiles"] + "/Google/Chrome/Application/chrome.exe"
ceScanPattern = "60 55 F0 B5 F9 7F 00 00 00 00 00 00 00 00 00 00 ? ? ? ? ? ? ? ? 3D"
soundPath = os.path.join(os.path.dirname(__file__), "asset/content.mp3")
soundContentPath = os.path.join(os.path.dirname(__file__), "asset/mountain.mp3")

time.sleep(1.0) 

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine(app)
context = engine.rootContext()
actions = Actions(engine.rootContext())

context.setContextProperty("actions", actions)  
engine.evaluate("global = this; window = this;")
engine.load(mainQmlPath)

keyboard.add_hotkey("ctrl+alt+c", test)

app.exec()
