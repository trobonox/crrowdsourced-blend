# Crrowdsourced Blend Bot

A bot which adds songs from a Discord thread into a spotify playlist.

## 🚀 Deployment
The only prerequisite is any installation of Python >=3.8.0

Then, install dependencies:
```
pip install -r requirements.txt
```
(This command can slightly vary depending on your operating system, for example on Linux it can be `pip3` instead of pip)

Before running, rename `config.example.json` to `config.json` and populate it with all required values.
To find the needed secrets for the Spotify API, you can consult the [Spotipy Documentation](https://spotipy.readthedocs.io/en/2.22.1/).

Then, you can run it using Python, optimizations are recommended:
```
python -OOO bot.py
```
(Just like with `pip`, this command can slightly vary so you need to use `python3` on Linux and MacOS)

---
© 2022-2023 Trobonox. Licensed under the MIT License.
