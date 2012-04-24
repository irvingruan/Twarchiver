Twarchiver
=====

**Simple tweet archiver**

Written by Irving Y. Ruan — [irvingruan@gmail.com](irvingruan@gmail.com)

## About

Twarchiver is a simple archiver utility that will fetch (up to 3,200) statuses of a user and generate a plaintext-style HTML overview of your tweets, their timestamps, and the permalinks to them. 

Twitter sets 3,200 statuses as the limit due to performance issues. See their [user timeline API rules](https://dev.twitter.com/docs/api/1/get/statuses/user_timeline) for more details.

## Requirements

Twarchiver works on *nix based systems and requires Python >= 2.4.

## Usage

To run:

`$ ./Twarchiver.py <username>`

And Twarchiver will generate a HTML-formatted file of your tweets on your Desktop with the naming scheme '<%username>.html'.

## Legal

Twarchiver is Copyright (c) 2012 Irving Ruan and BSD licensed. The full text of the license can be found in LICENSE.