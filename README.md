# ozone

## Installation

Requires Python3 and Google Chrome.

`pip3 install -r requirements.txt`

If you want to use keyring on Linux, I recommend installing this first. For details, read [here](https://github.com/jaraco/keyring).

`sudo apt install python-dbus`

## Configuration

Write your configuration options to record.py or enter as the command line option.

For password, I recommend using [keyring](https://github.com/jaraco/keyring) so you won't have to enter each time.
Use this command to set.

`keyring set https://login.microsoftonline.com your-mail`

## Example command

To Enter man-power time:
`python3 record.py -e 'mail' -m '2021/05' -p 'project' -u 'https://example.com/man-power' -P`

To punch in:
`python3 punch.py -t 'in' -e 'mail' -u 'https://example.com' -H`
