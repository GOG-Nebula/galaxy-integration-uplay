import os
from definitions import System, SYSTEM
import re
import requests
UBISOFT_REGISTRY = "SOFTWARE\\Ubisoft"
STEAM_REGISTRY = "Software\\Valve\\Steam"
UBISOFT_REGISTRY_LAUNCHER = "SOFTWARE\\Ubisoft\\Launcher"
UBISOFT_REGISTRY_LAUNCHER_INSTALLS = "SOFTWARE\\Ubisoft\\Launcher\\Installs"

if SYSTEM == System.WINDOWS:
    UBISOFT_SETTINGS_YAML = os.path.join(os.getenv('LOCALAPPDATA'), 'Ubisoft Game Launcher', 'settings.yml')

UBISOFT_CONFIGURATIONS_BLACKLISTED_NAMES = ["gamename", "l1", '', 'ubisoft game', 'name']

CHROME_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
ids_url = 'https://ubisoftconnect.com/invalid'
ids_response = requests.get(ids_url)
regex_ids_response = re.findall('APP_ID.{0,40}|GENOME_ID.{0,40}', ids_response.text) 

ids_result = []
for sub in regex_ids_response:
    sub = sub.replace('"','')
    if ':' in sub:
        ids_result.append(map(str.strip, sub.split(':', 1)))

ids_result = dict(ids_result)

CLUB_APPID = ids_result.get('APP_ID','')
CLUB_GENOME_ID = ids_result.get('GENOME_ID','')

AUTH_PARAMS = {
    "window_title": "Login | Ubisoft WebAuth",
    "window_width": 460,
    "window_height": 690,
    "start_uri": f"https://connect.ubisoft.com/login?appId={CLUB_APPID}&genomeId={CLUB_GENOME_ID}&lang=en-US&nextUrl=https:%2F%2Fconnect.ubisoft.com%2Fready",
    "end_uri_regex": r".*rememberMeTicket.*"
}

def regex_pattern(regex):
    return ".*" + re.escape(regex) + ".*"


AUTH_JS = {regex_pattern(r"connect.ubisoft.com/ready"): [
            r'''
            window.location.replace("https://connect.ubisoft.com/change_domain/"); 

            '''
        ],
            regex_pattern(r"connect.ubisoft.com/change_domain"): [
            r'''
            window.location.replace(localStorage.getItem("PRODloginData") +","+ localStorage.getItem("PRODrememberMe") +"," + localStorage.getItem("PRODlastProfile"));

            '''
        ]}

