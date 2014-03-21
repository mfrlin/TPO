#!/usr/bin/env python2
import distutils.sysconfig as sysconfig
import os
import sys
import tempfile

import autopep8

def get_libs_from_dir(path):
	libs = set()
	if not os.path.exists(path):
		return libs
	for fname in os.listdir(path):
		if fname.endswith('.py') or fname.endswith('.so'):
			libs.add(fname.split('.')[0])
		elif os.path.exists(os.path.join(path, fname, '__init__.py')):
			libs.add(fname)
	return libs

# generate set of standard libs
stdlib_path = sysconfig.get_python_lib(standard_lib=True)
stdlib = get_libs_from_dir(stdlib_path)
stdlib.update(get_libs_from_dir(os.path.join(stdlib_path, 'lib-dynload')))
stdlib.update(sys.builtin_module_names)

def prepare(path):
	with open(path) as f:
		source = f.read()
	source = source.split('\n')

	lines = []
	for line in source:
		# fix ident: tab -> space
		ident = 0
		while line.startswith('\t'):
			ident += 1
			line = line[1:]
		line = '    ' * ident + line

		lines.append(line)

	f, tmppath = tempfile.mkstemp()
	os.write(f, '\n'.join(lines))
	os.close(f)
	return tmppath

def lint(source, dir_path):
	local_libs = get_libs_from_dir(dir_path)

	source = source.split('\n')

	# check for sha-bang/copyright
	intro = []
	while source and (source[0].startswith('#') or not source[0]):
		intro.append(source[0])
		source = source[1:]

	# main linting
	imports = [[], [], [], []]
	lines = []
	prevline = None
	for line in source:
		# no need for multiple empty lines
		if not prevline and not line:
			continue

		# fix ident: space -> tab
		ident = 0
		while line.startswith('    '):
			ident += 1
			line = line[4:]
		line = '\t' * ident + line

		# fix imports
		if line.startswith('import') or line.startswith('from'):
			lib = line.split(' ')[1].split('.')[0]
			if lib.startswith('.'):
				imports[3].append(lib)
			elif lib in stdlib:
				imports[0].append(line)
			elif lib == 'django':
				imports[2].append(line)
			elif lib == 'enarocanje' or lib in local_libs:
				imports[3].append(line)
			else:
				imports[1].append(line)
			continue

		# done
		prevline = line
		lines.append(line)

	# generate output
	output = ''
	introcode = '\n'.join(intro).strip()
	if introcode:
		output += introcode + '\n'
		if introcode.count('\n') or not introcode.startswith('#!'):
			output += '\n'
	for group in imports:
		if group:
			output += '\n'.join(sorted(group)) + '\n\n'
	code = '\n'.join(lines).strip()
	if code:
		output += code + '\n'
	return output

def text_lint(path):
	with open(path) as f:
		source = f.read().decode('utf8')

	source = source.split('\n')
	lines = []
	prevline = None
	for line in source:
		# no need for multiple empty lines
		if not prevline and not line:
			continue

		# fix ident: space -> tab
		ident = 0
		while line.startswith('    '):
			ident += 1
			line = line[4:]
		line = '\t' * ident + line.rstrip()

		# done
		prevline = line
		lines.append(line)

	return '\n'.join(lines).strip() + '\n'

files = [(root, f)
		 for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__)))
		 for f in files]

for root, fname in files:
	path = os.path.join(root, fname)
	source = None
	if fname.endswith('.py'):
		tmppath = prepare(path)
		source = autopep8.fix_file(tmppath, autopep8.parse_args([tmppath, '--ignore=E123,E124,E127,E128,E501'])[0])
		source = lint(source, root)
		os.remove(tmppath)
	elif fname.endswith('.html') or fname.endswith('.css') or fname.endswith('.js'):
		source = text_lint(path)
	if source != None:
		with open(path, 'w') as f:
			f.write(source.encode('utf8'))
