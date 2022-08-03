#!/usr/bin/env python3

import sys
import os
from pprint import pprint
from traceback import print_exc
import tempfile
import subprocess

def hashline_to_macessid(line):
	try:
		l = line.strip()
	#	print(l)
		fields = l.split('*')
	#	pprint(fields)
		essid = fields[5]
		mac = fields[4]
		macessid = f"{mac}*{essid}"
	#	print(f"mac: {mac} essid: {essid} macessid: {macessid}")
		return macessid
	except:
		return None

def load_wordlist_to_usedset(wordlist):
	used = set()
	wordlistused = f"{wordlist}.used"
	with open(wordlistused, "r") as hfd:
		for l in hfd.readlines():
			macessid = hashline_to_macessid(l)
			if macessid:
				used.add(macessid)
#			print(f"macessid: {macessid}")
	return used

def add_hashlist_to_usedset(filtered_hashfile, wordlist):
	wordlistused = f"{wordlist}.used"
	with open(wordlistused, "a") as hfd:
		hfd.write("\n")
		hfd.write(filtered_hashfile)
		hfd.write("\n")
	print(f"its a good idea to run sort -u on {wordlistused} at some point")

def filter_hashfile(hashfile, wordlist):
	try:
		wordlist_used = load_wordlist_to_usedset(wordlist)
	except:
		wordlist_used = set()
#	pprint(wordlist_used)

	finals = []
	with open(hashfile, "r") as hfd:
		for l in hfd.readlines():
			l = l.strip()
			macessid = hashline_to_macessid(l)
			if macessid in wordlist_used:
				print(f"Removing {l}, matches {macessid} in {wordlist}")
			else:
				finals.append(l)
	pprint(finals)
	return finals


def run_fun(filtered_hashfile, wordlist):
	with tempfile.NamedTemporaryFile("w", delete=False) as tf:
		tf.write(filtered_hashfile)
		tf.write("\n")
		tf.close()
		arglist = ["hashcat", "-m", "22000", tf.name, wordlist]
		pprint(arglist)
		p = subprocess.run(arglist)
		os.unlink(tf.name)
		result = p.returncode
#https://github.com/hashcat/hashcat/blob/master/docs/status_codes.txt #cant used check=true because 1 is still good
		if result != 0 and result != 1:
			raise

if __name__ == "__main__":
	if not len(sys.argv) > 2:
		print(f"usage: {sys.argv[0]} hashfile wordlist")
		exit(1)
	hashfile = sys.argv[1].strip()
	wordlist = sys.argv[2].strip()
	hashfile_out_list = filter_hashfile(hashfile, wordlist)
	if not hashfile_out_list:
		print("empty hashfile_out_list")
		exit(0)
	hashfile_out = "\n".join(hashfile_out_list)
#	print(hashfile_out)
	run_fun(hashfile_out, wordlist)
	add_hashlist_to_usedset(hashfile_out, wordlist)
