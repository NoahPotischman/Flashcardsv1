from flask import Flask, render_template, request, redirect, url_for, flash
import random
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

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
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/username", methods=["POST"])
def get_username():
    username = request.form["username"]
    user_data = load_user_data(username)
    return redirect(url_for("quiz", username=username))

@app.route("/quiz/<username>", methods=["GET", "POST"])
def quiz(username):
    user_data = load_user_data(username)

    if request.method == "POST":
        user_answer = request.form["user_answer"]
        prompt = request.form["prompt"]
        answer = request.form["answer"]

        if user_answer.lower() == answer.lower():
            flash("Correct!")
            user_data["correct"].append(prompt)
        else:
            flash("Incorrect!")
            user_data["incorrect"].append(prompt)

        save_user_data(username, user_data)
        return redirect(url_for("quiz", username=username))

    flashcards_to_show = leitner_system(flashcards, user_data)
    random.shuffle(flashcards_to_show)
    card = flashcards_to_show[0]
    return render_template("quiz.html", card=card, username=username)

@app.route("/statistics/<username>")
def show_statistics(username):
    user_data = load_user_data(username)
    return render_template("statistics.html", user_data=user_data)

if __name__ == "__main__":
    # Create a list of Flashcard instances
    flashcards = [
        Flashcard("What is the capital of France?", "Paris"),
        Flashcard("What is the capital of Italy?", "Rome"),
    ]
    app.run(debug=True)
