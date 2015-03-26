# DAT Python API

This is a client in python for [Dat](https://dat-data.com). There are functions to interact with the REST api as well as local hooks. It integrates easily with [pandas](http://pandas.pydata.org).

Hello, collaboration.

## What is Dat?

Dat is a open data project designed to make data more accessible:

* Track incremental changes made in datasets
* Provide a REST api to share your data
* Designed to work with all data: big and small

Read the [docs](https://github.com/maxogden/dat) to learn more about Dat.

## Installation

  1. Install pip

  2. Obtain the Python DAT package

    `pip install datpy`

## Usage

This is a new library and it needs work! Please don't hesitate to send a pull request or to open an issue if you find something wrong or broken. It's probably because we messed up!

Here's a simple example of how to read a dat's data into a pandas object, and then update the dat accordingly after editing the values.

```python
from datpy import DatAPI

dat = DatAPI('http://localhost:6461')

df = dat.to_pandas()

# ... do some stuff to the pandas dataframe ...

dat.put_pandas(df)


```

[An ipython notebook example for dat](http://nbviewer.ipython.org/github/pkafei/Dat-Python/blob/master/examples/Using%20Python%20with%20Dat.ipynb) (outdated)

## API

#### DatAPI

`DatAPI` is a class that binds to a remote Dat via the http API. This is suitable for datasets that fit in memory.

For very large datasets and for code in production, please refer to the [dat commandline documentation](https://github.com/maxogden/dat/blob/master/docs/cli-usage.md) for stable and memory-safe interaction.

 ```python
 from datPython import DatAPI

 dat = DatAPI('http://imadat.myorganization.org')
 ```

 and with credentials:
 ```python

 # if the dat object already exists:
 dat.auth('admin', 'mypassword')

 # alternatively, in the constructor:
 dat = DatAPI('http://imadat.myorganization.org', username='admin', password='mypassword')
 ```

#### DatAPI#info()

 Return info about dat instance

 ```python
 > dat.info()
 {
  dat: "Hello",
  version: "6.9.4",
  changes: 49,
  name: "dat-test",
  description: "i am a description",
  publisher: "karissa",
  rows: 44,
  approximateSize: {
    rows: "5.93 kB"
  }
}
```

#### DatAPI#changes(opts=None)

 Return the rows that have been changed

 ```python
 > dat.changes()
[
  {
    change: 1,
    key: "schema",
    from: 0,
    to: 1,
    subset: "internal"
  },
  {
    change: 2,
    key: "ci4etk0wq0000tjxmj7ii2wx6",
    from: 0,
    to: 1
  },
  etc...
]
 ```

#### DatAPI#to_json(opts=None)

  alias: **DatAPI#rows(opts=None)**

  Get the rows in the dat. This returns a list of dictionaries, where each dictionary is the json representation of that row.

  ```python
> dat.to_json()
[
 {'key': 'ci4b027gv0001hyxm1oewmppr',
  'version': 1,
  'vote_share': 51.33,
  'state': 'CA',
  'republican': True},
 {'key': 'ci4b027fq0000hyxm4919va4t',
  'version': 2,
  'vote_share': 49.53,
  'state': 'DE',
  'republican': False},
  ...
]
  ```

  You can pass in any options supported by Dat's [REST api](https://github.com/maxogden/dat/blob/master/docs/rest-api.md)

  For example, ```opts={'limit': 1}``` expands to ```http://<host>/api/rows?limit=1
  ```python
> dat.to_json(opts={"limit": 1})
[
 {'key': 'ci4b027gv0001hyxm1oewmppr',
  'version': 1,
  'vote_share': 51.33,
  'state': 'CA',
  'republican': True},
]
  ```

#### DatAPI#to_csv()
Returns the data store in csv format.

```python
> dat.to_csv()
'vote_share,wee,woo,key,version\n51.33,,,1,1\n,foo,,ci4b027fq0000hyxm4919va4t,1\n,foo,,ci4b027gv0001hyxm1oewmppr,1\n,foo,,ci4b027ho0002hyxm41wpaje6,1\n,,boop,ci4b027hw0003hyxme100j1kt,1\n,foo,,ci4b03qh00004hyxmlfddel23,1\n,foo,,ci4b03qhn0005hyxm2893j8ty,1\n,foo,,ci4b03qhz0006hyxmewff'
```


#### DatAPI#to_file(fp, format='csv')
Write the data from your dat directly to a file.

`format`: 'json' or 'csv'

```python
> fp = open('path/to/file.csv', 'wb')
> dat.to_file(fp, format='csv')
> fp.close()
```

#### DatAPI#to_pandas()
Returns the data store into a pandas dataframe

```python
> df = dat.to_pandas()
> df.shape
(770, 13)
> df['columnName'].describe()
etc...
```

#### DatAPI#put_pandas(dataframe)

Sends a dataframe to a dat using bulk ndjson. This is still experimental.

`dataframe`: pandas.core.frame.DataFrame


```python
> df = dat.to_pandas()

# clean a column
> df['columnName'] = clean_up_column(df['columnName'])

# add a column
> df['anotherColumn'] = pd.Series([1, 2, 3, 4])

> dat.put_pandas(df)

```

You will then see the changes reflected. All of the affected rows will be bumped to the next version.

#### DatAPI#api(resource, method, data=None, opts=None, stream=False)

**Parameters**

`resource`: string

  the api resource to access. (e.g. 'rows', 'csv', 'session')

`method`: string

  the http method to use. (e.g., 'GET', 'PUT')

`data`: object (optional)

  arguments to be sent into raw body data (e.g., on post)

`opts`: object (optional)

  arguments to be entered into query parameters

`stream`: boolean (optional, default False)

  whether to stream the response

````python

> dat.api('csv', 'GET')
'vote_share,wee,woo,key,version\n51.33,,,1,1\n,foo,,ci4b027fq0000hyxm4919va4t,1\n,foo,,ci4b027gv0001hyxm1oewmppr,1\n,foo,,ci4b027ho0002hyxm41wpaje6,1\n,,boop,ci4b027hw0003hyxme100j1kt,1\n,foo,,ci4b03qh00004hyxmlfddel23,1\n,foo,,ci4b03qhn0005hyxm2893j8ty,1\n,foo,,ci4b03qhz0006hyxmewff'

```


#### DatAPI#json(resource, method, data=None, opts=None, stream=False)
Call the api and return the results as json.
```python
> dat.json('session', 'GET')
{'loggedOut': True}


> data = {
  "vote_share": 49.59,
  "republican": False
}
> dat.json('rows', 'POST', data=json.dumps(data), opts={"format": "json"})
 {'key': 'ci4b027fq0000hyxm4919va4t',
  'version': 2,
  'vote_share': 49.53,
  'state': 'DE',
  'republican': False},


```
### DatAPI.auth(username, password)

For Authentication, you'll need the username and password that exists on the dat server. Right now, dat uses basic auth as the authentication scheme.

 ```python

 # if the dat object already exists:
 dat.auth('admin', 'mypassword')

 # alternatively, in the constructor:
 dat = DatAPI('http://imadat.myorganization.org', username='admin', password='mypassword')
 ```

 [If you forgot your password, here's some help.](https://github.com/maxogden/dat/blob/master/docs/forgot-password.md)

# Developers

This is a new library and it needs work! Please don't hesitate to send a pull request.

## Contributing

First, create a fork, then install the requirements. Make your change and open a pull request!

```bash
$ git clone http://github.com/<your-fork>/Dat-Python
$ pip install -r requirements.txt
$ git commit -am "BUG: there was a bug that had this problem"
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
python test.py
```


# BSD Licensed

Copyright (c) 2014 Karissa McKelvey and contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
