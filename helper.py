import base64
import hashlib
import logging
import json
import re
import requests
import subprocess
import os
import urllib2

def extract_value(begin, key, end, s):
  '''Returns a string from a given key/pattern using provided regexes
  It takes 4 arguments:
  * begin: a regex/pattern to match left side
  * key: a regex/pattern that should be the key
  * end: a regex/pattern to match the right side
  * s: the string to extract values from

  Example: The following will use pull out the /bin/bash from the string s
  s = '\nShell: /bin/bash\n'
  shell = get_value(r'\s', 'Shell', r':\s(.*)\s', s)

  This function works well when you have a list of keys to iterate through where the pattern is the same.
  '''
  regex = begin + key + end
  r = re.search(regex, s)
  if hasattr(r, 'group'):
    if r.lastindex == 1:
      return r.group(1)
  return None

def clean_dict(dictionary):
  '''Returns a new but cleaned dictionary:

  * Keys with None type values are removed
  * Keys with empty string values are removed

  This function is designed so we only return useful data
  '''
  newdict = dict(dictionary)
  for key in dictionary.keys():
    if dictionary.get(key) is None:
      del newdict[key]
    if dictionary[key] == '':
      del newdict[key]
  return newdict

def clean_list(lst):
  '''Returns a new but cleaned list:

  * None type values are removed
  * Empty string values are removed

  This function is designed so we only return useful data
  '''
  newlist = list(lst)
  for i in lst:
    if i is None:
      newlist.remove(i)
    if i == '':
      newlist.remove(i)
  return newlist

def check_hashes(src, checksum):
  '''Return boolean on whether a hash matches a file or string'''
  if type(src) is str:
    hashes = get_hashes_string(src)
  else:
    logging.error('CheckHashes: Argument must be a string')
    raise Exception('CheckHashes: Failed to check')
  alg = [ 'md5', 'sha1', 'sha256', 'sha512' ]
  for alg in hashes:
    if hashes[alg] == checksum:
      return True
  logging.info('Check Hashes: No checksum match')
  return False

def get_hashes_string(s):
  '''Return a dictionary of hashes for a string'''
  hashes={}
  hashes['md5']    = hashlib.md5(s).hexdigest()
  hashes['sha1']   = hashlib.sha1(s).hexdigest()
  hashes['sha256'] = hashlib.sha256(s).hexdigest()
  hashes['sha512'] = hashlib.sha512(s).hexdigest()
  return hashes

def check_cachefile(cache_file):
  '''Return boolean on whether cachefile exists'''
  cache_dir  = '/var/cache'
  if cache_dir not in cache_file:
    cache_file = cache_dir + '/' + cache_file
  if os.path.isdir(cache_dir):
    if os.path.isfile(cache_file):
      logging.info('Cache file exists', cache_file)
      return True
    logging.info('Cache file %s did not exist, skipping', cache_file)
  return False

def open_file(file_path):
  '''Return file object if it exists'''
  dirname = os.path.dirname(file_path)
  filename = os.path.basename(file_path)
  if os.path.isdir(dirname):
    if os.path.isfile(file_path):
      f = open(file_path, 'rb')
      return f
    else:
      logging.info('OpenFile: File %s is not a file or does not exist ', filename)
  else:
    logging.error('OpenFile: Directory %s is not a directory or does not exist', dirname)

def open_cachefile(cache_file):
  '''Return file object if cachefile exists, create and return new cachefile if it doesn't exist'''
  cache_dir  = '/var/cache'
  if cache_dir not in cache_file:
    cache_file = cache_dir + '/' + cache_file
  if os.path.isdir(cache_dir):
    if os.path.isfile(cache_file):
      f = open(cache_file, 'r+')
      logging.info('Cache file %s exists, returning it', cache_file)
    else:
      if not os.path.isdir(os.path.dirname(cache_file)):
        os.makedirs(os.path.dirname(cache_file))
      f = open(cache_file, 'w')
      logging.info('Cache file %s created', cache_file)
    return f
  logging.error('%s is not a directory or does not exist', cache_dir)

def remove_cachefile(cache_file):
  '''Returns boolean on whether cachefile was removed'''
  cache_dir  = '/var/cache'
  if cache_dir not in cache_file:
    cache_file = cache_dir + '/' + cache_file
  if os.path.isdir(cache_dir):
    if os.path.isfile(cache_file):
      os.remove(cache_file)
      return True
    logging.info('Cache file %s did not exist, not removing it', cache_file)
  return False

