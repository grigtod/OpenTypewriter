import os.path
import keyboard 
import pystray
from playsound import playsound
from PIL import Image
from tendo import singleton
from other.helperVars import hv

keySoundOn = True
trayToggle = False

def onQuit():
    global icon 
    icon.stop()
    keyboard.wait.stop()

def playSound(_soundName, _useMainRegister):
    filePath = "assets/sfx/" + _soundName
    if os.path.isfile(filePath):
        playsound.playsound(filePath, _useMainRegister)
    else: print("Missing file: " + filePath)
   
def onKeyPress(e): 
    if e.event_type == "down": 
        if len(e.name) == 1: 
            if str(e.name).islower(): playSound(hv.lowerCaseFile, True)
            else: playSound(hv.upperCaseFile, True)
        if(e.scan_code == hv.scanCode_NewLine): playSound(hv.newLineFile, True)
        if(e.scan_code == hv.scanCode_Backspace): playSound(hv.deleteFile, True)
        if(e.scan_code == hv.scanCode_space): playSound(hv.spaceFile, True)
        if(e.scan_code == hv.scanCode_tab): playSound(hv.tabFile, True)

def toggleKeySound(_trayCall):
    global keySoundOn, icon
    keySoundOn = not keySoundOn 
    if keySoundOn == True:
        keyboard.hook(onKeyPress)
        icon.icon = getOnIcon() 
        playSound(hv.onEnableFile, _trayCall)
    else:
        keyboard.unhook(onKeyPress)
        icon.icon = getOffIcon()
        playSound(hv.onDisableFile, _trayCall)
    setIconMenu()
    
      
def onToggleViaKeyboard():
    toggleKeySound(False)

def onToggleViaTray():
    toggleKeySound(True)
 
def getOnIcon(): return Image.open('assets/icons/onIcon.ico')

def getOffIcon(): return Image.open('assets/icons/offIcon.ico')

def onCredits():
    import webbrowser
    webbrowser.open('http://opentypewriter.com/#info')

def onDonate():
    import webbrowser
    webbrowser.open('http://opentypewriter.com/#donate')
 
def getToggleMenu():
    global keySoundOn
    if keySoundOn: return pystray.MenuItem('Disable ' + hv.shortcut_toggle, onToggleViaTray, None, False, True, True)
    else: return pystray.MenuItem('Enable ' + hv.shortcut_toggle, onToggleViaTray, None, False, True, True)
    
def setIconMenu():
    global icon
    icon.menu = pystray.Menu(
        getToggleMenu(),    
        pystray.Menu.SEPARATOR, 
        pystray.MenuItem('Info', onCredits),
        pystray.MenuItem('Donate', onDonate),
        pystray.MenuItem('Exit ' + hv.shortcut_exit, onQuit))
    
def setTrayIcon():
    global icon 
    icon.icon = getOnIcon()
    icon.visible = True
    icon.title = hv.appName
    icon.HAS_DEFAULT_ACTION = True 
    setIconMenu()
    icon.run()

try:    #make sure the app can only be started once
    me = singleton.SingleInstance()
    icon = pystray.Icon('ClickSound')
    keyboard.add_hotkey('win+shift', onToggleViaKeyboard) 
    keyboard.add_hotkey('win+esc', onQuit) 
    keyboard.hook(onKeyPress)
    setTrayIcon() 
    keyboard.wait.Set('win+esc')
except: print("App already running! This app instance will stop now!")


