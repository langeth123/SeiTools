# SeiTools

# Features

- **Получение Faucet из офф крана**

- **Установка и подтверждения твиттера на BlueMove (сэкономит время кто минтит нфт)**

### Settings

Смотри config.py file

~~~python
THREAD_RUNNER_SLEEP = 1 # отвечает за задержкой между стартом потоков

~~~

Чтобы начать работу:
 - Загрузи аккаунты в формате: address:discord_token:proxy в файлик data.txt (папка data)
   / Прокси в формате: login:pass@ip:port (http). Если прокси не используете, то можно вставить: address:discord_token

По поводу прокси. Их в целом можно и не загружать (просто файлик оставить пустым). Но осторожней, дебанк любит рейтлимитать за большое кол-во запросов / плохие прокси

### How to run script
1. Устанавливаем Python: https://www.python.org/downloads/, я использую версию 3.9.8
2. При установке ставим галочку на PATH при установке

>![ScreenShot](https://img2.teletype.in/files/19/03/19032fbe-1912-4bf4-aed6-0f304c9bf12e.png)

3. После установки скачиваем бота, переносим все файлы в одну папку (создаете сами, в названии и пути к папке не должно быть кириллицы и пробелов)
4. Запускаем консоль (win+r -> cmd)
5. Пишем в консоль:
cd /d Директория
* Директория - путь к папке, где лежит скрипт (само название скрипта писать не нужно)
6. Прописываем:
pip install -r requirements.txt
7. После установки всех библиотек командой выше, запускаем софт:
python main.py

Скрипт запустился.
