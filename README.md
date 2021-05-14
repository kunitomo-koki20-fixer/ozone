# ozone

## Installation
Requires Python3 and Google Chrome.

`pip3 install -r requirements.txt`

If you want to use keyring on Linux, I recommend installing this first. For details, read [here](https://github.com/jaraco/keyring).

`sudo apt install python-dbus`

## configuration

Write your configuration options to record.py or enter as the command line option.

For password, I recommend using [keyring](https://github.com/jaraco/keyring) so you won't have to enter each time.
Use this command to set.
`keyring set https://login.microsoftonline.com your-mail`
