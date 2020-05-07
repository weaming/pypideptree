# Pypi Dep(endency) tree
## Commands

* `pypi-dep-tree`: show dependencies tree of one python package.
* `pypi-top-pkgs`: show the top packages on the dependencies tree of multiple packages in one requirements file.

## Usage Example

```sh
$ pypi-dep-tree celery
 celery
     pytz
     billiard
     kombu
         amqp
             vine
         importlib-metadata
             zipp
             pathlib2
                 six
                 scandir
             contextlib2
             configparser
```
