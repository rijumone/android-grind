import math
import time
import subprocess
from random import randrange



def main():
	while True:
		a = randrange(360)
		x = calc_x(a)
		y = calc_y(a)
		subprocess.call(['adb', 'shell', 'input', 'tap', str(x), str(y)])
		time.sleep(randrange(3, 6))

def calc_x(a):
	return 530+(229 * math.cos(a))

def calc_y(a):
	return 900+(229 * math.sin(a))

if __name__ == '__main__':
	main()