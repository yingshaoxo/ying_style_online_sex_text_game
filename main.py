import random
import os
import json


#########
# Normally, user_states saves user progress
#########

data_path = "./data.json"

user_states = {
    "yingshaoxo": {
        "level": 0,
    }
}


#########
# Normally, event functions should return [direct reply, interact method, arguments, next_function]
#########

class Event_Function_Class():
    def __init__(self, username):
        self.username = username
        self.event_functions = [
            [{"level": 0}, self.ask_for_account_register],
            [{"level": 1}, self.say_hi],
            [{"level": 1}, self.luck_day],
            [{"level": 2}, self.level_2],
            [{"level": 2}, self.level_2_i_see_a_girl_on_street],
            [{"level": 2}, self.level_2_gambling],
            [{"level": 2}, self.luck_day],
        ]
        if username not in user_states:
            user_states[self.username] = {
                "level": 0
            }

    def _print_debug_information(self):
        print(user_states[self.username])

    def _save_json_data(self):
        global user_states
        json_text = json.dumps(user_states, indent=4)
        with open(data_path, "w") as f:
            f.write(json_text)

    def _load_json_data(self):
        global user_states
        try:
            with open(data_path, "r") as f:
                json_text = f.read()
            user_states = json.loads(json_text)
        except Exception as e:
            print(e)
        self.__init__(self.username)

    def _set_user_level(self, level):
        user_states[self.username]["level"] = level

    def _get_user_level(self):
        return user_states[self.username]["level"]

    def look_around_in_that_level(self):
        return "", "look_around", "", self.look_around_in_that_level

    def ask_for_account_register(self):
        return "Do you want to get into a sex world? Give me your name!", "input_box", "input your name here:", self.reset_username

    def reset_username(self, response):
        #response = response.strip()
        #if response != "":
        #    self.__init__(response)
        #    self._set_user_level(1)
        #    return "Great, now you got a name.", "redirect", "Let's go to level 1.", self.say_hi
        #return "You should input something valid.", "redirect", "Let me do it!", self.ask_for_account_register
        self._set_user_level(self._get_user_level() + 1)
        return "Oh fuck, I forgot you told me your name before, sorry.", "redirect", "Now let's go to level 1.", self.say_hi

    def say_hi(self):
        return "There is a girl says Hi to you!", "choice", ["Say hi to her", "Refuse to say anything"], self.handle_hi

    def handle_hi(self, response):
        if "Say hi to her" in response:
            return "Hi! "+self.username+"!", "redirect", "What is the next?", self.level_up_for_free
        elif "Refuse to say anything" in response:
            return "Well, if you keep silence, girl keep silence.", "redirect", "Let's go back to hi", self.say_hi
        return "Well, if you keep silence, girl keep silence.", "redirect", "Let's go back to hi", self.say_hi
    def luck_day(self):
        result = random.choice([1,2,3])
        if result == 1:
            return "Oh! You got luck, today you meet the god: " + "ying" + "shao" + "xo" + ". So I would consider to level you up for free.", "redirect", "Yes, let's do it", self.level_up_for_free
        else:
            return "Maybe you should go around by hitting the enter button one more time", "redirect", "Thanks", self.look_around_in_that_level

    def level_up_for_free(self):
        self._set_user_level(self._get_user_level() + 1)
        return "OK! You just leveled up to " + str(self._get_user_level()), "redirect", "Thanks", self.look_around_in_that_level

    def level_2(self):
        return "Now you are in level 2", "redirect", "What's next?", self.look_around_in_that_level

    def level_2_i_see_a_girl_on_street(self):
        return "Wow! You just found a beauty on the street! How good her face and skin and legs looks like! Beautiful!", "redirect", "What's next?", self.look_around_in_that_level

    def level_2_gambling(self):
        return "You just meet a man who says you can have a gambling with him. Now you make a choice of [up, even, down]", "choice", ["The stock market will go up", "The stock market will not change", "The stock market will go down"], self.level_2_gambling_result

    def level_2_gambling_result(self, response):
        result = random.choice([1,2,3])
        if result == 1:
            return "Congratulations! You win!", "redirect", "What's next?", self.look_around_in_that_level
        elif result == 2:
            return "So bad! You loss!", "redirect", "What's next?", self.look_around_in_that_level
        return "Sorry! Your money get ate by monsters!", "redirect", "What's next?", self.look_around_in_that_level


#########
# Game Handler
#########

def game_loop(username):
    event_function_class = Event_Function_Class(username=username)
    event_function_class._load_json_data()
    while True:
        user_level = event_function_class._get_user_level()
        available_event_functions = []
        for event in event_function_class.event_functions:
            # could be <=
            if event[0]["level"] == user_level:
                available_event_functions.append(event[1])

        if len(available_event_functions) > 0:
            target_function = random.choice(available_event_functions)
        else:
            os.system("clear")
            print("You just reached highest level. Goodbye! May god bless you!")
            exit()

        direct_reply, interact_method, arguments, next_function = target_function()
        while True:
            print("\n\n----------------\n\n")
            os.system("clear")

            event_function_class._print_debug_information()
            event_function_class._save_json_data()
            print("\n\n----------------\n\n")

            print(direct_reply)
            print("\n\n")
            if interact_method == "redirect":
                input(arguments + " (Hit enter to continue) ")
                direct_reply, interact_method, arguments, next_function = next_function()
            elif interact_method == "input_box":
                response = input(arguments + " ").strip()
                direct_reply, interact_method, arguments, next_function = next_function(response)
            elif interact_method == "choice":
                response = ""
                while True:
                    for index, choice in enumerate(arguments):
                        print(str(index) + ". " + choice)
                    response = input("\n\nWhat do you choice? (input a number) ").strip()
                    if response.isdigit():
                        index = int(response)
                        if index < len(arguments):
                            response = arguments[index]
                            break
                direct_reply, interact_method, arguments, next_function = next_function(response)
            elif interact_method == "look_around":
                break
            else:
                input("Have a refresh? (y/n)")
                break


def main():
    username = input("What is your name? ").strip()
    game_loop(username)


if __name__ == "__main__":
    main()
