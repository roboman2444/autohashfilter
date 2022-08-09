#!/usr/bin/env python3

import sys
import os
from pprint import pprint
from traceback import print_exc
from binascii import unhexlify
def print_potfile(potfile):
	finals = []
	with open(potfile, "r") as pfd:
		for l in pfd.readlines():
			try:
				l = l.strip()
				key = l.split(":")[1].strip()
				essidraw = l.split(":")[0].split("*")[1].strip()
				try:
					essidascii = unhexlify(essidraw).decode("utf-8")
				except:
					essidascii = "error"
					print_exc()
				print(f"{essidascii}:{essidraw}:{key}")
			except:
				print_exc()


if __name__ == "__main__":
	if not len(sys.argv) > 1:
		print(f"usage: {sys.argv[0]} potfile")
		exit(1)
	potfile = sys.argv[1].strip()
	print_potfile(potfile)
