"""
https://github.com/pywren/pywren/blob/master/pywren/serialize/default_preinstalls.py

All modules that are pre-installed on the base Multyvac layer.
Generated by running the following on an empty layer:
    mods = list(pkgutil.iter_modules())
    for entry in sorted([(mod, is_pkg) for _,mod,is_pkg in mods]):
        print entry + ','
"""

# list of tuples [(package name, is a package?), ...]
modules = [
    ('BaseHTTPServer', False),
    ('Bastion', False),
    ('CDROM', False),
    ('CGIHTTPServer', False),
    ('Canvas', False),
    ('ConfigParser', False),
    ('Cookie', False),
    ('DLFCN', False),
    ('Dialog', False),
    ('DocXMLRPCServer', False),
    ('FileDialog', False),
    ('FixTk', False),
    ('HTMLParser', False),
    ('IN', False),
    ('MimeWriter', False),
    ('Queue', False),
    ('ScrolledText', False),
    ('SimpleDialog', False),
    ('SimpleHTTPServer', False),
    ('SimpleXMLRPCServer', False),
    ('SocketServer', False),
    ('StringIO', False),
    ('TYPES', False),
    ('Tix', False),
    ('Tkconstants', False),
    ('Tkdnd', False),
    ('Tkinter', False),
    ('UserDict', False),
    ('UserList', False),
    ('UserString', False),
    ('_LWPCookieJar', False),
    ('_MozillaCookieJar', False),
    ('__future__', False),
    ('_abcoll', False),
    ('_bsddb', False),
    ('_codecs_cn', False),
    ('_codecs_hk', False),
    ('_codecs_iso2022', False),
    ('_codecs_jp', False),
    ('_codecs_kr', False),
    ('_codecs_tw', False),
    ('_csv', False),
    ('_ctypes', False),
    ('_ctypes_test', False),
    ('_curses', False),
    ('_curses_panel', False),
    ('_elementtree', False),
    ('_heapq', False),
    ('_hotshot', False),
    ('_io', False),
    ('_json', False),
    ('_lsprof', False),
    ('_multibytecodec', False),
    ('_multiprocessing', False),
    ('_pyio', False),
    ('_sqlite3', False),
    ('_strptime', False),
    ('_testcapi', False),
    ('_threading_local', False),
    ('_weakrefset', False),
    ('abc', False),
    ('aifc', False),
    ('antigravity', False),
    ('anydbm', False),
    ('argparse', False),
    ('ast', False),
    ('asynchat', False),
    ('asyncore', False),
    ('atexit', False),
    ('audiodev', False),
    ('audioop', False),
    ('base64', False),
    ('bdb', False),
    ('binhex', False),
    ('bisect', False),
    ('bs4', True),
    ('bsddb', True),
    ('bz2', False),
    ('cProfile', False),
    ('calendar', False),
    ('certifi', False),
    ('cgi', False),
    ('cgitb', False),
    ('chunk', False),
    ('cmd', False),
    ('code', False),
    ('codecs', False),
    ('codeop', False),
    ('collections', False),
    ('colorsys', False),
    ('commands', False),
    ('compileall', False),
    ('compiler', True),
    ('contextlib', False),
    ('cookielib', False),
    ('copy', False),
    ('copy_reg', False),
    ('crypt', False),
    ('csv', False),
    ('ctypes', True),
    ('curses', True),
    ('datetime', False),
    ('dbhash', False),
    ('dbm', False),
    ('debconf', False),
    ('decimal', False),
    ('difflib', False),
    ('dircache', False),
    ('dis', False),
    ('distutils', True),
    ('doctest', False),
    ('dumbdbm', False),
    ('dummy_thread', False),
    ('dummy_threading', False),
    ('email', True),
    ('encodings', True),
    ('filecmp', False),
    ('fileinput', False),
    ('fnmatch', False),
    ('formatter', False),
    ('fpectl', False),
    ('fpformat', False),
    ('fractions', False),
    ('ftplib', False),
    ('functools', False),
    ('future_builtins', False),
    ('genericpath', False),
    ('getopt', False),
    ('getpass', False),
    ('gettext', False),
    ('glob', False),
    ('gzip', False),
    ('hashlib', False),
    ('heapq', False),
    ('hmac', False),
    ('hotshot', True),
    ('htmlentitydefs', False),
    ('htmllib', False),
    ('httplib', False),
    ('ihooks', False),
    ('imaplib', False),
    ('imghdr', False),
    ('importlib', True),
    ('imputil', False),
    ('inspect', False),
    ('io', False),
    ('json', True),
    ('keyword', False),
    ('lib2to3', True),
    ('linecache', False),
    ('linuxaudiodev', False),
    ('locale', False),
    ('logging', True),
    ('lsb_release', False),
    ('macpath', False),
    ('macurl2path', False),
    ('mailbox', False),
    ('mailcap', False),
    ('markupbase', False),
    ('md5', False),
    ('mhlib', False),
    ('mimetools', False),
    ('mimetypes', False),
    ('mimify', False),
    ('mmap', False),
    ('modulefinder', False),
    ('multifile', False),
    ('multiprocessing', True),
    ('multyvac', True),
    ('multyvacinit', True),
    ('mutex', False),
    ('netrc', False),
    ('new', False),
    ('nis', False),
    ('nntplib', False),
    ('ntpath', False),
    ('nturl2path', False),
    ('numbers', False),
    ('opcode', False),
    ('optparse', False),
    ('os', False),
    ('os2emxpath', False),
    ('ossaudiodev', False),
    ('parser', False),
    ('pdb', False),
    ('pickle', False),
    ('pickletools', False),
    ('pipes', False),
    ('pkgutil', False),
    ('platform', False),
    ('plistlib', False),
    ('popen2', False),
    ('poplib', False),
    ('posixfile', False),
    ('posixpath', False),
    ('pprint', False),
    ('profile', False),
    ('pstats', False),
    ('pty', False),
    ('py_compile', False),
    ('pyclbr', False),
    ('pydoc', False),
    ('pydoc_data', True),
    ('pyexpat', False),
    ('quopri', False),
    ('random', False),
    ('re', False),
    ('readline', False),
    ('repr', False),
    ('resource', False),
    ('requests', True),
    ('rexec', False),
    ('rfc822', False),
    ('rlcompleter', False),
    ('robotparser', False),
    ('runpy', False),
    ('sched', False),
    ('sets', False),
    ('sgmllib', False),
    ('sha', False),
    ('shelve', False),
    ('shlex', False),
    ('shutil', False),
    ('site', False),
    ('sitecustomize', False),
    ('smtpd', False),
    ('smtplib', False),
    ('sndhdr', False),
    ('socket', False),
    ('sqlite3', True),
    ('sre', False),
    ('sre_compile', False),
    ('sre_constants', False),
    ('sre_parse', False),
    ('ssl', False),
    ('stat', False),
    ('statvfs', False),
    ('string', False),
    ('stringold', False),
    ('stringprep', False),
    ('struct', False),
    ('subprocess', False),
    ('sunau', False),
    ('sunaudio', False),
    ('symbol', False),
    ('symtable', False),
    ('sysconfig', False),
    ('tabnanny', False),
    ('tarfile', False),
    ('telnetlib', False),
    ('tempfile', False),
    ('termios', False),
    ('test', True),
    ('textwrap', False),
    ('this', False),
    ('threading', False),
    ('timeit', False),
    ('tkColorChooser', False),
    ('tkCommonDialog', False),
    ('tkFileDialog', False),
    ('tkFont', False),
    ('tkMessageBox', False),
    ('tkSimpleDialog', False),
    ('toaiff', False),
    ('token', False),
    ('tokenize', False),
    ('trace', False),
    ('traceback', False),
    ('ttk', False),
    ('tty', False),
    ('turtle', False),
    ('types', False),
    ('unittest', True),
    ('urllib', False),
    ('urllib2', False),
    ('urlparse', False),
    ('user', False),
    ('uu', False),
    ('uuid', False),
    ('warnings', False),
    ('wave', False),
    ('weakref', False),
    ('webbrowser', False),
    ('whichdb', False),
    ('wsgiref', True),
    ('xdrlib', False),
    ('xml', True),
    ('xmllib', False),
    ('xmlrpclib', False),
    ('zipfile', False),
    ('sphinx', False),
    ('pygments', False),
    ('docutils', False),
    ('boto3', False),
    ('botocore', False),
    ('boto', False),
    ('yaml', False),
    ('builtins', False),
    ('enum', False),
    ('colorama', False),
    ('pkg_resources', False),
    ('click', False),
    ('numpy', False),
    ('matplotlib', False),
    ('OpenGL', False),
    ('scipy', False),
    ('sklearn', False),
    ('cvxpy', False),
    ('cvxopt', False),
    ('future', False),
    ('six', False),
    ('glob2', False),
    ('tblib', False),
    ('dill', False),
    ('multiprocess', False),
]
