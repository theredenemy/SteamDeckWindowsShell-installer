def makeinstallconfig():
    import configparser
    import os
    import win32ui
    import win32con
    gitrepodefault = "https://github.com/theredenemy/SteamDeckWindowsShell"
    installdirdefault = "C:/SteamDeckShell"
    ClientDirdefault = "C:/Program Files (x86)/Steam"
    ClientExedefault = "steam.exe"
    ClientExeArgdefault = "-noverifyfiles -gamepadui"
    waitforprodefault = "steamwebhelper.exe"
    print("Welcome to SteamDeckWindowsShell Installer")
    gitrepo = input(f"Enter the Git Repo to clone for SteamDeckWindowsShell. default:{gitrepodefault}: ")
    if not gitrepo:
        gitrepo = gitrepodefault
    installdir = input(f"Enter Installation Directory. default:{installdirdefault}: ")
    if not installdir:
        installdir = installdirdefault
    ClientDir = input(f"Enter Launcher Directory. default:{ClientDirdefault}: ")
    if not ClientDir:
        ClientDir = ClientDirdefault
    ClientExe = input(f"Enter Launcher Executable. default:{ClientExedefault}: ")
    if not ClientExe:
        ClientExe = ClientExedefault
    ClientExeArg = input(f"Enter Arguments for Launcher if there is no Arguments type False. default:{ClientExeArgdefault}: ")
    if not ClientExeArg:
        ClientExeArg = ClientExeArgdefault
    if ClientExeArg == "false":
        ClientExeArg = "False"
    waitforpro = input(f"Enter Process Name to Wait for. default:{waitforprodefault}: ")
    if not waitforpro:
        waitforpro = waitforprodefault
    ask_uac_prompt = win32ui.MessageBox("Turn off UAC Prompt. Recommended so there no UAC Prompt every login.", "Steam Deck Windows Shell Installer", win32con.MB_YESNO)
    if ask_uac_prompt == win32con.IDYES:
        uacpromptoff = "True"
    elif ask_uac_prompt == win32con.IDNO:
        uacpromptoff = "False"
    else:
        uacpromptoff = "True"
    ask_if_add_defender_Exclusion = win32ui.MessageBox("Add Defender Exclusion. Recommended so the Pyinstaller Executables dont get Flagged Because of Using the pre-compiled bootloader", "Steam Deck Windows Shell Installer", win32con.MB_YESNO)
    if ask_if_add_defender_Exclusion == win32con.IDYES:
        AddExclusion = "True"
    elif ask_if_add_defender_Exclusion == win32con.IDNO:
        AddExclusion = "False"
    else:
        AddExclusion = "True"
    
    print("Making Install Config...")
    config_file = configparser.ConfigParser()

    config_file.add_section("Install")

    config_file.set("Install", "gitrepo", gitrepo)
    config_file.set("Install", "installdir", installdir)
    config_file.set("Install", "uacpromptoff", uacpromptoff)
    config_file.set("Install", "AddExclusion", AddExclusion)
    

    config_file.add_section("SteamWindowsShell")

    config_file.set("SteamWindowsShell", "ClientDir", ClientDir)
    config_file.set("SteamWindowsShell", "ClientExe", ClientExe)
    config_file.set("SteamWindowsShell", "ClientExeArg", ClientExeArg)
    config_file.set("SteamWindowsShell", "waitforpro", waitforpro)

    if os.path.isfile("SteamDeckShellInstall.ini") == True:
        os.remove("SteamDeckShellInstall.ini")

    with open(r"SteamDeckShellInstall.ini", 'w') as configfileObj:
     config_file.write(configfileObj)
     configfileObj.flush()
     configfileObj.close()

    
if __name__ == '__main__':
    makeinstallconfig()