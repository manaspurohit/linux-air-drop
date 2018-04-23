# linux-air-drop
Wireless file transfer between Linux computers

Created by Tina Lee, Sam Lazarus, and Manas Purohit

## Lookup Server

The lookup server used is implemented as a node server. The source for that
can be found here: https://github.com/sl/airdrop-lookup-server

Additionally, we have a Heroku hosted version of the lookup server running at
https://airdrop-lookup.herokuapp.com. Note to TAs: if it happens to be down,
and you'd like to take use it while grading (the client and server programs
used for file transfer both use this hosted version), contact Sam Lazarus on
neu mail, and he can put it back up for you. That said, it's probably still up.

## Installation

To install, simply run `pip install -r requirements.txt` or
`pip3 install -r requirements.txt` (if you have a different binary for pip
on python three) And run the server and client software.
