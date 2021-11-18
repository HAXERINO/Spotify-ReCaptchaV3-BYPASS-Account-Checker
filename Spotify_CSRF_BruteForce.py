import re, crayons, requests

def GetCaptchaToken():  
    HeaderRecaptchaA =  {
                            "Accept": "*/*",
                            "Pragma": "no-cache",
                            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0)'
                        }
    CaptchaGetData = requests.get("https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39&co=aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbTo0NDM.&hl=en&v=_7Co1fh8iT2hcjvquYJ_3zSP&size=invisible&cb=l9c4tmvbpzv2", headers=HeaderRecaptchaA)
    TokenA = "".join(re.findall("type=\"hidden\" id=\"recaptcha-token\" value=\"(.*?)\"", str(CaptchaGetData.text)))
    
    HeaderRecaptchaB =    {
                                "Accept": "*/*",
                                "accept-encoding": "gzip, deflate, br",
                                "accept-language": "fa,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                                "content-length": "5628",
                                "origin": "https://www.google.com",
                                "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0)',
                                "Pragma": "no-cache",
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "referer": "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39&co=aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbTo0NDM.&hl=en&v=_7Co1fh8iT2hcjvquYJ_3zSP&size=invisible&cb=l9c4tmvbpzv2"
                            }
    DataPayload =   {
                        "v": "_7Co1fh8iT2hcjvquYJ_3zSP",
                        "reason": "q",
                        "c": TokenA,
                        "k": "6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39",
                        "co": "aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbTo0NDM.",
                        "size": "invisible",
                        "cb": "l9c4tmvbpzv2",
                        "hl": "en"
                    }
    TokenB = requests.post("https://www.google.com/recaptcha/enterprise/reload?k=6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39",headers=HeaderRecaptchaB, data=DataPayload)
    captchaToken = "".join(re.findall("\[\"rresp\",\"(.*?)\"", str(TokenB.text)))
    return captchaToken

def InitiateLOGIN(Email,Password):
    InitiateGetURI = "https://accounts.spotify.com/en/login?continue=https:%2F%2Fwww.spotify.com%2Fus%2Faccount%2Foverview%2F"
    DataA = requests.get(InitiateGetURI).cookies.get_dict()
    CSRFToken = DataA['sp_sso_csrf_token']
    SecureTPASESSION = DataA['__Secure-TPASESSION']
    HostSPCSRFSiD = DataA['__Host-sp_csrf_sid']
    HostDeviceID = DataA['__Host-device_id']
    SpTR = DataA['sp_tr']
    CaptchaToken = GetCaptchaToken()
    print(crayons.yellow(f'ReCaptchaV3 Token Captured:\n{CaptchaToken}\n'))
    PostURI = "https://accounts.spotify.com:443/login/password"
    PostCookies =   {
                        "__Host-device_id": str(HostDeviceID),
                        "__Secure-TPASESSION": str(SecureTPASESSION),
                        "sp_sso_csrf_token": str(CSRFToken),
                        "sp_tr": str(SpTR),
                        "__Host-sp_csrf_sid": str(HostSPCSRFSiD),
                        "__bon": "MHwwfDYzMTA5NzUwM3wyNjUwNjA5NTEyNnwxfDF8MXwx",
                        "remember": str(Email)
                    }
    PostHeaders =   {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-Csrf-Token": str(CSRFToken),
                        "Origin": "https://accounts.spotify.com",
                        "Dnt": "1",
                        "Referer": "https://accounts.spotify.com/en/login",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "Te": "trailers"
                    }
    PostData =      {
                        "remember": "true",
                        "continue": "https://accounts.spotify.com/en/status",
                        "username": str(Email),
                        "password": str(Password),
                        "recaptchaToken": str(CaptchaToken)
                    }
    print(crayons.blue(f'Final Result: {requests.post(PostURI, headers=PostHeaders, cookies=PostCookies, data=PostData).text}'))
def main():
    InitiateLOGIN('EMAIL_HERE','PASSWORD_HERE')
if __name__ == "__main__":
    main()
