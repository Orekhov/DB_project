#!/usr/bin/python
import sys
try: 
    import cgitb
    cgitb.enable()
except ImportError:
    sys.stderr = sys.stdout
def cgiprint(inline=''):
    sys.stdout.write(inline)
    sys.stdout.write('\r\n')
    sys.stdout.flush()           
 
ch = 'Content-Type: text/html'
 
htm = '''<html><head>
<title>%s</title>
</head><body>
%s
</body></html>
'''
h1 = '<h1>%s</h1>'
 
if __name__ == '__main__':
    cgiprint(ch)
    cgiprint()
    title = 'Hello World'
    headline = h1 % 'Hello, world!'
    print htm % (title, headline)