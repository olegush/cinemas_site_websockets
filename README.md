# Cinemas Site
The script displays movies on show in Saint Petersburg cinemas with KinoPoisk and IMDB ratings. Movies schedule parses from [kinoafisha.info](https://kinoafisha.info). Based on [Trio WebSocket](https://trio-websocket.readthedocs.io/en/stable/)


# How to Install

Python 3.6 and libraries from **requirements.txt** should be installed. It's better to use virtual environment.

```bash
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

# How to Test

```bash
python3 tests.py
```


# Quickstart

1. Run server:

```bash

$ python server.py

```

1. Run client:

```bash

$ python app.py

```

3. Goto http://0.0.0.0:5000/

![afkp screenshot](screenshots/afkp.png)
