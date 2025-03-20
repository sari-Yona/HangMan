from funcs import wellcome
from logo import logo
def main():
    print("\033[38;5;200m" + logo + "\033[0m") # מדפיס את הלוגו בצבע ורוד
    wellcome() #פונקצית דף הבית למשתמש לא מחובר עדיין


if __name__ == "__main__":
    main()
