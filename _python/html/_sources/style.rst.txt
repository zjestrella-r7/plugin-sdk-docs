Style Guide
***********

Conventions
-----------

The following sections document conventions you must follow while writing plugins.

.. only:: python

  Where rules are not defined in this document, follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_

.. only:: go

  Where rules are not defined in this document, follow `Effective Go <https://golang.org/doc/effective_go.html>`_

Plugin Names
------------

Regarding the name of the plugin as defined in the `plugin.spec.yaml` file.

``name: plugin_name``

Rules
^^^^^

* Names should be lowercase e.g. ``myplugin``
* Names should be succinct and represent their purpose or servicename e.g. ServiceNow should be ``servicenow``
* Use underscores to separate words if not a company or service name e.g. ``get_url``
* Where service and website is same, if domain is unique enough avoid top-level domain e.g. freegeoip.net should be ``freegeoip``
* Where service and website is same, if domain is not unique add top-level domain e.g. ifconfig is unix tool, web service ifconfig.co should be ``ifconfig_co``
* Numbers are valid in plugin names e.g. ``geolite2``
* Characters other than alpha-numeric and underscore are not allowed

Spec
----

Style information for the ``plugin.spec.yml`` file.

* In the spec file ``plugins.spec.yaml``, only quote titles, names, descriptions, and array types e.g. ``"[]string"``.

Indentation
^^^^^^^^^^^

Use 2 spaces for indentation::

  triggers:
    my_trigger1:
      blah:
        blah:
    my_trigger2:
      blah:
        blah:

Line Breaks
^^^^^^^^^^^

Schema sections: metadata, triggers, action, connections, should be separated by a line break.

Example::

  ...
  tags: [ "blah" ]
  icon: "blah"

  triggers:
    my_trigger1:
      blah:
        blah:
    my_trigger2:
      blah:
        blah:

    actions:
      my_action1:
        blah:
          blah:
      my_action2:
        blah:
          blah:

Quoting
-------

* Titles and descriptions fields should be double-quoted
* Of all the types, only the array types need to be double quoted. Do not quote the others.

Good::

  input:
    url:
      type: string
      description: "URL to Download"
      required: true
    timeout:
      description: "Optional timeout in seconds"
      type: integer
      default: 60
    array:
      description: "Array of things"
      type: "[]string"
    output:
      bytes:
      title: "Base64 Encoded File"

Bad::

  input:
    url:
      type: "string" # This shouldn't be quoted
      description: "URL to Download"
      required: "true" # This shouldn't be quoted
    timeout:
      type: "integer" # This shouldn't be quoted
      description: "Optional timeout in seconds"
      default: "60" # This shouldn't be quoted
  output:
    bytes:
      title: Base64 Encoded File # This should be quoted

Punctuation
-----------

Do not add end of sentence punctuation to ``titles``, ``names``, and ``descriptions``. Other fields should not have them anyway.

Branch Names
------------

Git branch names should follow rules for Plugin Names. Always work from a topic branch of the same name as the plugin.::

  git branch -b plugin_name


Tags
----

Requirements:
* Lower case characters
* Numbers permitted
* No underscores


.. code-block:: none

  tags: [ "malware", "ioc", "rat", "trojan", "remote" ]

Commit Messages
---------------

Git commits should be descriptive and describe the fix or change.

Rules
^^^^^

* Use the imperative e.g. ``Fix`` instead of ``Fixed`` or ``Fixes``
* First letter of description should be capitalized
* Use form: ``<description>``

