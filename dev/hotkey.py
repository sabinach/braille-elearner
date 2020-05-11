from pynput.keyboard import Key, Controller

keyboard = Controller()

# Press and release space
keyboard.press(Key.cmd)
keyboard.press(Key.tab)
keyboard.release(Key.tab)
keyboard.release(Key.cmd)