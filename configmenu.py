def makeinstallconfig():
    import configparser
    import os
    gitrepodefault = "https://github.com/theredenemy/SteamDeckWindowsShell"
    installdirdefault = "C:/SteamDeckShell"
    print("Welcome Text")
    gitrepo = input(f"Enter the Git Repo to clone for SteamDeckWindowsShell. default:{gitrepodefault}: ")
    if not gitrepo:
        gitrepo = gitrepodefault
    installdir = input(f"Enter Installation Directory. default:{installdirdefault}: ")
    if not installdir:
        installdir = installdirdefault
    
    
