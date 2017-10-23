# Dragons of Mugloar solution
**Program written in Python language**

**Tries to solve game goal:**
 * to have consistent dragon survival rate of at least 50%
 * fight with knights with best skills in different weather conditions

![Game Start](/images/game_start.png)


## Run program
* Open python bash console and type:
  * install requirements with `pip install -r requirements.txt` (add `--user` at the end for permissions if needed)
  * start game by typing `python start_battle.py` or run shell script `./start.sh`



## Code explanation

* Written in Python 2.7.12
* For better console output, used are 2 additional requirements:
  * pyfiglet and termcolor 
* Program asks how many rounds would you like to play
* New game is fetched via `dragonsofmugloar.com/api/game` using requests
* Weather is fetched via `dragonsofmugloar.com/weather/api/report/` using requests
* Dragon skills are swapped depending on knight skills and weather
* Dragon data is put to game api to solve battle
* Finally results are displayed whether battle was victorious or not
* Game steps are logged in 'battle.log' file

## Testing
* Code is uploaded to https://www.pythonanywhere.com/ to give others shared console access
* Or testing can be done also manually on your local machine