<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Writing your Go Plugin](#writing-your-plugin)
  - [Required Variables](#required-variables)
  - [Parameters](#parameters)
  - [Logging](#logging)
  - [Cache](#cache)
  - [Plugin Status](#plugin-status)
  - [Tests](#test)

## Writing your Plugin

The following sections document things you need to know to develop quality plugins.

### Required Variables

Output variables which are defined as `required: false`, the default, don't have to be returned as JSON from the plugin.
They can be omitted and in some cases it's better to omit them. For example, the finger plugin tries to grab many
attributes of a user from the finger daemon such as the real name, shell, home directory, etc.. There's no guarantee that
all the attributes will have values, and in some cases, the absence of values doesn't mean our plugin failed. When this
is true, we can omit returning the key/value pairs instead of setting them to empty. This is a better practice because
another plugin that depends on the output variable as input in the workflow will not get an empty value and try to
proceed with it but rather the workflow stops there.

Example of returning all variables, irrespective of them having a meaningful value:
...
# Go
```

Example of returning only meaningful variables:
...
# Go
```

Example of output variables displayed in web interface
![Output Variables](imgs/output_var.png)

### Parameters

Input variables defined in the spec file are available in a dictionary called `params` where the value can be accessed by the variable/key name.
We can do this the long way or in shorter form:
```
# Go
```

### Logging

Log informational messages including warnings and errors, they're displayed to the user in the Log section of the Job Output.

![Log Output](imgs/log_var.png)

Informational logging can be done by raising an exception or logging directly, a few examples are below. 
```
# Go
```

Note that the raising of exceptions will cause the plugin to fail.

### Cache

Plugins can use persistent storage for caching files using the `enable_cache: true` in the plugin spec file.
`/var/cache` can then be used for storage across all the plugin's containers.

### Plugin Status

Plugin failures are caused by raising exceptions. Do this when something doesn't go right and the next best option is to fail.
```
# Go
```

### Tests

The test method is used to provide tests of the plugin by returning JSON. It should be completed with practical test(s) of plugin functionality.
Raising an exception will cause the test method to fail.

```
# Go
```

Tests are executed in the Komand WUI after configuring a plugin. A log of the JSON output is also viewable.

![Testing Interface](imgs/test.png)

![Testing Log](imgs/test_log.png)

The user parameters are available in the method as well.

Testing Examples:
* Successful connections to API or service
* Validating known output of command

Example for testing the `hashit` plugin that generates hashes of a string. We test against known hashes of a string.
```
# Go
```
