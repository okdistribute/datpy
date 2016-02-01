# DAT Python API

This is a client in python for [Dat](https://dat-data.com)'s command-line API.

[![travis](https://img.shields.io/travis/karissa/datpy.svg?style=flat)](https://travis-ci.org/karissa/datpy)
[![pypi](https://img.shields.io/pypi/dm/datpy.svg?style=flat)](https://pypi.python.org/pypi/datpy)
[![pypi](https://img.shields.io/pypi/v/datpy.svg?style=flat)](https://pypi.python.org/pypi/datpy)
[![pypi](https://img.shields.io/pypi/pyversions/datpy.svg?style=flat)](https://pypi.python.org/pypi/datpy)

## What is Dat?

Dat is a peer-to-peer data sync tool. Read the [docs](https://github.com/maxogden/dat) to learn more about Dat.

## Installation

  0. Install [dat](https://github.com/maxogden/dat)

    `npm install -g dat`

  1. Install datpy

    `pip install datpy`

## Usage

This is a new library and it needs work! Please don't hesitate to send a pull request or to open an issue if you find something wrong or broken.


```python
import datpy
```

## datpy.Dat(home='~/.dat')

`Dat` is a class that binds to some global Dat. By default, the metadata storage is placed in `~/.dat`.

```python
> import datpy
> mydat = datpy.Dat()
```

For each command, a `dat` instance accepts any of the options supported by Dat's [commandline api](http://github.com/datproject/docs).

### `mydat.link(, path=None, **kwargs*)`

Creates a link to the data and begins to seed it over the network.

Example:

```python
> dat.link('./path/to/my/data')
'dat://a53d819bdf5c3496a2855df83daaac885686cac4b0bccfc580741b04898e3b32'
```

### `mydat.download(link, path=None)`

Downloads the link to the local hard drive. This will open a tcp connection to the public network.

You can provide a `path` argument to download the data to a specific folder.

```python
> dat.download()
```

### `mydat.close()`

Closes any tcp connections opened with `download` or `link`.

## Contributing

First, create a fork, then install the requirements. Make your change and open a pull request. You might need to create a virtual environment, depending on your setup.

```bash
$ git clone http://github.com/<your-fork>/datpy
$ pip install -r requirements.txt
$ git commit -am "BUG: there was a bug here fixes #33"
$ git push origin master
 ... open pull request!
```

## Testing

Install `nosetests` for the best testing environment. If you don't have `pandas` installed, it will skip the pandas tests.

```bash
nosetests
```

To run just one test

```bash
nosetests test.py:SimpleTest.test_rows
```

To run the entire suite without `nosetests`:

```bash
python tests/test.py
```

## Publishing

First, edit `setup.py` to bump the version number on both the `version` key and the `download_url`. Then, to push to pip/pypi:

```
python setup.py register -r pypi
python setup.py sdist upload -r pypi
```


# BSD Licensed

Copyright (c) 2014 Karissa McKelvey and contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
