import platform
import subprocess
import psutil
import time
import re

# For Windows
def get_active_window_title_windows():
    try:
        import pygetwindow as gw
        window = gw.getActiveWindow()
        return window.title
    except Exception as e:
        return str(e)

# For Linux
def get_active_window_title_linux():
    try:
        root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
        stdout, stderr = root.communicate()
        m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
        if m != None:
            window_id = m.group(1)
            window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
            stdout, stderr = window.communicate()
        return stdout.decode()

    except Exception as e:
        return str(e)

def get_active_window_title():
    if platform.system() == 'Linux':
        return get_active_window_title_linux()
    elif platform.system() == 'Windows':
        return get_active_window_title_windows()
    else:
        return "Unsupported OS"


def get_linux_window_ids(pid):
    proc = subprocess.run(
        ["wmctrl", "-lp"], 
        capture_output=True, 
        text=True
    )
    return [line.split()[0] for line in proc.stdout.split("\n") if line.split()[2]==str(pid)]


def run_app(args, shell):
    controlled_id = None
    proc = subprocess.Popen(args, shell=False)
    p = psutil.Process(proc.pid)
    if p.is_running():
        print("Process is running")
    else:
        print("Process is not running")
    if platform.system() == 'Windows':
        try:
            from pywinauto import application

            controlled_id = proc.pid
            app = application.Application().connect(process=controlled_id)
            win = app.top_window()
            win.maximize_box.click()  # Maximize window
            win.set_focus()  # Bring to front
        except Exception as e:
            print(f"Error: {str(e)}")
    elif platform.system() == 'Linux':
        time.sleep(1) # Sleep for a while to let the process start and create a window
        window_ids = get_linux_window_ids(proc.pid)
        if window_ids:
            controlled_id = window_ids[0]
            subprocess.call(["wmctrl", "-i", "-a", controlled_id])
            subprocess.call(["wmctrl", "-i", "-r", controlled_id, "-b", "add,maximized_vert,maximized_horz"])
        else:
            print("Could not find a window ID associated with the process.")
    else:
        return "Unsupported OS"
    return controlled_id