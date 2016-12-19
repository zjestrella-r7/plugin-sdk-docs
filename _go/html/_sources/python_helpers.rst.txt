To make use of the helpers, import the komand namespace

You can make use of ``dir`` python builtin to fund out more about a specific function

``dir(komand.helper.clean_dict)``

You can also use an sdk builtin ``help`` method to display information in the plugin output, although this is for testing only and will result in an error in the plugin.
Avoid leaving these calls in the final plugin. You should strive to rely on the official documentation where possible.

``help(komand.helper.clean_dict)``

clean_dict(dict)
^^^^^^^^^^^^^^^^

Takes a dictionary as an argument and returns a new, cleaned, dictionary

.. code-block:: python

  >>> a = { 'a': 'stuff', 'b': 1, 'c': None, 'd': 'more', 'e': '' }
  """Keys c and e are removed"""
  >>> komand.helper.clean_dict(a)
  {'a': 'stuff', 'b': 1, 'd': 'more'}

clean_list(list)
^^^^^^^^^^^^^^^^

Takes a list as an argument and returns a new, cleaned, list

.. code-block:: python

  >>> lst = [ 'stuff', 1, None, 'more', '', None, '' ]
  >>> clean_list(lst)
  ['stuff', 1, 'more']

open_file(path)
^^^^^^^^^^^^^^^

Takes a file path as a string to open and returns a file object on success or None

.. code-block:: python

  >>> f = open_file('/tmp/testfile')
  >>> f.read()
  'test\n'

check_cachefile(path)
^^^^^^^^^^^^^^^^^^^^^

Takes a string of the file path to check

.. code-block:: python

  >>> komand.helper.check_cachefile('/var/cache/mycache')
  True
  """This works too, /var/cache is not required"""
  >>> komand.helper.check_cachefile('mycache')
  True
  >>> komand.helper.check_cachefile('nofile')
  False

remove_cachefile(path)
^^^^^^^^^^^^^^^^^^^^^^

Takes a file path as a string

.. code-block:: python

  >>> os.listdir('/var/cache')
  ['test']
  >>> komand.helper.remove_cachefile('test')
  True
  >>> os.listdir('/var/cache')

open_cachefile(file)
^^^^^^^^^^^^^^^^^^^^

Takes a file path as a string

.. code-block:: python

  >>> f = komand.helper.open_cachefile('/var/cache/test')
  >>> f.read()
  'stuff\n'
  >>> os.listdir('/var/cache')
  []
  >>> f = komand.helper.open_cachefile('/var/cache/myplugin/cache.file')
  """The file has been created"""
  >>> komand.helper.check_cachefile('/var/cache/myplugin/cache.file')
  True

lock_cache(file)
^^^^^^^^^^^^^^^^

Takes a file path as a string

.. code-block:: python

  >>> f = komand.helper.lock_cache('/var/cache/lock/lock1')
  >>> f
  True

unlock_cache(file, delay)
^^^^^^^^^^^^^^^^^^^^^^^^^

Takes a file path as a string and a delay length in seconds as an int or float

.. code-block:: python

  >>> delay = 60
  >>> f = komand.helper.unlock_cache('/var/cache/lock/lock1', delay)
  """Sixty seconds later"""
  >>> f
  True
  >>> file_name = '/var/cache/lock/lock1'
  >>> f = komand.helper.unlock_cache(file_name, 60)
  """Sixty seconds later"""
  >>> f
  True

get_hashes_string(str)
^^^^^^^^^^^^^^^^^^^^^^

Returns a dictionary of common hashes from a string

.. code-block:: python

  >>> get_hashes_string('thisisastring')
  {u'sha256': '572642d5581b8b466da59e87bf267ceb7b2afd880b59ed7573edff4d980eb1d5', u'sha1':
  '93697ac6942965a0814ed2e4ded7251429e5c7a7', u'sha512':
  '9145416eb9cc0c9ff3aecbe9a400f21ca2b99c927f63a9a245d22ac4fe6fe27036643e373708e3bdf7ace4f3b52573182ec6d1f38c7d25f9e06144617ad1cdc8',
  u'md5': '0bba161a7165a211c7435c950ee78438'}

check_hashes(src, checksum)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns a boolean on whether checksum was a hash of provided string

.. code-block:: python

  >>> check_hashes('thisisastring', '0bba161a7165a211c7435c950ee78438')
  True
  >>> check_hashes('thisisanotherstring', '0bba161a7165a211c7435c950ee78438')
  False

extract_value()
^^^^^^^^^^^^^^^

Takes 4 arguments that regexes/patterns as strings

.. code-block:: python

  >>> string = '\n\tShell: /bin/bash\n\t'
  >>> komand.helper.extract_value(r'\s', 'Shell', r':\s(.*)\s', string)
  '/bin/bash'

open_url(url)
^^^^^^^^^^^^^

Takes a URL as a string and optionally a timeout as an int, verify as a boolean, and a dictionary of headers

A urllib2 obj is returned upon success. `None` is returned if a 304 Not modified is the response.

.. code-block:: python

  >>> urlobj = open_url('http://google.com')
  >>> urlobj.read()
  '<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en"><head><meta content="Se...'
  >>> urlobj = open_url(url, Range='bytes=0-3', Authorization='aslfasdfasdfasdfasdf')
  >>> urlobj.read()
  Auth
  >>> urlobj = open_url(url, timeout=1, User_Agent='curl/0.7.9', If_None_Match=etag)
  ERROR:root:HTTPError: 304 for http://24.151.224.211/ui/1.0.1.1038/dynamic/login.html
  >>> type(a)
  <type 'NoneType'>
  >>> urlobj = open_url(url, User_Agent='curl/0.7.9', If_Modified_Since=mod)
  ERROR:root:HTTPError: 304 for http://24.151.224.211/ui/1.0.1.1038/dynamic/login.html

get_url_filename(url)
^^^^^^^^^^^^^^^^^^^^^

Takes a URL as a string, returns filename as string or None

.. code-block:: python

  >>> url = 'http://www.irongeek.com/robots.txt'
  >>> get_url_filename(url)
  'robots.txt'
  >>> get_url_filename('http://203.66.168.223:83/')
  'Create_By_AutoWeb.htm'
  >>> if get_url_filename('http://www.google.com') is None:
  ...   print 'No file found'
  No file found

exec_command(path_with_args)

Takes a command and its arguments as a string

.. code-block:: python

  >>> exec_command('/bin/ls')
  {'rcode': 0, 'stderr': '', 'stdout':
  'GO.md\nPYTHON.md\nREADME.md\nSPEC.md\nball.pyc\nimgs\nold.py\nplugins.py\nplugins.pyc\nstatic.py\nstatic.pyc\n'}
