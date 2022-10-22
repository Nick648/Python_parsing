import subprocess
# import sys
import os

FULL_WAY = os.getcwd()  # == CUR_DIR
CUR_DIR = os.path.abspath(os.curdir)
CUR_DIR_FILE = os.path.abspath(__file__)  # With name file.py
OS_DIR = os.curdir  # .
HOME_DIR = os.path.expanduser('~')
DESKTOP_DIR = os.path.expanduser('~') + r'\Desktop'


def out_os_module():  # Output information: Dont need!
    # print(f'sys.executable: {sys.executable}')
    print('*' * 50)
    print(f"FULL_WAY: {FULL_WAY}; \nCUR_DIR: {CUR_DIR}; "
          f"\nCUR_DIR_FILE: {CUR_DIR_FILE}; \nOS_DIR: {OS_DIR}"
          f"\nHOME_DIR: {HOME_DIR}; \nDESKTOP_DIR: {DESKTOP_DIR}")
    print('*' * 50)


def install_modules():  # Module installer from a file
    if not os.path.exists('venv'):
        print("No interpreter!\n Add in settings virtualenv!")
        return
    way = os.path.join(os.getcwd(), r'venv\Scripts\python.exe')
    subprocess.check_call([way, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])


if __name__ == '__main__':
    # out_os_module()
    install_modules()
    print(f"\n\n{'*' * 20} Done! {'*' * 20}")
