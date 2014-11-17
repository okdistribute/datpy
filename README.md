# DAT Python API

## What is Dat?

Dat is a open data project designed to make data more data more accessible:

* Track incremental changes made in datasets
* Designed to work with big data
* streaming feature to provide faster access to datasets 

Read the [docs](https://github.com/maxogden/dat/blob/master/docs/what-is-dat.md) to learn about Dat.

## Instructions

1. To get access to the Pythn Dat API run 
`pip install dat`

2. Create a dat using  using `dat init` and to listen to your dat run `dat listen`

3. Import Dat 'from Dat import Dat' and set dat to the connection that you are listening to `dat = Dat('http://localhost:6461')`


## DAT GET
The GET API allows user to access dat data store and it's attributes.


### DAT Info
`dat.info` Provides info about dat instance
```
{"dat":"Hello","version":"6.8.4","changes":702,"name":"bionode","rows":701,"approximateSize":{"rows":"136.76 kB"}}
```

### DAT Diff
`dat diff` displays the rows that have been changed
```
{"change":1,"key":"schema","from":0,"to":1,"subset":"internal"}
{"change":2,"key":"ci1fj4cqd00004buy9jabbyz0","from":0,"to":1}
{"change":3,"key":"ci1fj4cqf00014buyoa2m4ad2","from":0,"to":1}
{"change":4,"key":"ci1fj4cqg00024buyfkbap6h2","from":0,"to":1}
{"change":5,"key":"ci1fj4cqg00034buysgolrtcr","from":0,"to":1}
{"change":6,"key":"ci1fj4cqg00044buyn9w7cc2n","from":0,"to":1}
{"change":7,"key":"ci1fj4cqi00054buyzmivu7j7","from":0,"to":1}
{"change":8,"key":"ci1fj4cqj00064buyvwbnvn3k","from":0,"to":1}
```






Future Goals:
* [Pandas I/O API](http://pandas.pydata.org/pandas-docs/stable/io.html)

* [Dat and Ipython](http://ipython.org/)

Looking to make using Dat and Python seamless as possible for developers. If you have any suggestions or any use cases for Dat and Python, please comment.