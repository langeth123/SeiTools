from config import *

DISCORD_AUTH_URL = "https://discord.com/api/v9/oauth2/authorize"
FAUCET_URL       = "https://faucet-v3.seinetwork.io/"

class Faucet:
    def __init__(self, address: str, token: str, proxies: dict = None, tryings=5) -> None:
        self.address = address
        self.token   = token
        self.session = requests.Session()
        self.tryings = tryings

        self.discord_auth_token = None

        if proxies:
            self.session.proxies.update(proxies)
    
    def send_request(self, method: str, url: str, **kwargs):
        for _ in range(self.tryings):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    **kwargs
                )
                status = response.status_code

                if status == 200:
                    return response.json()
                else:
                    if status in [401] and url == DISCORD_AUTH_URL:
                        return response.json()
                    
                    else:
                        logger.error(f'[{self.address}] Bad status code: {status}')
                        sleep(5)

            except Exception as error:
                logger.error(f'[{self.address}] Failed to do req for: {url} | {error}')
                sleep(5)

    def login_with_discord(self) -> None:
        kwargs = {
            "headers": {
                "authorization" : self.token
            },
            "params": {
                'client_id'     : '1090401271028142140',
                'response_type' : 'code',
                'redirect_uri'  : 'https://app.sei.io/faucet',
                'scope'         : 'identify guilds.members.read'
            },
            "json": {
                'permissions'   : '0',
                'authorize'     : True
            }
        }
        response = self.send_request("post", DISCORD_AUTH_URL, **kwargs)
        if response is None:
            raise MaxTryingsExceed()
        
        else:
            if "location" in response.keys():
                logger.success(f'[{self.address}] Made login with discord')

                token = response["location"].split("code=")[1]
                self.discord_auth_token = token # stoken for changid data on faucet site

            elif "401: Unauthorized" in response.values():
                raise BadDiscordToken(self.token)
    

    def exchange_code(self):
        json_data = {
            "discordCode": self.discord_auth_token
        }
        response = self.send_request("post", FAUCET_URL + "exchange-code", json=json_data)

        if response is False:
            logger.error(f'[{self.address}] Failed to exhange code (unknown error)')
            raise Exception("Failed to exhange code from sei site")
        else:
            if "verifiedAccessToken" in response.keys():
                logger.info(f'[{self.address}] Got code for faucet')
                self.faucet_token = response.get("verifiedAccessToken")
            else:
                raise Exception("verifiedAccessToken not at response")
            
    def request_faucet(self):
        json = {
            'address': self.address,
            'discordAccessToken': self.faucet_token,
        }

        response = self.send_request("post", FAUCET_URL + "atlantic-2", json=json)
        if response is False:
            logger.error(f'[{self.address}] Failed to request tokens from site')
            raise Exception("Failed to request tokens from site")
        else:
            if response.get("status") == 'fail':
                logger.error(f'[{self.address}] Failed to request faucet: {response["message"]}')

            elif response.get("status") == 'success':
                message_id = response["data"].get("messageId")
                logger.success(f'[{self.address}] Request faucet successfully. ID: {message_id}')