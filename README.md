# **Geogramint - OSINT Geolocalization tool for Telegram**
<p align="center">
<img src="https://github.com/Alb-310/Geogramint/blob/master/appfiles/Geogramint.png" width="300"/>
</p>

<p align="center"> <img src="https://img.shields.io/badge/version-1.0-orange" /> <img src="http://ForTheBadge.com/images/badges/made-with-python.svg"/> <a href="https://github.com/Alb-310"> <img alt="GitHub" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/><a/> <a href="https://twitter.com/Alb_310"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/by-alb310.svg"/><a/> <img src="https://img.shields.io/badge/License-GPLv3-blue.svg"/>
<p align="center"> <a href="https://projetfox.com/"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/fox%20badge.png" width="200"/> <a/>

## **About**

Geogramint is an OSINT tool that uses Telegram's API to find nearby users and groups. Inspired by [Tejado's Telegram Nearby Map](https://github.com/tejado/telegram-nearby-map), which is no longer maintained, it aims to provide a more user-friendly alternative.

Geogramint only finds Telegram users and groups which have activated the nearby feature. Per default it is deactivated.

The tool is fully supported on Windows and partially supported on Mac OS and Linux distributions.

<p align="center"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/Geogramint_image.png" />

## 🛠️ Installation

**Requirements:** [Python 3.8 or 3.9](https://www.python.org/downloads/release/python-3913/)<br>

### On Windows [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)

+ #### With the installer: Click [here!](https://github.com/Alb-310/Geogramint/releases/tag/1.0)
+ #### With Github:
```bash
git clone https://github.com/Alb-310/Geogramint.git
cd Geogramint/
pip3 install -r requirements.txt

python3 geogramint.py
```
Or depending on your installation :
```bash
git clone https://github.com/Alb-310/Geogramint.git
cd Geogramint/
pip install -r requirements.txt

python geogramint.py
```

### On Mac OS  [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg) and Linux [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)

+ #### With Github:
```bash
git clone https://github.com/Alb-310/Geogramint.git
cd Geogramint/
pip3 install -r requirements.txt

python3 geogramint.py
```
Or depending on your installation :
```bash
git clone https://github.com/Alb-310/Geogramint.git
cd Geogramint/
pip install -r requirements.txt

python geogramint.py
```

More details in the [Wiki](https://github.com/Alb-310/Geogramint/wiki/Installation-Guide).

## 📡 Example

1. Start by creating an API key for your Telegram account [here](https://my.telegram.org). You will also need to put a profile picture on your account and, in your `Privacy and Security` settings, enable the profile picture for everyone.

<p align="center"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/privacy_settings.jpg" width="300"/>

2. Launch **Geogramint**
3. In the settings, write your information (api_id, api_hash and phone number) and then `save`

<p align="center"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/Geogramint_settings_1.png" width="500"/> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/Geogramint_settings_2.png" width="500"/>

4. Choose the location where you want to search, either by moving around the map or by using the search feature with coordinates in `lat, lon` format

<p align="center"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/Geogramint_search.png" width="700"/>

5. Telegram will send you a verification code, write it in the pop-up window (+ your two-step verification password if you have one)

<p align="center"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/Geogramint_code.png" width="700"/>

6. Then click `Start Search`
7. All results will be displayed following: 
+ green for 500m
+ yellow for 1000m
+ orange for 2000m
+ red for >3000m

(NB: results can also be found in `Geogramint/cache_telegram/` in `json` format + profiles pictures)

<p align="center"> <img src="https://github.com/Alb-310/Geogramint/blob/master/.github/Geogramint_results.png" width="700"/>

8. `Reset` will clear the results and erase the `cache_telegram`

More details in the [Wiki](https://github.com/Alb-310/Geogramint/wiki/Demonstration).

## 📖 Wiki

Remember to check the [Wiki](https://github.com/Alb-310/Geogramint/wiki) before posting an issue or asking a question.

## 📝 License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)

## 🙏 Thanks to:
+ My teammates at Projet FOX
+ [sergiombd](https://github.com/sergiombd)
