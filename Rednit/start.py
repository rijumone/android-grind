import time
import subprocess
from random import randint, uniform
from PIL import Image, ImageOps

def main():
	while True:
		# decide number of times to view pics
		img_ts = str(int(time.time()))
		n_times_view = randint(1,8)
		print('n_times_view', n_times_view)
		for _ in range(n_times_view):

			# _capture_and_pull_screenshot('{}_{}'.format(img_ts, _))
			# _crop_out_notif_bar('{}_{}'.format(img_ts, _))
			_tap_right()
			# wait for image to load
			time.sleep(uniform(0.5, 1.2))
		_swipe_right()
		# wait for next profile to load
		time.sleep(uniform(0.2, 0.5))



def _capture_and_pull_screenshot(file_name):
	subprocess.call(['adb', 'shell', 'screencap', '/sdcard/Scrape/{}.png'.format(file_name)])
	subprocess.call(['adb', 'pull', '/sdcard/Scrape/{}.png'.format(file_name), 'tmp/{}.png'.format(file_name)])

def _tap_right():
	subprocess.call(['adb', 'shell', 'input', 'tap', str(randint(792,951)), str(randint(804,1478))])

def _swipe_right():
	subprocess.call(['adb', 'shell', 'input', 'touchscreen', 'swipe', str(randint(100,120)), str(randint(760,1421)), str(randint(850,950)), str(randint(760,1421))])

def _crop_out_notif_bar(file_name):
	ImageOps.crop(Image.open('tmp/{}.png'.format(file_name)), (0, 210, 0, 230)).save('tmp/{}.png'.format(file_name))


if __name__ == '__main__':
	main()