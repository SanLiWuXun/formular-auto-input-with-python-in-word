#import math
import re
import time
#import latexify
import keyboard
import os
#import pyautogui
#import pyperclip
import win32gui, win32con, win32com.client
import pythoncom
from tkinter import *

def getInput(title, message):
    def return_callback(event):
        #print('quit...')
        root.quit()
    def close_callback():
        tkinter.messagebox.showinfo('message', 'no click...')
    root = Tk(className=title)
    root.wm_attributes('-topmost', 1)
    screenwidth, screenheight = root.maxsize()
    width = 600
    height = 160
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)
    root.resizable(0, 0)
    lable = Label(root, height=2)
    lable['text'] = message
    lable.pack()
    entry = Entry(root,width=560)
    entry.bind('<Return>', return_callback)
    entry.pack()
    entry.focus_set()
    root.protocol("WM_DELETE_WINDOW", close_callback)
    root.mainloop()
    str = entry.get()
    root.destroy()
    return str

def prepose_window(hwnd, wildcard):
    '''
    Pass to win32gui.EnumWindows() to check all the opened windows
    把想要置顶的窗口放到最前面，并最大化
    '''
    pythoncom.CoInitialize()
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        win32gui.BringWindowToTop(hwnd)
        # 先发送一个alt事件，否则会报错导致后面的设置无效：pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        # 设置为当前活动窗口
        win32gui.SetForegroundWindow(hwnd)
        # 最大化窗口
        #win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

def inputFormular():
	doc_window_active = win32gui.GetForegroundWindow()
	doc_window_active_name = u''+win32gui.GetWindowText(doc_window_active)

	with open('background.py','r') as f_read:
		content = f_read.read()

	#formular = input('input the formular:')
	formular = getInput('input','input the formular:')

	if '=' not in formular:
		content = content.replace('formular_to_be_replaced',formular)

		win32gui.EnumWindows(prepose_window, ".*%s.*" % doc_window_active_name)

		content = content.replace('delete_functionName_and_eq',"formular = formular.replace('\\mathrm{functionName}() =','')")
		content = content.replace('delete_bracket',"")
	else:
		content = content.replace('delete_functionName_and_eq',"")

		formular_name = formular.split('=')[0]
		formular_content = formular.split('=')[1]
		if '(' not in formular_name:
			#formular_name = formular.split('=')[0]
			#formular_content = formular.split('=')[1]

			win32gui.EnumWindows(prepose_window, ".*%s.*" % doc_window_active_name)

			content = content.replace('functionName',formular_name)
			content = content.replace('formular_to_be_replaced',formular_content)
			content = content.replace('delete_bracket',"formular = formular.replace('()','')")
		else:
			#formular_name = formular.split('=')[0]
			#formular_content = formular.split('=')[1]
			formular_name_wo_bracket = formular_name.split('(')[0]

			win32gui.EnumWindows(prepose_window, ".*%s.*" % doc_window_active_name)

			content = content.replace('functionName()',formular_name)
			content = content.replace('functionName',formular_name_wo_bracket)
			content = content.replace('formular_to_be_replaced',formular_content)
			content = content.replace('delete_bracket',"formular = formular.replace('()','')")
	

	with open('run_cache','w') as f_write:
		f_write.write(content)

	#time.sleep(3)#第一个版本先用sleep实现等待回到word再动作，后面考虑使用Win32 API实现切换前台活动窗口

	win32gui.EnumWindows(prepose_window, ".*%s.*" % doc_window_active_name)

	os.system('python run_cache')

if __name__ == '__main__':
	keyboard.add_hotkey('ctrl+`',inputFormular)
	keyboard.wait()