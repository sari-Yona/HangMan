from requests import session
from hangMan import hang
from colorama import init, Fore
import pygame
import time

# אתחול pygame- עבור ספרית הצלילים
pygame.mixer.init()

# אתחול הצבעים
init()
# איתחול הSSESION
session = session()

basic_url = "http://127.0.0.1:5000"


# השמעת צלילים
def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    # המתן עד שהשמע יסתיים
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


# פונקציה להחלפת אות במחרוזת
def replace_char(string, index, new_char):
    # המרת המחרוזת לרשימה
    s_list = list(string)
    # החלפת האות באינדקס
    s_list[index] = new_char
    # המרת הרשימה חזרה למחרוזת
    return ''.join(s_list)


# הגרלה
def lottery():
    try:
        num = int(input("Enter a num: "))
    except ValueError as e:
        print("Error!! enter only nums!")
        lottery()
    response = session.get(f"{basic_url}/lottery/{num}")
    if response.status_code == 200:
        return response.text
    elif response.status_code == 401:
        print("Oops! pleas log in!!")
        return ""


# התחברות
def login():
    name = input("Enter your name: ")
    password = input("Enter your passord: ")
    player = {"name": name, "password": password}
    response = session.post(f"{basic_url}/login", json=player)
    # cookie = response.cookies.get_dict()
    if response.status_code == 404:
        print("Pleas sign in!")
    else:
        print(f"Hello {response.cookies.get_dict()['user']}! wellcom to our amazing game!!")
    return response.status_code


# הרשמה
def signin():
    name = input("Enter your name: ")
    password = input("Enter your passord: ")
    Id = input("Enter your Id number: ")
    player = {"name": name, "password": password, "Id": Id}
    response = session.post(f"{basic_url}/signin", json=player)
    if response.status_code == 404:
        print("Password exists!")
        signin()
    else:
        print(f"Hello {response.cookies.get_dict()['user']}! wellcom to our amazing game!!")

    return response.status_code


# דף בית למשתמש מחובר
def home():
    try:
        num = int(input("""Hello! Wellcome to the hang-man game.
Press 1 to start play
2 to history,
3 to log out
"""))
    except ValueError as e:  # תקינות  הקלט
        print("You're wrong! Press only 1, 2 or 3.")
        home()
    if num == 1:
        word = lottery()
        if word == "":
            login()
        else:
            game(word)
    elif num == 2:
        history()
    elif num == 3:
        # התנתקות ומחיקת העוגיה
        response = session.get(f"{basic_url}/del-cookie")
        if response.status_code == 200:
            print("\033[38;5;200m" + "Have a good day :)" + "\033[0m")
        elif response.status_code == 401:
            print("You are not logged in anymore. Details not saved.")
    else:  # תקינות  הקלט
        print("You are wrong! Please press only 1, 2 or 3.")


# קבלת ההיסטוריה של המשתמש הנוכחי
def history():
    response = session.get(f"{basic_url}/history")
    if response.status_code == 401:
        print("Oops! pleas log in!!")
        login()
        history()
    else:
        data = response.json()  # המרת התגובה ל-JSON
        print(data)
        home()


# דף בית למשתמש שאינו מחובר עדיין
def wellcome():
    try:
        num = int(input("""Hello! Wellcome to the hang-man game.
Press 1 to log in and start play. Press 2 to enrollment. """))
    except ValueError as e:  # תקינות  הקלט
        print("You're wrong! Enter only numbers!")
        wellcome()
    if num == 1:
        status = login()
        if status == 200:
            word = lottery()
            if word == "":
                login()
            else:
                game(word)
        else:
            signin()
            home()
    elif num == 2:
        signin()
        home()
    else: #תקינות  הקלט
        print("You are wrong! Please press only 1 or 2.")
        wellcome()


# כישלון
def fail(word):
    print(Fore.RED + "Failure!!" + Fore.RESET)
    print(f"The word was: {word}...")
    data = {"word": word, "win": False}
    response = session.post(f"{basic_url}/finish", json=data)
    if response.status_code == 200:
        print("Details have been updated successfully.")
        home()
    elif response.status_code == 401:
        print("Your login has expired. The details are not saved in the system. Pleas log in again.")
        wellcome()
    elif response.status_code == 500:
        print("Details was not updated.")
        wellcome()


# ניצחון
def win(word):
    print("\033[38;5;82m" + "Yoa are win!!!!" + "\033[0m")
    print(f"The word was: {word}!!")
    data = {"word": word, "win": True}
    response = session.post(f"{basic_url}/finish", json=data)
    if response.status_code == 200:
        print("Details have been updated successfully.")
        home()
    elif response.status_code == 401:
        print("Your login has expired. The details are not saved in the system. Pleas log in again.")
        wellcome()
    elif response.status_code == 500:
        print("Details was not updated.")
        wellcome()


# המשחק עצמו
def game(word):
    currentWord = word
    show = "_ " * len(word)
    failure = 0
    #print(word)
    while True:
        print(f"Your word is {show}. you have another {7 - failure} wrong times.")
        letter = input("Enter a letter: ")
        while not (letter.isalpha() and letter.islower()):  #תקינות  הקלט
            print("You must enter only a lowercase English letter!")
            letter = input("Enter a letter: ")
        index = currentWord.find(letter)
        if index == -1:
            play_sound('./bad.mp3')
            print(Fore.RED + "O'ops! you are not right!" + Fore.RESET)
            print("\033[38;5;200m" + hang[failure] + "\033[0m")
            failure += 1
            # בדיקת כישלון
            if failure == 7:
                fail(word)
                break
        else:
            play_sound('./good.mp3')
            index1 = word.find(letter)
            while show[index1 * 2] != "_":
                index1 = word.find(letter, index1 + 1)
            show = replace_char(show, index1 * 2, letter)
            currentWord = replace_char(currentWord, index, "")
            print("\033[38;5;82m" + "success!" + "\033[0m")
            # בדיקת הצלחה
            if show.find("_") == -1:
                win(word)
                break
