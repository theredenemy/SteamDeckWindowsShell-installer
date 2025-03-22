import os
import time
import shutil
print("Setting up Virtual Environment")
venvdir = "Compiling_venv"
if os.path.isfile("main.spec") == True:
    os.remove("main.spec")
if os.path.isfile("make_venv.bat") == True:
    os.remove("make_venv.bat")
if os.path.isfile("load_venv.bat") == True:
    os.remove("load_venv.bat")
if os.path.isfile("SteamDeckWindowsShell_installer.exe") == True:
    os.remove("SteamDeckWindowsShell_installer.exe")
if os.path.isdir("dist") == True:
    shutil.rmtree("dist")
if os.path.isdir("build") == True:
    shutil.rmtree("build")
if os.path.isdir(venvdir) == True:
    shutil.rmtree(venvdir)

if os.path.isdir(venvdir) == False:
    
    f = open("make_venv.bat", "w")
    makevenvbat = f'''python -m venv {venvdir}
    cls
    call {venvdir}/Scripts/activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install pyinstaller'''
    f.write(makevenvbat)
    f.close()
    os.system("make_venv.bat")

f = open("load_venv.bat", "w" )
loadvenvbat = f'''call {venvdir}/Scripts/activate.bat
start /wait cmd.exe /c "pyinstaller main.py --onefile "'''
f.write(loadvenvbat)
f.close()
print("Compiling")
os.system("load_venv.bat")
time.sleep(2)
shutil.move("dist\\main.exe", "SteamDeckWindowsShell_installer.exe")
time.sleep(2)
if os.path.isfile("main.spec") == True:
    os.remove("main.spec")
if os.path.isfile("make_venv.bat") == True:
    os.remove("make_venv.bat")
if os.path.isfile("load_venv.bat") == True:
    os.remove("load_venv.bat")
if os.path.isdir("dist") == True:
    shutil.rmtree("dist")
if os.path.isdir("build") == True:
    shutil.rmtree("build")
if os.path.isdir(venvdir) == True:
    shutil.rmtree(venvdir)