See `Git Best Practices <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_

Examples
^^^^^^^^

Good
&&&&

.. code-block:: none

  >  Add Phishtank Plugin (#47)

  >  Update README example to match imap spec.

  >  Create README.md

  >  Remove Imap prefix to all names since imap is the package.

  >  Add basic headers (to, from, subject, date) and body to IMAP MessageEvent.  Process actual events from given inbox and send to queue.

  >  Change sleep duration to interval and remove filter for now

  >  Refactor imap plugin for expandability to additional triggers and actions. Add in validation to Connection and Trigger input.

  >  Move everything up a directory.  Fix issue where you cannot go get private repo locally.

  >  Use new API for calling triggers and actions

  >  Refactor IMAP plugin to use new plugin-sdk

  >  Update example to use new plugin-sdk

  >  Remove extraneous comments

  >  Remove -f flag from docker tag command

Bad
&&&

.. code-block:: none

  > add draft of plugin

Action & Triggers Names
-----------------------

Names are specified in the ``plugin.spec.yaml`` file. Example of good style is below::


  actions:
    match_string:
      name: "Match String"
      description: "Match string from a text file"
    match_number:
      name: "Match Number"
      description: "Match number from a text file"
    extract:
      name: "Extract"
      description: "Extract files from archive"

Rules
^^^^^

* ``name`` shouldn't be any more than one or two words. The description is intended to give the rest of the detail.
* Each word in the ``name`` should have the first letter capitalized E.g. ``Match String`` since it's a title
* First word in the ``description`` should have the first letter capitalized and not be same as ``name`` E.g. ``Match string from text file``

Property Names
--------------

Property names are defined here. These include input/output variables, actions, triggers, and connections names.

Common
^^^^^^

* ``host`` - Neutral: Used when either an IP address or domain name can be the value.
* ``address`` - Used for IP address values only (IPv4 or IPv6) e.g. ``8.8.8.8``
* ``domain`` - Used for domain name values only e.g. ``www.google.com``

Rules
&&&&&

* Names should be lowercase e.g. ``timeout``
* Names should be succinct and represent their purpose, limit of 2 words e.g. ``country_code``
* Use underscores to separate words if not succinct ``metro_code``
* Characters other than alpha and underscores are not allowed

Variable Names
--------------

.. only:: python

  Lower case variable names and underscores are permitted. CamelCase is only permitted when API's return keys in
  CamelCase and it becomes cleaner to match them, otherwise it shouldn't be used.

  Quoting
  -------

  In your code, make quoting consistent

  Good
  ^^^^

  .. code-block:: python

    return {'file': e_file ,'status': 'file not modified', 'status_code': '200'}

  Bad
  ^^^

  .. code-block:: python

    return {"file": e_file ,"status": 'file not modified', "status_code": '200'}

.. only:: go

  Standard golang style conventions apply. When in doubt, refer to `Effective Go <https://golang.org/doc/effective_go.html>`_

Logging
-------

When logging, use the following conventions:

* ``FunctionName: Message``
  * Where FunctionName is the name of the function from which logging is called
  * Capitalize the first letter in each word of the function name
  * Capitalize the first letter in each colon delimited section

Example
^^^^^^^

.. only:: python

  .. code-block:: python

    def check_cachefile(cache_file):
      logging.info('CheckCacheFile: File %s did not exist', cache_file)


.. only:: go

  .. code-block:: go

    func CheckCachefile(cacheFile) {
      log.Printf("CheckCacheFile: File %s did not exist", cacheFile)
    }

Errors
------
For logging errors returned from a library, use the library name:

* ``LibaryName: ExceptionName: Message``
  * Where LibaryName is the name of the library from which logging
  * Capitalize the first letter in each word of the library
  * Capitalize the first letter in each colon delimited section

Example
^^^^^^^

.. only:: python

  .. code-block:: python

    except requests.exceptions.HTTPError:
      logging.error('Requests: HTTPError: status code %s for %s', str(resp.status_code), url)

.. only:: go

  .. code-block:: go

    if err != nil {
      log.Printf("Library: HTTPError: %s", err.Error())
    }

Triggers
--------

Inputs
^^^^^^

For usability, all triggers should support a input called interval that is passed to the sleep mechanism in the sdks language::


  interval:
    type: integer
    description: "Poll interval in seconds"
    default: 300
    required: false


Todo
----

Remove the TODO lines that are automatically generated with the plugin, once all tasks have been completed.

Tests
-----

Each plugin should include JSON test files in the ``tests`` directory.

They are generated with ``docker run komand/<plugin> sample <action> | jq '.' > tests/<testname>``. They should be pretty
print formatted with ``jq``.

Rules
^^^^^

* Success tests for all actions
* Failure tests for all actions
* Tests for all optional inputs and for all actions
* Failure tests should be suffixed with ``_bad`` e.g. ``png_download_bad.json``
* Success tests should not be suffixed e.g. ``png_download.json``

Examples
^^^^^^^^

* Sucess: ``<desc>_<action>.json`` e.g. ``domain_lookup.json``, ``github_lookup.json``
* Failure: ``<desc>_<action>_bad.json`` e.g. ``nxdomain_lookup_bad.json``, ``private_ip_lookup_bad.json``

Examples from the ``csv`` plugin::

  tests:
  ├── 1r_filter.json
  ├── 1r_filter_bad.json
  ├── 1r_filter_bad2.json
  ├── 1r_filter_bad3.json
  ├── 1r_filter_bad4.json
  ├── 1r_space_filter.json
  └── csv_filter_bad.json