def open_url(url):
  '''Return url object given a URL as a string'''
  try:
    resp = urllib2.urlopen(url)
    return resp
  except urllib2.HTTPError, e:
    logging.error('HTTPError: %s for %s', str(e.code), url)
  except urllib2.URLError, e:
    logging.error('URLError: %s for %s', str(e.reason), url)
  raise Exception('URL Request Failed')

def check_url(url):
  '''Return boolean on whether we can access url successfully
  We submit an HTTP HEAD request to check the status. This way we don't download the file for performance.
  '''
  try:
    resp = requests.head(url)
    resp.raise_for_status()
    if resp.status_code >= 200 and resp.status_code <= 399:
      return True
  except requests.exceptions.HTTPError:
    logging.error('Requests: HTTPError: status code %s for %s', str(resp.status_code), url)
  except requests.exceptions.Timeout:
    logging.error('Requests: Timeout for %s', url)
  except requests.exceptions.TooManyRedirects:
    logging.error('Requests: TooManyRedirects for %s', url)
  except requests.ConnectionError:
    logging.error('Requests: ConnectionError for %s', url)
  return False

def exec_command(command):
  '''Return dict with keys stdout, stderr, and return code of executed subprocess command'''
  try:
     p = subprocess.Popen(command,
       shell=True,
       stdin=subprocess.PIPE,
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE,
       close_fds=True)
     stdout = p.stdout.read()
     stderr = p.stderr.read()
     rcode  = p.poll()
     return { 'stdout': stdout, 'stderr': stderr, 'rcode': rcode }
  except OSError as e:
    logging.error('SubprocessError: %s %s: %s', str(e.filename), str(e.strerror), str(e.errno))
  raise Exception('Subprocess failed')

def encode_file(file_path):
  '''Return a string of base64 encoded file provided as an absolute file path'''
  try:
    f = open_file(file_path)
    efile = base64.b64encode(f.read())
  except (IOError, OSError) as e:
    logging.error('File open error: %s', e.strerror)
    raise Exception('File Open Failed')
  finally:
    if type(f) is file:
      f.close()
  return efile

def check_url_modified(url):
  '''Return boolean on whether the url has been modified.
  We submit an HTTP HEAD request to check the status. This way we don't download the file for performance.
  '''
  try:
    resp = requests.head(url)
    resp.raise_for_status()
    if resp.status_code == 304:
      return False
    if resp.status_code == 200:
      return True
  except requests.exceptions.HTTPError:
    logging.error('Requests: HTTPError: status code %s for %s', str(resp.status_code), url)
  except requests.exceptions.Timeout:
    logging.error('Requests: Timeout for %s', url)
  except requests.exceptions.TooManyRedirects:
    logging.error('Requests: TooManyRedirects for %s', url)
  except requests.ConnectionError:
    logging.error('Requests: ConnectionError for %s', url)
  return False

def get_url_content_disposition(headers):
  '''Return filename as string from content-disposition by supplying requests headers'''
  # Dict is case-insensitive
  if headers.get('content-disposition'):
    filename = re.findall("filename=(.+)", headers['content-disposition'])
    return str(filename[0].strip('"'))
  return None

def get_url_path_filename(url):
  '''Return filename from url as string if we have a file extension, otherwise return None.'''
  if url.find('/', 9) == -1:
    return None
  name = os.path.basename(url)
  try:
    for n in range(-1,-5,-1):
      if name[n].endswith('.'):
        return name
  except IndexError:
    logging.error('Range: IndexError: URL basename is short: %s of %s', name, url)
    return None
  return None

def get_url_filename(url):
  '''Return filename as string from url by content-disposition or url path, or return None if not found'''
  try:
    resp = requests.head(url)
    resp.raise_for_status()
    name = get_url_content_disposition(resp.headers)
    if name is not None:
      return name
    name = get_url_path_filename(url)
    if name is not None:
      return name
    return None
  except requests.exceptions.MissingSchema:
    logging.error('Requests: MissingSchema: Requires ftp|http(s):// for %s', url)
  except requests.exceptions.HTTPError:
    logging.error('Requests: HTTPError: status code %s for %s', str(resp.status_code), url)
  except requests.exceptions.Timeout:
    logging.error('Requests: Timeout for %s', url)
  except requests.exceptions.TooManyRedirects:
    logging.error('Requests: TooManyRedirects for %s', url)
  except requests.ConnectionError:
    logging.error('Requests: ConnectionError for %s', url)
