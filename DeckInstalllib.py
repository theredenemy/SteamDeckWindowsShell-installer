def get_url(repository, file_type, find_to_match):
    import requests

    url = f"https://api.github.com/repos/{repository}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    assets = response.json().get("assets", [])
    download_url = next(
        (a["browser_download_url"] for a in assets if find_to_match in a["browser_download_url"] and a["browser_download_url"].endswith(f".{file_type}")),
        None,
    )
    return download_url

def download_file(url,filename):
    import requests
    file_data = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(file_data.content)
    return filename

def set_defender_ExclusionPath(dir):
    import os
    dirmod = f"'{dir}'"
    os.system(f'powershell -Command "Set-MpPreference -ExclusionPath {dirmod}"')

def remove_defender_ExclusionPath(dir):
    import os
    dirmod = f"'{dir}'"
    os.system(f'powershell -Command "Remove-MpPreference -ExclusionPath {dirmod}"')


def install(installconfig):
    import configparser
    import os
    import configHelper
    import shutil
    import DeckInstalllib
    import time
    import subprocess
    import setshellkey
    import sys
    import winreg
    # Set Variables
    installerfiles_dir = "installerfiles"
    python_install_url = "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
    git_install_url = DeckInstalllib.get_url("git-for-windows/git", "exe", "64-bit")
    gitrepodirname = "steam_deck_shell"
    config = configHelper.read_config(installconfig)
    ClientDir = config['SteamWindowsShell']['ClientDir']
    ClientExe = config['SteamWindowsShell']['ClientExe']
    ClientExeArg = config['SteamWindowsShell']['ClientExeArg']
    waitforpro = config['SteamWindowsShell']['waitforpro']
    gitrepo = config['Install']['gitrepo']
    installdir = config['Install']['installdir']
    uacpromptoff = config['Install']['uacpromptoff']
    AddExclusion = config['Install']['AddExclusion']
    start_dir_main = subprocess.getoutput('echo %cd%')
    start_dir = rf'{start_dir_main}'
    start_dir = start_dir.replace('\\', '/')
    filename = os.path.basename(sys.executable)
    reboot = 0
    if not os.path.isfile(installconfig) == True:
        print("NO FILE")
        return
    # Start Install
    print("Starting Installation")
    time.sleep(3)
    USERPROFILE = subprocess.getoutput("echo %USERPROFILE%")
    startup_dir = f"{USERPROFILE}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    if os.path.isfile(f"{startup_dir}\\startup.cmd") == True:
        os.remove(f"{startup_dir}\\startup.cmd")
    if os.path.isdir(installerfiles_dir) == True:
        os.system(f"rd /s /q {installerfiles_dir}")
    os.mkdir(installerfiles_dir)
    os.chdir(installerfiles_dir)
    installer_directory = subprocess.getoutput('echo %cd%')
    if not shutil.which("git"):
        print("Downloading Git")
        git_installer = DeckInstalllib.download_file(git_install_url,"git_install.exe")
        print("Installing Git")
        os.system(f"{git_installer} /SILENT")
        reboot = 1
    if not shutil.which("pip"):
        print("Downloading Python")
        python_installer = DeckInstalllib.download_file(python_install_url,"python_install.exe")
        print("Installing Python")
        os.system(f"{python_installer} /passive PrependPath=1 InstallAllUsers=1")
        reboot = 1
    if uacpromptoff == "True":
        print("Disabling UAC Prompt")
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "ConsentPromptBehaviorAdmin", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "PromptOnSecureDesktop", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    time.sleep(3)
    if os.path.isdir(installdir) == True:
        shutil.rmtree(installdir)
    os.mkdir(installdir)
    current_directory = subprocess.getoutput('echo "%cd%"')
    installer_directory = subprocess.getoutput('echo "%cd%"')
    if AddExclusion == "True":
        print("Adding Defender Exclusions")
        DeckInstalllib.set_defender_ExclusionPath(installer_directory)
        DeckInstalllib.set_defender_ExclusionPath(installdir)
    if reboot == 1:
        print("Restarting Windows. (Continue after Restart)")
        time.sleep(3)
        USERPROFILE = subprocess.getoutput("echo %USERPROFILE%")
        startup_dir = f"{USERPROFILE}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        if len(start_dir) >= 2 and start_dir[1] == ':':
            drive = start_dir[:2]
            rest = start_dir[2:].lstrip('\\')
        else:
            drive = ""
            rest = start_dir
        f = open("startup.cmd", "w")
        startupscript = f'''cd / 
        {drive}
        cd {rest}
        start {filename} --installconfig {installconfig}
        '''
        f.write(startupscript)
        f.close()
        shutil.move("startup.cmd", startup_dir)
        os.system("shutdown -r -f -t 0")
        return
    print("Cloning Git Repository")
    os.system(f"git clone {gitrepo} {current_directory}\\{gitrepodirname}")
    if os.path.isdir(gitrepodirname) == False:
        print("NO DIR")
        return
    
    os.chdir(gitrepodirname)
    print("Setting up Virtual Environment")
    venvdir = "venv"
    if os.path.isdir(venvdir) == False:
    
        f = open("make_venv.bat", "w")
        makevenvbat = f'''python -m venv {venvdir}
        cls
        call {venvdir}/Scripts/activate.bat
        python -m pip install --upgrade pip
        pip install -r requirements.txt'''
        f.write(makevenvbat)
        f.close()
        os.system("make_venv.bat")

    f = open("load_venv.bat", "w" )
    loadvenvbat = f'''call {venvdir}/Scripts/activate.bat
    start /wait cmd.exe /c "pyinstaller shell.py --onefile && pyinstaller restoreshell.py --onefile"'''
    f.write(loadvenvbat)
    f.close()
    print("Compiling")
    os.system("load_venv.bat")
    time.sleep(2)
    os.chdir("dist")
    time.sleep(2)
    shutil.move("shell.exe", f"{installdir}\\shell.exe")
    time.sleep(2)
    shutil.move("restoreshell.exe", f"{installdir}\\restoreshell.exe")
    time.sleep(2)
    print("Cleaning up")
    time.sleep(2)
    os.chdir(start_dir)
    time.sleep(2)
    if AddExclusion == "True":
        DeckInstalllib.remove_defender_ExclusionPath(installer_directory)
    time.sleep(2)
    os.system(f"rd /s /q {installerfiles_dir}")
    print("Making Config File...")
    time.sleep(2)
    os.chdir(installdir)
    config_file = configparser.ConfigParser()
    config_file.add_section("SteamWindowsShell")
    config_file.set("SteamWindowsShell", "ClientDir", ClientDir)
    config_file.set("SteamWindowsShell", "ClientExe", ClientExe)
    config_file.set("SteamWindowsShell", "ClientExeArg", ClientExeArg)
    config_file.set("SteamWindowsShell", "waitforpro", waitforpro)

    with open(rf"{installdir}/SteamWinShellconfig.ini", 'w') as configfileObj:
        config_file.write(configfileObj)
        configfileObj.flush()
        configfileObj.close()
    time.sleep(3)
    setshellkey.SetAsShell(f"{installdir}/shell.exe")
    time.sleep(2)
    print("Restarting Windows")
    time.sleep(3)
    os.system("shutdown -r -f -t 0")




    
    




    