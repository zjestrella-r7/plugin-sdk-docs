<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Conventions](#conventions)
  - [Plugin Names](#plugin-names)
  - [Branch Names](#branch-names)
  - [Commit Messages](#commit-messages)
  - [Property Names](#property-names)
  - [Loggign](#logging)
  - [Tests](#tests)

## Conventions

The following sections document conventions you must follow while writing plugins

### Plugin Names

Regarding the name of the plugin as defined in the `plugin.spec.yaml` file.

`name: plugin_name`

##### Rules:

* Names should be lowercase e.g. `myplugin`
* Names should be succinct and represent their purpose or servicename e.g. ServiceNow should be `servicenow`
* Use underscores to separate words if not a company or service name e.g. `get_url`
* For websites, if domain is unique enough avoid tld e.g. freegeoip.net should be `freegeoip`
* For websites, if domain is not unique enough add tld e.g. ifconfig is unix tool, web service ifconfig.co should be `ifconfig_co`
* Numbers are valid in the plugin names e.g. `geolite2`
* Characters other than alpha-numeric and underscore are not allowed

### Branch Names

Git branch names should follow [Plugin Names](#plugin-names) rules. Always work from a topic branch of the same name as the plugin.

```
git branch -b plugin_name
```

### Commit Messages

Git commits should be descriptive and describe the fix or change.

#### Rules

* Use the imperative e.g. `Fix` instead of `Fixed` or `Fixes`
* First letter of description should be capitalized
* Use form: `<description>`

See [Git Best Practices](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)

#### Examples

##### Good: 

>  Add Phishtank Plugin (#47)
>  Update README example to match imap spec.
>  Create README.md
>  Remove Imap prefix to all names since imap is the package.
>  Add basic headers (to, from, subject, date) and body to IMAP MessageEvent.  Process actual events from given inbox and send to queue.
>  Change sleep duration to frequency and remove filter for now
>  Refactor imap plugin for expandability to additional triggers and actions. Add in validation to Connection and Trigger input.
>  Move everything up a directory.  Fix issue where you cannot go get private repo locally.
>  Use new API for calling triggers and actions
>  Refactor IMAP plugin to use new plugin-sdk
>  Update example to use new plugin-sdk
>  Remove extraneous comments
>  Remove -f flag from docker tag command

##### Bad:

> add draft of plugin

### Property Names

Properties, are defined here. These include input/output variables, actions, triggers, and connections names.

##### Common

* `host` - Neutral: Used when either an IP address or domain name can be the value. 
* `address` - Used for IP address values only (IPv4 or IPv6) e.g. `8.8.8.8`
* `domain` - Used for domain name values only e.g. `www.google.com`

##### Rules:

* Names should be lowercase e.g. `timeout`
* Names should be succinct and represent their purpose, limit of 2 words e.g. `country_code`
* Use underscores to separate words if not succinct `metro_code`
* Characters other alpha and underscores are not allowed

### Logging

When logging, 

#### Exceptions

* Write library where the exception is being handled from
* Write the exception type 
* Write description with values used to help debug the error

Form: `'<Library>: <Exception/Error>: <Description>'`

```
except requests.exceptions.HTTPError:
  logging.error('Requests: HTTPError: status code %s for %s', str(resp.status_code), url)
except requests.exceptions.Timeout:
  logging.error('Requests: Timeout for %s', url)
except requests.exceptions.TooManyRedirects:
  logging.error('Requests: TooManyRedirects for %s', url)
except requests.ConnectionError:
  logging.error('Requests: ConnectionError for %s', url)
```

### Tests

Each plugin should include JSON test files in the `tests` directory.

The are generated with `docker run komand/<plugin> sample <action> | jq '.' > tests/<testname>`

#### Rules

* Success tests for all actions
* Failure tests for all actions
* Tests for all optional inputs and for all actions
* Failure tests should be suffixed with `_bad` e.g. `png_download_bad.json`
* Success tests should not be suffixed e.g. `png_download.json`

Examples:
* Sucess: `<desc>_<action>.json` e.g. `domain_lookup.json`, `github_lookup.json`
* Failure: `<desc>_<action>_bad.json` e.g. `nxdomain_lookup_bad.json`, `private_ip_lookup_bad.json`

Examples from the `csv` plugin.
```
tests:
├── 1r_filter.json
├── 1r_filter_bad.json
├── 1r_filter_bad2.json
├── 1r_filter_bad3.json
├── 1r_filter_bad4.json
├── 1r_space_filter.json
└── csv_filter_bad.json
```
