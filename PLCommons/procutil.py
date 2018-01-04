import platform, subprocess

#from pycommon import util

#判断平台类型
def is_linux_or_mac():
    return platform.system() == 'Linux' or platform.system() == 'Darwin'

#关闭进程
def kill_process_by_name(procnames):
    names = []
    if isinstance(procnames, str):
        names.append(procnames)
    elif isinstance(procnames, list):
        names = procnames

    for procname in names:
        if is_linux_or_mac():
            subprocess.call(['killall', procname])
        else:
            subprocess.call('taskkill /F /IM ' + procname, shell=True)