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
    import requests
    import time
    import subprocess
    import setshellkey
    import win32api
    import win32con
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
    uacoff = config['Install']['uacoff']
    AddExclusion = config['Install']['AddExclusion']
    start_dir = subprocess.getoutput('echo "%cd%"')
    
    # Start Install
    if os.path.isdir(installerfiles_dir) == True:
        shutil.rmtree(installerfiles_dir)
    os.mkdir(installerfiles_dir)
    os.chdir(installerfiles_dir)
    if not shutil.which("git"):
        git_installer = DeckInstalllib.download_file(git_install_url,"git_install.exe")
        os.system(f"{git_installer} /SILENT")
    if not shutil.which("python"):
        python_installer = DeckInstalllib.download_file(python_install_url,"python_install.exe")
        os.system(f"{python_installer} /silent /PrependPath=1 /InstallAllUsers=1")
    time.sleep(3)
    if os.path.isdir(installdir) == True:
        shutil.rmtree(installdir)
    os.mkdir(installdir)
    current_directory = subprocess.getoutput('echo "%cd%"')
    installer_directory = current_directory
    if AddExclusion == "True":
        DeckInstalllib.set_defender_ExclusionPath(current_directory)
        DeckInstalllib.set_defender_ExclusionPath(installdir)
    os.system(f"git clone {gitrepo} {current_directory}\\{gitrepodirname}")
    if os.path.isdir(gitrepodirname) == False:
        print("NO DIR")
        return
    
    os.chdir(gitrepodirname)
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
    os.system("load_venv.bat")
    time.sleep(2)
    os.chdir("dist")
    time.sleep(2)
    shutil.move("shell.exe", f"{installdir}\\shell.exe")
    time.sleep(2)
    shutil.move("restoreshell.exe", f"{installdir}\\restoreshell.exe")
    time.sleep(2)
    os.chdir(start_dir)
    time.sleep(2)
    if AddExclusion == "True":
        DeckInstalllib.remove_defender_ExclusionPath(installer_directory)
    time.sleep(2)
    shutil.rmtree(installer_directory)
    setshellkey.SetAsShell(f"{installdir}\\shell.exe")
    if uacoff == "True":
        os.system("reg delete HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA")
        os.system("reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f")
    win32api.ExitWindowsEx(win32con.EWX_REBOOT | win32con.EWX_FORCE, 0)



    
    




    