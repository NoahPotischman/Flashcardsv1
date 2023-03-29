import random
import json
import os

# flashcard class
class Flashcard:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer
        self.correct_count = 0

""" function to load user data from a JSON file, create a new one if it doesn't exist"""
def load_user_data(username):
    if not os.path.exists("user_data"):
        os.mkdir("user_data")
    filepath = f"user_data/{username}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            user_data = json.load(f)
    else:
        user_data = {"correct": [], "incorrect": []}
    return user_data

""" function to save user data to a JSON file """
def save_user_data(username, user_data):
    filepath = f"user_data/{username}.json"
    with open(filepath, "w") as f:
        json.dump(user_data, f, indent=2)

""" function to display user statistics """
def show_statistics(user_data):
    print("Correct answers:")
    for question in user_data["correct"]:
        print(question)
    print("\nIncorrect answers:")
    for question in user_data["incorrect"]:
        print(question)

""" implimentation of the Leitner system for flashcard repetition """
def leitner_system(flashcards, user_data):
    new_flashcards = []
    for flashcard in flashcards:
        if flashcard.prompt not in user_data["correct"]:
            new_flashcards.append(flashcard)

    if not new_flashcards:
        user_data["correct"] = []
        new_flashcards = flashcards.copy()
        print("\nYou've answered all questions correctly! The system is resetting...\n")
        
    return new_flashcards

""" The program main function which 
    1. Creates a list of flashcard instances
    2. Gets the users username and loads their data
    3. Runs the main loop """
def main():
    # Create a list of Flashcard instances
    flashcards = [
    Flashcard("What is the capital of France?", "Paris"),
    Flashcard("What is the capital of Italy?", "Rome"),
    Flashcard("What is the capital of Germany?", "Berlin"),
    Flashcard("What is the capital of the United States?", "Washington, D.C."),
    Flashcard("What is the capital of Canada?", "Ottawa"),
    Flashcard("What is the capital of the United Kingdom?", "London"),
    Flashcard("What is the capital of Spain?", "Madrid"),
    Flashcard("What is the capital of Australia?", "Canberra"),
    Flashcard("What is the capital of Brazil?", "Brasília"),
    Flashcard("What is the capital of Argentina?", "Buenos Aires"),
    Flashcard("What is the capital of Russia?", "Moscow"),
    Flashcard("What is the capital of China?", "Beijing"),
    Flashcard("What is the capital of India?", "New Delhi"),
    Flashcard("What is the capital of Japan?", "Tokyo"),
    Flashcard("What is the capital of South Korea?", "Seoul"),
    Flashcard("What is the capital of South Africa?", "Pretoria (executive), Bloemfontein (judicial), Cape Town (legislative)"),
    Flashcard("What is the capital of Mexico?", "Mexico City"),
    Flashcard("What is the capital of Colombia?", "Bogotá"),
    Flashcard("What is the capital of Nigeria?", "Abuja"),
    Flashcard("What is the capital of Egypt?", "Cairo"),
    Flashcard("What is the capital of Turkey?", "Ankara"),
    Flashcard("What is the capital of Iran?", "Tehran"),
    Flashcard("What is the capital of Iraq?", "Baghdad"),
    Flashcard("What is the capital of Saudi Arabia?", "Riyadh"),
    Flashcard("What is the capital of United Arab Emirates?", "Abu Dhabi"),
    Flashcard("What is the capital of Kuwait?", "Kuwait City"),
    Flashcard("What is the capital of Qatar?", "Doha"),
    Flashcard("What is the capital of Oman?", "Muscat"),
    Flashcard("What is the capital of Yemen?", "Sana'a"),
    Flashcard("What is the capital of Afghanistan?", "Kabul"),
    Flashcard("What is the capital of Pakistan?", "Islamabad"),
    Flashcard("What is the capital of Bangladesh?", "Dhaka"),
    Flashcard("What is the capital of Thailand?", "Bangkok"),
    Flashcard("What is the capital of Vietnam?", "Hanoi"),
    Flashcard("What is the capital of Indonesia?", "Jakarta"),
    Flashcard("What is the capital of Philippines?", "Manila"),
    Flashcard("What is the capital of Malaysia?", "Kuala Lumpur"),
    Flashcard("What is the capital of Singapore?", "Singapore"),
    Flashcard("What is the capital of South Sudan?", "Juba")
    ]

    # get the users username and load their data
    username = input("Enter your username: ")
    user_data = load_user_data(username)

    # main loop 
    while True:
        print("\nOptions:")
        print("|--------------------------|")
        print("| 1. Start quiz            |")
        print("| 2. Show statistics       |")
        print("| 3. Exit                  |")
        print("|--------------------------|")


        option = input("Enter option number: ")

        if option == "1":
            flashcards_to_show = leitner_system(flashcards, user_data)
            random.shuffle(flashcards_to_show)
            for card in flashcards_to_show:
                user_answer = input(card.prompt + " ")
                if user_answer.lower() == card.answer.lower():
                    print("Correct!")
                    user_data["correct"].append(card.prompt)
                    card.correct_count += 1
                else:
                    print("Incorrect!")
                    user_data["incorrect"].append(card.prompt)
            save_user_data(username, user_data)

        elif option == "2":
            show_statistics(user_data)

        elif option == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()