from config import *
from Modules.Faucet import *
from Modules.BlueMove import *


def account_handler(account_data: dict):
    if len(account_data.keys()) == 2:
        account = Faucet(account_data["address"], account_data["token"])

    elif len(account_data.keys()) == 3:
        account = Faucet(
            account_data["address"], 
            account_data["token"], 
            account_data["proxies"]
        )
    try:
        account.login_with_discord()
        logger.info(f'[{account_data["address"]}] got discord token: {account.discord_auth_token}')
        """
        discord token required for faucet
        """

    except BadDiscordToken:
        logger.error(f'[{account_data["address"]}] Bad discord token. May it dead..')
        return
    
    try:
        account.exchange_code()
    except Exception as error:
        logger.error(f'[{account_data["address"]}] Error: {error}')
        return
    
    try:
        account.request_faucet()
    except Exception as error:
        logger.error(f'[{account_data["address"]}] Error: {error}')

def bluemove_handler(account_data: dict):
    if len(account_data.keys()) == 2:
        account = BlueMove(account_data["address"])

    elif len(account_data.keys()) == 3:
        account = BlueMove(
            account_data["address"], 
            account_data["proxies"]
        )
    
    try:
        account.login()
    except Exception as error:
        logger.error(f'[{account_data["address"]}] Failed to login: {error}')
    
    try:
        account.set_twitter()
    except Exception as error:
        logger.error(f'[{account_data["address"]}] Failed to set twitter: {error}')
    

def main(task):
    threads = []
    for i in ACCOUNTS:
        threads.append(Thread(
            target=task,
            args=(i,)
        ))
    
    for k in threads:
        k.start()
        sleep(THREAD_RUNNER_SLEEP)
    
    for j in threads:
        j.join()

def get_action() -> str:
    theme = {
        "Question": {
            "brackets_color": "bright_yellow"
        },
        "List": {
            "selection_color": "bright_blue"
        }
    }

    question = [
        inquirer.List(
            "action",
            message=colored("Выберите действие", 'light_yellow'),
            choices=["Get Faucet", "Approve Bluemove", "Both", "exit"],
        )
    ]
    action = inquirer.prompt(question, theme=loadth(theme))['action']
    return action


if __name__ == '__main__':
    while True:
        try:
            action = get_action()
            if action == "Get Faucet":
                main(account_handler)
            elif action == "Approve Bluemove":
                main(bluemove_handler)
            elif action == "Both":
                main(account_handler)
                main(bluemove_handler)
            elif action == "exit":
                input("press any key to exit")
                break
        except Exception as error:
            logger.error(f'Fatal error: {error}')