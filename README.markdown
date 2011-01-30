tbclient
==========

Overview
----------
tbclient is a command line client for REST service on top of Marcuscom Tinderbox.

Installation
------------

First you need to ensure you have everything needed installed:

 * Python 2.6+ (not sure if works on earlier versions)

Installation is pretty simple, just execute:

	sudo python setup.py install

Configuration
-------------

Create a configuration file ~/.trc:

	[default]
	apihost = tindy.my
	username = username
	passwd = userpass

Set reasonable permissions on it:

	chmod 600 ~/.trc

And now you should be ready.

Usage
-----

### Listing Builds

$ tbc build
 id           name     status   current port updated
  1    8.x-FreeBSD       IDLE           None 2011-01-30 14:05:25
$

### Getting Build Details

To get details of a build with id '1' use:

	$ tbc build 1
	name: 8.x-FreeBSD
	description: 8.x with FreeBSD ports tree.
	status: IDLE
	updated: 2011-01-30 14:05:25
	currentport: None
	remake count: 0
	jail id: 1
	portstree_id: 1
	    
	$

### Listing Queue Entries

	$ tbc queue
	 id   username                 port        build pri     status            enqueued           completed
	 10      novel      security/gnutls  8.x-FreeBSD  10    SUCCESS 2011-01-30 13:54:43 2011-01-30 14:05:27
	$

### Adding Queue Entry

	$ tbc queue add -b 1 -p 5 editors/vim

Where *1* is id of a build and *5* is a priority.

Support
-------
Feel free to drop a mail to novel@FreeBSD.org if you have any feedback.
