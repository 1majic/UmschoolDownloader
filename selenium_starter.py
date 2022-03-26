import json
import os
import pickle

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

config = {}
with open('Config.txt') as cfg:
    cfg = cfg.read().split('\n')
    for i in cfg:
        name = i.split('=')
        config[name[0]] = name[1]

config["savefile.default_directory"] = fr"{os.getcwd()}\files"


def StartUrlDriver(url, proxy=None):
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.135 "
        "Safari/537.36")
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
             "profile.default_content_settings.popups": 0,
             "savefile.default_directory": config["savefile.default_directory"],
             "directory_upgrade": True,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "plugins.always_open_pdf_externally": True,
             "download.default_directory": config["savefile.default_directory"]
             }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--kiosk-printing')
    options.add_argument("--disable-logging");
    # options.headless = True
    # options.binary_location = '/app/.apt/usr/bin/google-chrome'
    # chromedriver = '/app/.chromedriver/bin/chromedriver'
    options.binary_location = fr"{config['chrome.directory']}"
    chromedriver = 'drivers/98.exe'
    os.environ["webdriver.chrome.driver"] = chromedriver
    options.add_argument("--disable-dev-shm-usage");
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    if proxy:
        options.add_extension(proxy)
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
    driver.get(url)
    return driver