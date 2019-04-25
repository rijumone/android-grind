# game is launched and ready

import csv
import time
import subprocess
import pytesseract
from PIL import Image, ImageOps

def main():

	while True:
		# swipe screen to corner to ensure image has nothing beneath it
		for _ in range(2):
			# twice to make sure
			subprocess.call(['adb', 'shell', 'input', 'touchscreen', 'swipe', '1200', '600', '200', '200'])


		_tap_achievements_btn()
		_capture_and_pull_screenshot()

		with open('tmp/gains.csv', 'a') as out_file:
			csv_writer = csv.writer(out_file)
			write_this_lst = []
			for current in ['cash', 'gold', 'skips']:
				_ = _check_assets(current)
				print('current {}: {}'.format(current, _))
				write_this_lst.append(_)
			print(write_this_lst)
			csv_writer.writerow(write_this_lst)
			
		_tap_achievements_btn()
		# crop the image to extract only the portion with text
		ImageOps.crop(Image.open('tmp/screen.png'), (860, 650, 120, 0)).save('tmp/screen_cropped.png')

		# feed this image to OCR to get the words
		earn_txt = pytesseract.image_to_string(Image.open('tmp/screen_cropped.png'))
		print(earn_txt)
		if earn_txt.lower().strip().split()[0] != 'earn':
			print('didn\'t match "earn xxxx", breaking')
			break
		
		# tap on the 'earn gold' icon
		subprocess.call(['adb', 'shell', 'input', 'tap', '1260', '710'])
		
		time.sleep(2)
		# attempt to identify type of ad and time to sleep
		pos_X_btn, sleep_sec = _get_pos_and_sec()
		# wait 30 seconds plus few seconds extra for the ad to complete playing
		print('sleeping for {} seconds'.format(sleep_sec))
		time.sleep(sleep_sec)
		# print('sleeping for 2 seconds')
		# time.sleep(2)
		
		# tap on 'X' button
		subprocess.call(['adb', 'shell', 'input', 'tap', str(pos_X_btn[0]), str(pos_X_btn[1])])

		# keep checking if screen returned after ad
		returned_after_ad = False
		while not returned_after_ad:
			# capture the screen
			_capture_and_pull_screenshot()
			# crop it
			ImageOps.crop(Image.open('tmp/screen.png'), (1040, 630, 70, 20)).save('tmp/screen_cropped.png')
			if pytesseract.image_to_string(Image.open('tmp/screen_cropped.png')).lower().strip() != 'continue':
				print('sleeping for 3 seconds while waiting for screen to return from ad')
				time.sleep(3)
			else:
				returned_after_ad = True

		# tap on 'continue' button
		subprocess.call(['adb', 'shell', 'input', 'tap', '1250', '690'])

		# give it some time to return to main screen
		time.sleep(5)
		print('=====================================================================')
		# break

def _capture_and_pull_screenshot():
	subprocess.call(['adb', 'shell', 'screencap', '/sdcard/screen.png'])
	subprocess.call(['adb', 'pull', '/sdcard/screen.png', 'tmp/screen.png'])

def _check_assets(asset_type):
	''' check appropriate asset_type from exiting image and return a string'''

	if asset_type == 'gold':
		crop_tpl = (1020, 0, 195, 660)
	elif asset_type == 'cash':
		crop_tpl = (860, 0, 310, 660)
	elif asset_type == 'skips':
		crop_tpl = (758, 0, 470, 660)
	
	ImageOps.crop(Image.open('tmp/screen.png'), crop_tpl).save('tmp/screen_cropped.png')
	print(crop_tpl)
	return pytesseract.image_to_string(Image.open('tmp/screen_cropped.png')).lower().strip()

def _get_pos_and_sec():
	_capture_and_pull_screenshot()
	# import pdb;pdb.set_trace()
	for crop_tpl in [(953, 20, 80, 660), ]:
		ImageOps.crop(Image.open('tmp/screen.png'), crop_tpl).save('tmp/screen_cropped.png')
		result_lst = pytesseract.image_to_string(Image.open('tmp/screen_cropped.png')).lower().strip().split()
		if 'seconds' in result_lst or 'remaining' in result_lst:
			try:
				return (1260, 10), int(result_lst[0])
			except:
				pass

	return (1260, 10), 30

def _tap_achievements_btn():
	# tap on achievments button
	subprocess.call(['adb', 'shell', 'input', 'tap', '400', '20'])
		

if __name__ == '__main__':
	main()