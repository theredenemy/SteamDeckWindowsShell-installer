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

def install(installconfig):
    import configparser
    import os
    import configHelper
    config = configHelper.read_config(installconfig)
    ClientDir = config['SteamWindowsShell']['ClientDir']
    ClientExe = config['SteamWindowsShell']['ClientExe']
    ClientExeArg = config['SteamWindowsShell']['ClientExeArg']
    waitforpro = config['SteamWindowsShell']['waitforpro']
    gitrepo = config['Install']['gitrepo']
    installdir = config['Install']['installdir']
    uacoff = config['Install']['uacoff']

    