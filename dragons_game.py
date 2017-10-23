#!/usr/bin/env python
import requests
import time
import weather_helper

from helper import Logging, TerminalFontColors


class DragonsOfMugloarGame(Logging):
    DRAGON = 'dragon'
    GAME_ID = "gameId"
    KNIGHT = "knight"
    NAME = "name"

    ATTACK = "attack"
    ARMOR = "armor"
    AGILITY = "agility"
    ENDURANCE = "endurance"

    VALID_KNIGHT_SKILLS = (ATTACK, ARMOR, AGILITY, ENDURANCE)

    FORECAST = "WEATHER FORECAST:"
    NORMAL_WEATHER = "NMR"  # "Normal fights"
    STORM = "SRO"  # "Everyone dies"
    HEAVY_RAIN = "HVA"  # "Knights come by umbrella boats"
    LONG_DRY = "T E"  # "Kite surfing helps to win battle"
    FOG = "FUNDEFINEDG"  # "Excellent knight locating skills"

    VALID_WEATHER_STATUSES = (NORMAL_WEATHER, STORM, HEAVY_RAIN, LONG_DRY, FOG)

    count_victory = 0
    count_defeat = 0

    def fetch_new_game_from_api(self):
        try:
            game = requests.get('http://www.dragonsofmugloar.com/api/game').json()

            if not game:
                raise ValueError()
            game_id = game.get(self.GAME_ID)
            self.logger.info("Fetching game data from game API with id: %s", game_id)
            knight = game.get(self.KNIGHT)

            self.terminal_output(knight=knight, dragon=False)
            self.extract_knight_skills(knight)
            self.get_weather_forecast(game_id, knight)

        except ValueError:
            self.logger.exception("Failed to fetch game from game API")

    def extract_knight_skills(self, knight):
        knight_name = knight.get(self.NAME)
        knight.pop(self.NAME)
        knight = {str(k): int(v) for k, v in knight.items()}  # converts unicode keys to strings
        self.logger.info("Knight %s is starting to conquer our kingdom", knight_name)
        self.logger.info("Knight has following skills: %s", knight)
        return knight

    def get_weather_forecast(self, game_id, knight):
        weather = requests.get('http://www.dragonsofmugloar.com/weather/api/report/' + str(game_id))
        self.swap_dragon_skills_by_weather(knight, weather, game_id)

    def is_valid_weather_for_battle(self, weather, condition):
        match = weather.text.find(condition)
        return match > 0 and condition in self.VALID_WEATHER_STATUSES

    def create_dragon(self, game_id, values):
        dragon = {self.DRAGON: {
            "scaleThickness": values[0],
            "clawSharpness": values[1],
            "wingStrength": values[2],
            "fireBreath": values[3]
        }}

        self.terminal_output(knight=False, dragon=dragon)

        self.logger.info("Dragon skills: %s" % dragon.get('dragon'))
        self.put_dragon_and_knight_into_fight(game_id, dragon)

    # Beat knight skills with swapping dragon-knight skill values
    @staticmethod
    def set_skills_for_dragon(skill_name, skill_value, max_skill, min_skill):
        if skill_name == max_skill:
            value = skill_value + 2
            return value
        elif skill_name == min_skill:
            return skill_value
        else:
            value = skill_value - 1
            return value

    def swap_dragon_skills_by_weather(self, knight, current_weather, game_id):
        knight_attack = knight.get(self.ATTACK)
        knight_armor = knight.get(self.ARMOR)
        knight_agility = knight.get(self.AGILITY)
        knight_endurance = knight.get(self.ENDURANCE)

        # Find maximum and minimum knight skills to add/subtract skills to dragon
        max_skill = max(knight, key=knight.get)
        min_skill = min(knight, key=knight.get)

        if self.is_valid_weather_for_battle(current_weather, self.NORMAL_WEATHER):
            self.create_dragon(game_id, values=(
                self.set_skills_for_dragon(self.ATTACK, knight_attack, max_skill, min_skill),
                self.set_skills_for_dragon(self.ARMOR, knight_armor, max_skill, min_skill),
                self.set_skills_for_dragon(self.AGILITY, knight_agility, max_skill, min_skill),
                self.set_skills_for_dragon(self.ENDURANCE, knight_endurance, max_skill, min_skill),
            ))
            msg = weather_helper.REGULAR
            print "\n", TerminalFontColors.GREY + self.FORECAST, msg
            self.logger.info("%s: %s", self.FORECAST, msg)

        # STORM: everybody dies
        elif self.is_valid_weather_for_battle(current_weather, self.STORM):
            self.create_dragon(game_id, values=(knight_attack, knight_armor, knight_agility, knight_endurance))
            msg = weather_helper.STORM
            print "\n", TerminalFontColors.GREY + self.FORECAST, msg
            self.logger.info("%s: %s", self.FORECAST, msg)

        # HEAVY RAIN WITH FLOODS: Knights come by umbrella boats
        elif self.is_valid_weather_for_battle(current_weather, self.HEAVY_RAIN):
            self.create_dragon(game_id, values=(4, 10, 6, 0))
            msg = weather_helper.HEAVY_RAIN
            print "\n", TerminalFontColors.GREY + self.FORECAST, msg
            self.logger.info("%s: %s", self.FORECAST, msg)

        # LONG DRY: Dragons who have achieved great balance of their inner-self through meditation
        # and kite surfing can win battles
        elif self.is_valid_weather_for_battle(current_weather, self.LONG_DRY):
            self.create_dragon(game_id, values=(5, 5, 5, 5))
            msg = weather_helper.LONG_DRY
            print "\n", TerminalFontColors.GREY + self.FORECAST, msg
            self.logger.info("%s: %s", self.FORECAST, msg)

        # FOG: Dragons have excellent knight locating skills
        elif self.is_valid_weather_for_battle(current_weather, self.FOG):
            self.create_dragon(game_id, values=(4, 4, 5, 7))
            msg = weather_helper.FOG
            print "\n", TerminalFontColors.GREY + self.FORECAST, msg
            self.logger.info("%s: %s", self.FORECAST, msg)

    def put_dragon_and_knight_into_fight(self, game_id, dragon):
        battle = requests.put("http://www.dragonsofmugloar.com/api/game/" + str(game_id) +
                              "/solution", json=dragon).json()
        battle = {str(k): str(v) for k, v in battle.items()}
        status = battle.get("status")
        message = battle.get("message")

        print TerminalFontColors.YELLOW + status.upper(), ":", message
        self.logger.info("STATUS: %s, Message:  %s:", status, message)

        DragonsOfMugloarGame.count_victory += 1 if status is 'Victory' else DragonsOfMugloarGame.count_defeat + 1
        win_percentage = "{0:.0f}%".format((self.count_victory/(self.count_victory + self.count_defeat)*100))
        time.sleep(1)
        print "\n", TerminalFontColors.RED + "STATISTICS | VICTORY: %s | DEFEAT: %s | WIN RATE: %s" % \
                                             (self.count_victory, self.count_defeat, win_percentage)
        print "-" * 140
        return status

    def terminal_output(self, knight, dragon):
        if knight:
            print "\n", TerminalFontColors.BLUE + "NEW BATTLE BEGINS"
            self.wait()
            print TerminalFontColors.GREEN + "-" * 140
            print TerminalFontColors.GREEN + "Knight:", knight
            self.wait()
            print TerminalFontColors.BLUE + "versus"
            self.wait()
        elif dragon:
            print TerminalFontColors.RED + "Dragon:", dragon.get('dragon')
            self.wait()
            print "-" * 140

    @staticmethod
    def wait():
        return time.sleep(0.3)
