from pygame import mixer
from pynput import keyboard
import sys
# from threading import Thread
from glob import glob

combi = [
	{keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='2')}, # pause and unpause
	{keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='1')}, # quit
	{keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='3')}, # next
	{keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='4')}, # previous
	{keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='5')}, # rewind
	{keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='6')}, # display files
	{keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode(char='7')}, # select track
]

current = set()

mixer.init()
flag = True
position = 0

def on_press(key):
	global flag
	global current
	if any([key in COMBO for COMBO in combi]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in combi):
			if key.char == '1':
				mixer.quit()
				sys.exit()
			elif key.char == '2':
				if flag:
					mixer.music.pause()
				else:
					mixer.music.unpause()
				flag = not flag
			elif key.char == '3':
				audio_next()
			elif key.char == '4':
				audio_previous()
			elif key.char == '5':
				rewind_current()
			elif key.char == '6':
				display_songs()
			elif key.char == '7':
				current = set()
				select_track()

def on_release(key):
	if any([key in COMBO for COMBO in combi]):
		current.remove(key)

def keyboard_listener():
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

def audio_play():

	files = glob("E:\\Music\\*.mp3")
	mixer.music.load(files[position])
	mixer.music.play()
	for i in range(1, len(files)):
		mixer.music.queue(files[i])
	mixer.music.rewind()

def audio_next():

	global position
	files = glob("E:\\Music\\*.mp3")
	position = (position+1)%len(files)
	audio_play()

def audio_previous():

	files = glob("E:\\Music\\*.mp3")
	global position
	position = (position + len(files) - 1)%len(files)
	mixer.music.stop()
	mixer.music.load(files[position])
	mixer.music.play()

def rewind_current():

	files = glob("E:\\Music\\*.mp3")
	global position
	mixer.music.stop()
	mixer.music.load(files[position])
	mixer.music.play(-1)

def display_songs():

	files = glob("E:\\Music\\*.mp3")
	global position
	for pos, i in enumerate(files):
		if pos == position:
			print(str(pos+1)+". " + i + "\t CURRENTLY PLAYING")
		else:
			print(str(pos+1)+". "+i)

def select_track():

	files = glob("E:\\Music\\*.mp3")
	global position
	position = int(input("Enter the track no.: "))-1
	mixer.music.stop()
	mixer.music.load(files[position])
	mixer.music.play()

#Thread(target = audio_play).start()
audio_play()
keyboard_listener()
# keyboard_listener()
# Thread(target = keep_playing).start()
#Thread(target = keyboard_listener).start()
