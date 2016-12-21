The godoc for the plugin-sdk-go project is another good source of in-depth documentation for these methods. You can find a link to the godoc for each package below.

Package cache
^^^^^^^^^^^^^

`cache GoDoc <https://godoc.org/github.com/komand/plugin-sdk-go/plugin/cache>`_

The cache package contains all the functionality needed to operate with the plugin concept of a ``cache``, which currently is the
local plugin filesystem, under the route ``/var/cache/``. Therefore, the paths you pass into these methods should all assume
they are relative to ``/var/cache/`` or ``var/cache/lock`` for the Lock suite of methods.

They should not begin with a leading slash (although if they do, it will be trimmed).

You can append sub-paths to the name argument, and they will be respected. If the sub directories do not exist, they will be created.

CheckCachFile(name string) (bool, error)
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

``CheckCacheFile`` checks if a file exists in ``/var/cache``. If there is an error in checking the filesystem, it will be returned alongside a ``false``

Therefore, you should always expect to handle this error just in case. A result of ``true`` will never have an error.

OpenCacheFile(name string) (\*os.File, error)
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

``OpenCacheFile`` will return a pointer to a file handle for the caller to use as they see fit.

The caller must remember to call `Close()` on the file before they are done with it.

If the file does not exist, it will be created.

If there are any errors, an error will be returned along with a nil pointer for the ``os.File``

RemoveCacheFile(name string) error
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

``RemoveCacheFile`` will delete the file with the name provided, but will not remove any directories.

If there is an error removing the file, the method will return an error

LockCacheFile(name string) (bool, error)
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

``LockCacheFile`` will create a ``lock`` file if and only if it does not already exist.

If anything unexpected occurs when attempting to grab the lock, you will receive a return value  of false, err

If the file already exists, the lock is held by another process, and you will receive a return value of false, nil

If the file does not exist, and is able to be grabbed, you will receive a return value of true, nil

A call to this method will block the current thread until it is able to receive the lock successfully. At present, there is no timeout.
It will wait 1 millisecond in between each attempt to grab the lock, so as not to needlessly burn CPU cycles.

UnlockCacheFile(name string, delay \*time.Duration) (bool, error)
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

``UnlockCacheFile`` will remove a ``lock`` file if it exists.

It will optionally wait the provided delay value, if one was provided. This is a convenience for the caller, who may be using locks to help act as a
throttling / rate limiting mechanism to prevent too many concurrent calls to a given service.

If anything unexpected goes wrong, you'll receive a return value of false, err

If nothing unexpected goes wrong, you'll receive either true, nil or false, nil depending on how the underyling call to ``os.Remove`` returns

Package utils
^^^^^^^^^^^^^

`utils GoDoc <https://godoc.org/github.com/komand/plugin-sdk-go/plugin/utils>`_

The utils package has some simple helpers for basic operations that don't really belong anywhere else.

OpenFile(name string, flags int, perms os.FilePerms) (\* os.File, error)
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

``OpenFile`` is a convenience for dealing with the file system at a slightly lower level than what you might find in the ``cache`` package

It is not scoped to any particular directory, nor does it assume to know anything about the name you pass in, and so you should prefix it with a slash to start at the root of the filesystem if you so intend (recommended)

The caller is responsible for knowing the correct flags and permissions for the file.

The caller is responsible for closing the file when they are done with it.

DoesFileExist(path string) (bool, error)
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

``DoesFileExist`` will check if a file exists in the local file system.

It is not scoped to any particular directory, nor does it assume to know anything about the name you pass in, and so you should prefix it with a slash to start at the root of the filesystem if you so intend (recommended)

If there are any unexpected errors, it will return false, error

If the file does not exist, it will return false, nil

Otherwise, it will return true, nil
