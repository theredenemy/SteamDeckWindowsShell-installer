

def modify_HKLM_registry(key_path, value_name, value_data, value_type):
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        winreg.CloseKey(key)
        print(f"Registry key '{key_path}\\{value_name}' modified successfully.")
    except Exception as e:
        print(f"Error modifying registry key: {e}")

def SetAsShell(shell):
    import pathlib
    import winreg
    file_extension = pathlib.Path(__file__).suffix
    if file_extension == ".py":
      Dosetshell = 0
    else:
      Dosetshell = 1
    if Dosetshell == 0:
       print("File Extension .py does not Work with Shell Key. canceling")
       return
    modify_HKLM_registry("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon", "Shell", shell, winreg.REG_SZ)