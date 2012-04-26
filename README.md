Twarchiver
=====

**Simple tweet archiving utility**

Written by Irving Y. Ruan — [irvingruan@gmail.com](irvingruan@gmail.com)

## About

Twarchiver is a simple archiving utility that will fetch (up to 3,200) statuses for a user and generate a plaintext-style HTML overview of your tweets, their timestamps, and the permalinks, if available, to them. 

Twitter sets 3,200 statuses as the limit due to performance issues. See their [user timeline API rules](https://dev.twitter.com/docs/api/1/get/statuses/user_timeline) for details.

## Requirements

The python package, simplejson, is needed for Twitter's API. You can either download the [tarball](http://pypi.python.org/packages/source/s/simplejson/simplejson-2.5.0.tar.gz#md5=3160556224e3e0cd9605c101eb0de3b9) and install it using:

`$ python setup.py install`

Or get it using pip via:

`$ pip install simplejson`


Twarchiver works on *nix based systems and requires Python >= 2.4.

## Usage

To run:

`$ ./Twarchiver.py <username>`

And Twarchiver will generate a HTML-formatted file of your tweets on your Desktop with the naming scheme '<%username>.html'.

## Legal

Twarchiver is Copyright (c) 2012 Irving Ruan and MIT licensed. The full text of the license can be found in LICENSE.