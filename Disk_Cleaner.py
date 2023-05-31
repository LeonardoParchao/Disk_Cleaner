import os
import ctypes
import sys
import shutil

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        print("Script already running with admin privileges.")
    else:
        params = " ".join([sys.executable] + sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()

def erase_browser_login(browser_name):
    if browser_name.lower() == "chrome":
        login_data_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
        if os.path.exists(login_data_path):
            os.remove(login_data_path)
            print("Login information erased from Chrome browser.")
        else:
            print("Chrome login data not found.")
    elif browser_name.lower() == "firefox":
        login_data_path = os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\")
        if os.path.exists(login_data_path):
            for profile_folder in os.listdir(login_data_path):
                login_db_path = os.path.join(login_data_path, profile_folder, "logins.json")
                if os.path.exists(login_db_path):
                    os.remove(login_db_path)
                    print("Login information erased from Firefox browser.")
                    break
            else:
                print("Firefox login data not found.")
        else:
            print("Firefox profile folder not found.")
    else:
        print("Unsupported browser.")

def delete_temp_files():
    temp_folder = os.environ.get("TEMP")
    if temp_folder:
        shutil.rmtree(temp_folder)
        print("Temporary files deleted successfully.")
    else:
        print("Temporary files folder not found.")

def delete_folder_contents(folder_path):
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in {folder_path} deleted successfully.")
    else:
        print(f"{folder_path} not found.")

def empty_recycle_bin():
    SHEmptyRecycleBinW = ctypes.windll.shell32.SHEmptyRecycleBinW
    flags = 0  # 0 for normal delete, or 1 for delete with confirmation
    result = SHEmptyRecycleBinW(None, None, flags)
    if result == 0:
        print("Recycle bin emptied successfully.")
    else:
        print("Failed to empty the recycle bin.")

run_as_admin()

browser = input("What browser is being used:")
erase_browser_login(browser)

delete_temp_files()

documents_folder = os.path.expanduser("~\\Documents")
pictures_folder = os.path.expanduser("~\\Pictures")
downloads_folder = os.path.expanduser("~\\Downloads")

delete_folder_contents(documents_folder)
delete_folder_contents(pictures_folder)
delete_folder_contents(downloads_folder)

empty_recycle_bin()
