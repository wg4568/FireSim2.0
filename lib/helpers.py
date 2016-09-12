import math, os, binascii, itertools, pygame
from random import randint, seed as set_seed
from noise import pnoise1, pnoise2
from hashlib import md5

def control_check():
	keys = list(pygame.key.get_pressed())
	mouse = pygame.mouse.get_pressed()
	keys.append(mouse[0])
	keys.append(mouse[1])
	keys.append(mouse[2])
	return keys

def random_seed(length=16):
	set_seed(binascii.b2a_hex(os.urandom(length)))
	return binascii.b2a_hex(os.urandom(length))

def noise1D(val, seed=random_seed(), sharp=100):
	sharp = float(sharp)
	seed = parse_seed(seed)
	val = pnoise1((val/float(sharp)) + seed)
	return val

def noise2D(val1, val2, seed=random_seed(), sharp=100.):
	sharp = float(sharp)
	seed = parse_seed(seed)
	return pnoise2((val1/sharp) + seed, (val2/sharp) + seed)

def bended2D(*args, **kwargs):
	return noise2D(val1)

def translate(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)
	return rightMin + (valueScaled * rightSpan)

def parse_seed(seed):
	h = md5(str(seed)).hexdigest()
	s = translate(int(h, 16), 0, 10**38, 0, 1000)
	return s

def dist_between(x1, y1, x2, y2):
	return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def merge_dicts(*dicts):
	base = dicts[0]
	for d in dicts:
		for item in d:
			base[item] = d[item]
	return base