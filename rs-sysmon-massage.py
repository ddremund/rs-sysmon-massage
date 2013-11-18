#!/usr/bin/python -tt

# Copyright 2013 Derek Remund (derek.remund@rackspace.com)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

def process_lines(lines):

	firstline = lines.pop(0)
	datetime = firstline.split('_')
	date = datetime[0]
	time = datetime[1]
	cpudata  = ''
	memdata = ''
	loaddata = ''

	for index,data in enumerate(lines):
		tokens = data.split()
		if len(tokens) < 1:
			continue
		if 'load' in tokens:
			loaddata = '{},{},{}\n'.format(date,time, ','.join(tokens[9:]))
			continue
		if 'Mem:' in tokens:
			nexttokens = lines[index+1].split()
			memdata = '{},{},{},{}\n'.format(date,time,','.join(tokens[1:]), ','.join(nexttokens[1:]))
			memdata += ',{},{},{},{},{},{}'.format(nexttokens[1], nexttokens[2], 
				float(tokens[2])/float(tokens[1]) * 100,
				float(tokens[3])/float(tokens[1]) * 100,
				float(nexttokens[1])/float(tokens[1]) * 100,
				float(nexttokens[2])/float(tokens[1]) * 100)
			continue
		if 'avg-cpu:' in tokens:
			nexttokens = lines[index+1].split()
			cpudata = '{},{},{}'.format(data,time,','.join(nexttokens))

	return (cpudata, memdata, loaddata)

def main():

	cpudata = 'Date,Time,%user,%nice,%system,%iowait,%steal,%idle\n'
	memdata = 'Date,Time,total,used,free,shared,buffers,cache,realused,realfree,%used,%free,%realused,%realfree\n'
	loaddata = 'Date,Time,ldavg-1,ldavg-5,ldavg-15\n'

	if len(sys.argv) > 1:
		directory = sys.argv[1]
	else:
		directory = os.path.dirname(os.path.realpath(__file__))

	for root, sub_folders, files in os.walk(directory):
		for filename in files:
			file_path = os.path.join(root, filename)

			with open(file_path, 'r') as f:
				lines = f.read().splitlines()
				cpuresults, memresults, loadresults = process_lines(lines)
				cpudata = cpudata + cpuresults
				memdata = memdata + memresults
				loaddata = loaddata + loadresults
	#with open(os.path.join(directory, 'cpu.csv'), 'w') as f:
	#	f.write(cpudata)
	#with open(os.path.join(directory, 'mem.csv'), 'w') as f:
	#	f.write(memdata)
	#with open(os.path.join(directory, 'load.csv'), 'w') as f:
	#	f.write(loaddata)

	print cpudata
	print memdata
	print loaddata

if __name__ == '__main__':
	main()