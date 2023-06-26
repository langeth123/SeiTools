from config import *

BLUEMOVE_URL = "https://sei-api-testnet.bluemove.net/api/"

class BlueMove:
    def __init__(self, address: str, proxies: dict = None, tryings=5) -> None:
        self.address = address
        self.session = requests.Session()
        self.tryings = tryings

        if proxies:
            self.session.proxies.update(proxies)
    
    def send_request(self, method: str, url: str, **kwargs):
        for _ in range(self.tryings):
            try:
                kwargs["timeout"] = 10
                response = self.session.request(
                    method=method,
                    url=url,
                    **kwargs
                )
                status = response.status_code

                if status == 200:
                    return response.json()
                else:
                    logger.error(f'[{self.address}] Bad status code: {status}')
                    sleep(5)

            except Exception as error:
                logger.error(f'[{self.address}] Failed to do req for: {url} | {error}')
                sleep(5)
    
    def login(self):
        json_data = {
            'walletAddress': self.address,
            'deviceToken': None
        }
        response = self.send_request("post", BLUEMOVE_URL + "auth-signature/login", json=json_data)
        if response is False:
            raise Exception("failed to login to bluemove")
        else:
            if "jwt" in response.keys():
                self.jwt_token = response.get("jwt")
                logger.success(f'[{self.address}] Made login to bluemove')
    
    def set_twitter(self):
        kwargs = {
            "json": {
                "twitterScreenName": ''.join(random.choices(string.ascii_lowercase, k=random.randint(7, 15)))
            },
            "headers": {
                "authorization": "Bearer " + self.jwt_token
            }
        }
        response = self.send_request("post", BLUEMOVE_URL + "users/check-follow-twitter", **kwargs)
        if response is False:
            raise Exception("failed to check twitter")
        else:
            if "data" in response.keys():
                if response["data"]["is_follow_twitter"]:
                    logger.success(f'[{self.address}] Twitter was setted!')
        