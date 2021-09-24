# TeleController - Controll your PC using telegram bots





## Requirements 

this project uses below libraries :
* __python-telegram-bot__
* __pyscreenshot__
* __pyautogui__
* __pyttsx3__

Install requirements using pip :
``` pip install -r requirements.txt```

## BEFORE USING
at first we should create a telegram bot using @BotFather in telegram  and get our bot token . server needs this token to work .
## USAGE
result of ```python3 server.py --help ```:

> usage: server.py [options]
> 
> controll your system securely from telegram bots
> 
> optional arguments:   -h, --help            show this help message and
> exit   -T TOKEN, --token TOKEN
>                         Token of your telegram Bot   -P PASSWORD, --password PASSWORD
>                         Password For your Bot !   -p IP:PORT, --proxy IP:PORT
>                         use a socks5 proxy
> 
> Enjoy it :)

if telegram is censored in your country , you can use from -p or --proxy option . by this option you can use a socks5 proxy (like TOR service) for server traffic .

for example we can run server using :
```python3 server.py -p 127.0.0.1:9150 --token <TOKEN> --password <PASSWORD>```

also for security issues , you can run server script without --token and --password options . in this case , script asks TOKEN and PASSWORD from you :
> ```python3 server.py -p 127.0.0.1:9150```

after run the server , we can go to our telegram bot and controll our pc using bot's Reply Keyboard markup . of course when we start the bot , we should enter the password that we passed to server script .

# TODO

- [ ] Project can run on linux
- [ ] Clean up code
- [ ] More Security


