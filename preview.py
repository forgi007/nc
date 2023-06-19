#!/usr/bin/python3

import http.server

import html
import io
import os
import socketserver
import sys
import urllib.parse

SUFFIX = urllib.parse.quote('.xhtml')


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(SUFFIX):
            path = self.path.replace(SUFFIX, '')
            f = self.send_file_in_html(path)
        else:
            f = self.send_head()
        
        if f:
            self.copyfile(f, self.wfile)
            f.close()
    
    def send_file_in_html(self, path):
        enc = sys.getfilesystemencoding()
        path = self.translate_path(path)
        (dirname, filename) = os.path.split(path)
        try:
            list = os.listdir(dirname)
            list.sort(key=lambda a: a.lower())
        except os.error:
            list = []
        try:
            nextname = list[list.index(filename)+1] + SUFFIX
        except ValueError:
            self.send_error(404, "File not found")
            return None
        except IndexError:
            nextname = ''
        
        r=[]
        r.append('<html>')
        r.append('<head><meta http-equiv="Content-Type" content="text/html; charset=%s"></head>' % enc)
        r.append('<body><a href="%s"><img src="%s"></img></a></body>'\
            % (os.path.join('./',nextname), os.path.join('./',filename) ))
        r.append('</html>')
        
        encoded = '\n'.join(r).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f
    
    def list_directory(self, path):
        ''' Overwriting SimpleHTTPRequestHandler.list_directory()
            Modify marked with `####`
        '''
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        displaypath = html.escape(urllib.parse.unquote(self.path))
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            if os.path.isfile(fullname):        ####
                linkname = name + SUFFIX       ####
            r.append('<li><a href="%s">%s</a></li>'
                    % (urllib.parse.quote(linkname), html.escape(displayname)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f
    

if __name__=='__main__':
    httpd = socketserver.TCPServer(("", 8000), Handler)
    print("Serving on 0.0.0.0:8000 ...")
    httpd.serve_forever()
