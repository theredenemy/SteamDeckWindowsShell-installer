


import ctypes, os
import sys
import time
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
if is_admin == True:
    print("OK")
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    exit()

try:
    checkarg = sys.argv[1]
    argcheck = True
    checkarg = 0
except IndexError:
    argcheck = False
    

if argcheck == True:
    print(sys.argv)
else:
    import configmenu
    configmenu.makeinstallconfig()