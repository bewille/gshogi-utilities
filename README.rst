Utilities for gshogi:

Gshogi is a program to play Shogi - japanese chess.
It was created by John Cheetham: see http://johncheetham.com/projects/gshogi/index.html

I found it is a nice graphical representation and is very useful to play agains engines and learn to play Shogi by using games and literature from the internet.

I publish here some routines which I found useful. They do some translations tasks and are just what I managed to piece together for private purposes. They are by no means error free and you may still have to edit the resulting files by hand in some cases. Unfortunately there is no standardisation in psn-files so many authors use them as a kind of symbolic notation. These programs create a format which is readable by gshogi.

These programs need Python3 and the tkinter-package.

Installation
------------
Python 3 is required. If you are using a system that uses python 2 as default
(do python -V to check) then you need to use python3 for commands and package
names. For example the package name will be python3-cairo instead of
python-cairo and the build command will be python3 setup.py build.


You need to install these packages first:

    gcc python python-devel python-cairo python-gobject gtk3



psn2psn reads a lot of psn-files and tries to put them in a format which can be read by gshogi.

The package PosX.pyw3 needs the python package pyperclip and xclip on Linux.
Copy the ASCII-Representation of a shogi-position and press the button of the program:
under Edit-> paste position you can now paste the posititon to gshogi
- comes in handy sometimes when replaying positions from publications
- doesn't work in all cases since there are a bunch of ways to represent shogi-boards this way. Works e.g. for "Quest of the lost systems" http://www.shogi.net/quest/

USL-translator will translate files e.g. from the Shogi-Maze website http://shogimaze.free.fr - actually from BCM-Games USL-format. If you are running Linux there is no way to run BCM-games under wine to my knowledge so this may be useful.

Kifu-translator will translate games in kif-format. Handy to pick recent games from japanese websites.

Bernd Wille, May 2017