import math
import time
import latexify
import keyboard
import pyautogui
import pyperclip

@latexify.with_latex
def functionName():
    return formular_to_be_replaced

def insertFormular(delay):
	pyautogui.hotkey('alt','q')
	time.sleep(delay)

	#get formular and modify
	formular = str(functionName)
	formular = formular.replace('\\triangleq','=')#replace '\triangleq' to '='
	delete_functionName_and_eq
	delete_bracket

	#print(formular)
	pyperclip.copy(formular)
	time.sleep(delay)
	#pyperclip.paste()
	pyautogui.hotkey('ctrl','v')
	#time.sleep(delay)
	pyautogui.hotkey('alt','f4')
	#print(f)

if __name__ == '__main__':
	#keyboard.add_hotkey('ctrl+`',insertFormular,args=(0.5,))
	#keyboard.wait()
	insertFormular(0.5)