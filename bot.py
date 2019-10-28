#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pedro Gabaldon

import os
import io
import sys
import threading
import argparse

from google.cloud import vision
import pyscreenshot as ImageGrab

from colors import *
import g_search
import gNLP

def main(AutoShot=False):
	os.system('') #Enable Windows ANSI/VT100

	envGAC = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
	
	if not envGAC:
		print 'Remember to establish GOOGLE_APPLICATION_CREDENTIALS environment variable.'
		sys.exit()

	client = vision.ImageAnnotatorClient()

	if AutoShot:
		try:
			im=ImageGrab.grab(bbox=(int(os.getenv('x1')),int(os.getenv('y1')),int(os.getenv('x2')),int(os.getenv('y2'))))
		except TypeError:
			print bcolors.BOLD + 'Did you forget to set x1,y1,x2,y2 env variables?' + bcolors.ENDC
			sys.exit()
		im.save('go.jpg')
		file_name = 'go.jpg'
	else:
		file_name = args.image

	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()

	image = vision.types.Image(content=content)
	
	response = client.text_detection(image=image)
	texts = response.text_annotations

	print 'Texts:\n'

	text = texts[0].description.splitlines()
	try:
		q = texts[0].description[0:texts[0].description.index('?') + 1].replace('\n', ' ').replace('"', '')
		#q.replace('¿', '')
		index = [i for i, s in enumerate(text) if '?' in s]
	except ValueError:
		q = texts[0].description[0:texts[0].description.index(':')].replace('\n', ' ').replace('"', '')
		#q.replace(':', '')
		index = [i for i, s in enumerate(text) if ':' in s]

	print bcolors.BOLD + q + bcolors.ENDC + '\n'

	remove = ['a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 'por', u'según', 'sin', 'so', 'sobre', 'tras', 'versus', 'las', 'los', 'el', 'la', 'un', 'una', 'unos', 'unas', 'del']
	optA = text[index[0] + 1].lower().replace('"', '').split()
	optB = text[index[0] + 2].lower().replace('"', '').split()
	optC = text[index[0] + 3].lower().replace('"', '').split()

	opt1 = []
	opt2 = []
	opt3 = []

	for w in optA:
		if w not in remove:
			opt1.append(w)

	for w in optB:
		if w not in remove:
			opt2.append(w)

	for w in optC:
		if w not in remove:
			opt3.append(w)

	opt1 = ' '.join(opt1)
	opt2 = ' '.join(opt2)
	opt3 = ' '.join(opt3)

	print bcolors.WARNING + 'Opt1: ' + opt1
	print 'Opt2: ' + opt2
	print 'Opt3: ' + opt3 + bcolors.ENDC

	threadGS = threading.Thread(target=g_search.search, args=(q, [opt1, opt2, opt3]))
	threadGNLP = threading.Thread(target=gNLP.gNLP, args=(q, [opt1, opt2, opt3]))
	
	threadGNLP.start()
	threadGS.start()

	threadGNLP.join()
	threadGS.join()

	sys.exit()	

if __name__ == '__main__':
	parse = argparse.ArgumentParser(description='Q12 Bot')
	parse.add_argument('-as, --autoshot', dest='autoshot', help='Auto screenshot.', action='store_true')
	parse.add_argument('-i, --image', dest='image', type=str, nargs='?', help='Path of image to use.', metavar='Path')
	args = parse.parse_args()

	if args.autoshot:
		main(AutoShot=True)
	elif args.image:
		main()
	else:
		print 'Use: python {0} -h or --help, to see options.'.format(sys.argv[0])
		sys.exit()






