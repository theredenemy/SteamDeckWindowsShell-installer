import ctypes, os
import sys
import pathlib
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
if is_admin == True:
    print("OK")
    try:
        checkarg = sys.argv[2]
        argcheck = True
        checkarg = 0
    except IndexError:
        argcheck = False
    

    if argcheck == True:
        print(sys.argv)
        import argparse
        import DeckInstalllib

        parser = argparse.ArgumentParser()
        parser.add_argument("--installconfig")

        args = parser.parse_args()
        installconfig_file = args.installconfig
        DeckInstalllib.install(installconfig_file)
    else:
        import configmenu
        import DeckInstalllib
        configmenu.makeinstallconfig()
        DeckInstalllib.install("SteamDeckShellInstall.ini")

else:
    try:
        if pathlib.Path(__file__).suffix == ".py":
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
    except IndexError:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

