<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Writing your Go Plugin](writing-your-plugin)
  - [Variables](#variables)
  - [Parameters](#parameters)
  - [Logging](#logging)
  - [Cache](#cache)
  - [Plugin Status](#plugin-status)
  - [Tests](#test)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Writing your Plugin

The following sections document things you need to know to develop quality plugins.

#### Variables

Variables

![Output Variables](imgs/output_var.png)

#### Parameters

Input variables defined in the spec file are available in a dictionary called `params` where the value can be accessed by the variable/key name.
We can do this the long way or in shorter form:
```
# Python
self.input.parameters['var']
params['var']
```

#### Logging

Log informational messages including warnings and errors, they're displayed to the user in the Log section of the Job Output.

![Log Output](imgs/log_var.png)

Informational logging can be done by raising an exception or logging directly, a few examples are below. 
```
# Python
logging.info("connecting")
raise ValueError('connecting')
raise Exception('connecting')
```

Note that the raising of exceptions will cause the plugin to fail.

### Cache

Plugins can use persistent storage for caching files using the `enable_cache: true` in the plugin spec file.
`/var/cache` can then be used for storage across all the plugin's containers.

### Plugin Status

Plugin failures are caused by raising exceptions. Do this when something doesn't go right and the next best option is to fail.
```
# Python
raise ValueError('connecting')
raise Exception('connecting')
```

#### Tests

The test method is used to provide tests of the plugin by returning JSON. It should be completed with practical test(s) of plugin functionality.
Raising an exception will cause the test method to fail.

```
# Python
def test(self, params={}):
  """TODO: Test action"""
  return {}
```

Tests are executed in the Komand WUI after configuring a plugin. A log of the JSON output is also viewable.

![Testing Interface](imgs/test.png)

![Testing Log](imgs/test_log.png)

The user parameters are available in the method as well.

Testing Examples:
* Successful connections to API or service
* Validating known output of command
