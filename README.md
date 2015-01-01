# DAT Python API

This is a REST api client in python for [Dat](https://dat-data.com).

## What is Dat?

Dat is a open data project designed to make data more accessible:

* Track incremental changes made in datasets
* Designed to work with big data
* Streaming feature to provide

Read the [docs](https://github.com/maxogden/dat) to learn more about Dat.

## Instructions

  1. Install pip

  2. Obtain the Python DAT package

    `pip install datPython`

  3. Import Dat

    `from datPython import Dat`

  4. Set dat to the connection that you are listening to

    `dat = Dat('http://localhost:6461')`

## API


#### Dat#info

 Return info about dat instance

 `dat.info()`

#### Dat#changes

 Return the rows that have been changed

 `dat.changes()`

#### Dat#rows

  Get the rows in the dat. This returns a list of dictionaries, where each dictionary is the json representation of that row.

  ```python
> dat.rows()
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

#### Dat#csv
Returns the data store in csv format

```python
> dat.csv()
'vote_share,wee,woo,key,version\n51.33,,,1,1\n,foo,,ci4b027fq0000hyxm4919va4t,1\n,foo,,ci4b027gv0001hyxm1oewmppr,1\n,foo,,ci4b027ho0002hyxm41wpaje6,1\n,,boop,ci4b027hw0003hyxme100j1kt,1\n,foo,,ci4b03qh00004hyxmlfddel23,1\n,foo,,ci4b03qhn0005hyxm2893j8ty,1\n,foo,,ci4b03qhz0006hyxmewff'
```

#### Dat#import(filename, type='json')
Import data into the dat

`dat.import('example.json', 'json')`
`dat.import('example.csv', 'csv')`

Python in Dat Example: http://nbviewer.ipython.org/github/pkafei/Dat-Python/blob/master/examples/Using%20Python%20with%20Dat.ipynb


#### Dat#api(resource, method, data=None, opts=None, stream=False)
Call the api.

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

#### Dat#json
```

#### Dat#json
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

# BSD Licensed

Copyright (c) 2014 Portia Burton and contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
