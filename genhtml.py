#!/usr/bin/python

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import urllib
import cgi
import sys

def escape(unescaped):
	return cgi.escape(unescaped.encode('ascii', 'xmlcharrefreplace')) # Replace both reserved HTML characters and non-ascii characters HTMLwise

def quote_url(maybe_quoted):
	if '"' in maybe_quoted or '\\' in maybe_quoted: # We don't really care if it's malformed as long as it doesn't contain anything harmful
		return urllib.quote(maybe_quoted)
	else: # Seems good?
		return maybe_quoted

def project(name, link, people, description):
	print('<div class="project">\n\t<p>\n\t\t<a class="name-link" href="%s">%s</a>' % (quote_url(link), escape(name))) # Name
	print('\t\t<span class="participants">%s</span>' % escape(people)) # People
	print('\t</p>\n\t<p class="description">%s</p>\n</div>' % escape(description)) # Description

def person(nick, link, description):
	if not link:
		nick_html = escape(nick)
	else:
		nick_html = '<a class="nick-link" href="%s">%s</a>' % (quote_url(link), escape(nick))

	print('<div class="person">\n\t<p class="nick">%s</p>' % nick_html) # Nick with or without a link
	print('\t<p class="description">%s\n</p></div>' % escape(description)) # Description

def main(filename):
	f = open(filename, 'r')

	for line in f:
		if line[-1] == '\n':
			line = line[:-1]

		command = line.split('\t')[0]

		if command == 'rem':
			# Comment, skip
			continue
		elif command == 'project':
			# Use the "project" generator
			name, link, people, description = line.split('\t')[1:]
			project(name, link, people, description)
		elif command == 'person':
			# Use the "person" generator
			nick, link, description = line.split('\t')[1:]
			person(nick, link, description)
		elif command == '':
			# Copy rest of the line as-is
			print('\t'.join(line.split('\t')[1:]))
		else:
			print('Illegal command "%s"' % command, file=sys.stderr)
			assert(not 'Illegal command')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage %s file' % sys.argv[0], file=sys.stderr)
		sys.exit(1)
	main(sys.argv[1])
