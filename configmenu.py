def makeinstallconfig():
    import configparser
    import os
    import win32ui
    import win32con
    gitrepodefault = "https://github.com/theredenemy/SteamDeckWindowsShell"
    installdirdefault = "C:/SteamDeckShell"
    print("Welcome Text")
    gitrepo = input(f"Enter the Git Repo to clone for SteamDeckWindowsShell. default:{gitrepodefault}: ")
    if not gitrepo:
        gitrepo = gitrepodefault
    installdir = input(f"Enter Installation Directory. default:{installdirdefault}: ")
    if not installdir:
        installdir = installdirdefault
    #ask_uac_off = input("Turn off UAC. Recommended so there no UAC Prompt every login. default:y")
    ask_uac = win32ui.MessageBox("Turn off UAC. Recommended so there no UAC Prompt every login.", "Steam Deck Windows Shell Installer", win32con.MB_YESNO)
    if ask_uac == win32con.IDYES:
        uacoff = True
    elif ask_uac == win32con.IDNO:
        uacoff = False
    else:
        uacoff = True
    

    
    
