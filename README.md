BurningButt
===========

Information Security Project

===========

Current version is aimed at opening files
encrypted with gpg utility.

To make such a file you need:

$ gpg -o secure.gpg --symmetric --cipher-algo AES256 server.c

Note that this runs under python2.7 and you have to install
PyQt4 and pexpect module.
