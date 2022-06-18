## Browser in the Browser exploit

Thanks to the work of mrd0x for making this possible

https://github.com/mrd0x/BITB

Command line generation browser in the browser exploit framework

Simply choose a target url

The script will create and host the generated phishing site at default 127.0.0.1:8000

![alt text](screenshots/gif.gif?raw=true)

captured credentials can be found in credentials.txt in the root folder.

## Usage

`git clone http://github.com/warren2i/bitb`

`pip install requirements.txt`

`python main.py -u <url>`



**ToDo**

this needs to be the correct resolution... How to find targets native resolution? perhaps capture in several aspect ratio, use js to detect?

sometimes this favicon.ico standard is not followed, perhaps if not found search html for .ico file and use instead?

~~fetch logo for login page~~