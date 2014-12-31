# DAT Python API

## What is Dat?

Dat is a open data project designed to make data more accessible:

* Track incremental changes made in datasets
* Designed to work with big data
* streaming feature to provide faster access to datasets

Read the [docs](https://github.com/maxogden/dat/blob/master/docs/what-is-dat.md) to learn more about Dat.

## Instructions

  1. Install pip

  2. Obtain the Python DAT package

    `pip install datPython`

  3. Import Dat

    `from datPython import Dat`

  4. Set dat to the connection that you are listening to

    `dat = Dat('http://localhost:6461')`

## DAT Info
 Return info about dat instance

 `dat.info()`

### DAT Diff
 Return the rows that have been changed
 
 `dat.diff()`

## DAT GET Rows
Return the dat data store

`dat.rows()` 

## DAT GET CSV
Returns data store in csv format

`dat.csv()`

## DAT GET Python Dictionary
Returns data store in dictionary format

`dat.dict()`

## Dat POST JSON
Post JSON to dat instance

`dat.post_json('example.json')`

## Dat POST CSV
Post CSV to dat instance

`dat.post_csv('example.csv')`

Python in Dat Example: http://nbviewer.ipython.org/github/pkafei/Dat-Python/blob/master/examples/Using%20Python%20with%20Dat.ipynb

### BSD Licensed

Copyright (c) 2014 Portia Burton and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.