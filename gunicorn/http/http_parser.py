# -*- coding: utf-8 -
#
# 2010 (c) Benoit Chesneau <benoitc@e-engura.com> 
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
from ctypes import *

class HttpParser(object):
    
    def __init__(self):
        self.headers = {}
        self.version = None
        self.method None
        self.path = None
        self._content_len = None        
        
    def header(self, headers, buf):
        """ take a string buff. It return 
        environ or None if parsing isn't done.
        """
        
        # wee could be smarter here
        # by just reading the array, but converting
        # is enough for now
        cs = "".join(buf)
        ld = len("\r\n\r\n")
        i = cs.find("\r\n\r\n")
        if i != -1:
            if i > 0:
                r = cs[:i]
            buf = create_string_buffer(cs[i+ ld:])
            return self.finalize_headers(headers, r)
        return None
        
    def finalize_headers(self, headers, headers_str):
        lines = headers_str.split("\r\n")
        
        # parse first line of headers
        self._first_line(lines.pop(0))
        
        # parse headers. We silently ignore 
        # bad headers' lines
        hname = ""
        for line in lines:
            if line == "\t":
                self.headers[hname] += line.strip()
            else:
                try:
                    hname =self._parse_headerl(line)
                except ValueError: 
                    # bad headers
                    pass
        headers = self.headers
        self._content_len = int(self._headers.get('Content-Length'))
        return headers
    
    def _first_line(self, line):
        method, path, version = line.strip().split(" ")
        self.version = version.strip()
        self.method = method.upper()
        self.path = path
        
    def _parse_headerl(self, line):
        name, value = line.split(": ", 1)
        name = name.strip()
        self.headers[name] = value.strip()
        return name
      
    @property
    def should_close(self):
        if self._should_close:
            return True
        if self.headers.get("Connection") == "close":
            return True
        if self.headers.get("Connection") == "Keep-Alive":
            return False
        if self.version < "HTTP/1.1":
            return True
        
    @property
    def is_chunked(self):
        transfert_encoding = self._headers.get('Transfer-Encoding', False)
        return (transfert_encoding == "chunked")
        
    @property
    def content_length(self):
        transfert_encoding = self._headers.get('Transfer-Encoding')
        content_length = self._headers.get('Content-Length')
        if transfert_encoding is None:
            if content_length is None:
                return 0
            return int(content_length)
        else:
            return None
            
    def body_eof(self):
        #TODO : add chunk
        if self._len_content == 0:
            return True
        return False
        
    def fetch_body(self, buf, data):
        dlen = len(data)
        resize(buf, sizeof(data))
        if self.is_chunked:
            # do chunk
        else:
            if self.content_len > 0:
                nr = min(len(data), self._content_len)
                # addessof may be not needed here
                memmove(addressof(buf), addressof(data), nr)
                self._content_len -= nr
                data.value = None
                resize(buf, nr)
        self.start_offset = 0
        return data     