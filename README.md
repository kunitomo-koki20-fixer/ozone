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

`record.py -e 'mail' -m '2021/05' -p 'project' -u 'https://example.com' -P`

## Register Alias

Copy & Paste below commands to your ~/.bashrc, ~/.zshrc or etc..

```bash
alias ozone-attend="python3 ~/{folder path to this project}/ozone/attend.py -e {your email} -u '{attendance url}'"
alias ozone-leave="python3 ~/{folder path to this project}/ozone/leave.py -e {your email} -u '{attendance url}'"

function ozone-record(){
while getopts m:p: OPT
do
    case $OPT in
        p) month=$OPTARG;;
        m) project=$OPTARG;;
    esac
done
python3 ~/{folder path to this project}/ozone/record.py -e {your email} -m $month -p $project -u '{manpower management url}'
}
```
