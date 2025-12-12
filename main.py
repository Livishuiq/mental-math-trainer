#!/usr/bin/env python3
"""
Mental Math Trainer
Simple terminal game to practice fast arithmetic.
Features:
- difficulty levels (easy / medium / hard)
- timing per question (records response time)
- scoring with streak bonus and time bonus
- simple, beginner-friendly code
"""

import random
import time
import sys

def intro():
    print("="*48)
    print("     MENTAL MATH TRAINER  •  Quick Brain Game")
    print("="*48)
    print("Instructions:")
    print(" - Choose a difficulty (easy / medium / hard).")
    print(" - Answer each math problem as fast and as accurate as you can.")
    print(" - Type 'quit' anytime to stop early.")
    print()

def choose_difficulty():
    while True:
        level = input("Choose difficulty (easy / medium / hard) [easy]: ").strip().lower()
        if level == "":
            return "easy"
        if level in ("easy","medium","hard"):
            return level
        print("Please type easy, medium, or hard.")

def generate_problem(level):
    """Return (question_str, correct_answer)."""
    if level == "easy":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+","-"])
    elif level == "medium":
        a = random.randint(2, 50)
        b = random.randint(2, 50)
        op = random.choice(["+","-","*"])
    else:  # hard
        op = random.choice(["+","-","*","/"])
        if op == "/":
            b = random.randint(2, 12)
            c = random.randint(2, 12)
            a = b * c  # ensure integer division
        else:
            a = random.randint(10, 150)
            b = random.randint(2, 100)

    if op == "+":
        q = f"{a} + {b}"
        ans = a + b
    elif op == "-":
        q = f"{a} - {b}"
        ans = a - b
    elif op == "*":
        q = f"{a} * {b}"
        ans = a * b
    else:  # '/'
        q = f"{a} / {b}"
        ans = a // b

    return q, ans

def compute_score(base_points, correct, time_taken, streak):
    """
    Score calculation:
    - base_points: points for difficulty
    - correct: True/False
    - time_taken: seconds (float)
    - streak: consecutive correct answers before this question
    """
    if not correct:
        return 0
    # time bonus: faster answers get more bonus (max 5)
    time_bonus = max(0, int(5 - time_taken))  # if time_taken <5 seconds -> positive
    # streak multiplier: small extra for consecutive correct (max +5)
    streak_bonus = min(5, streak // 2)
    return base_points + time_bonus + streak_bonus

def play_rounds(level, rounds=10):
    stats = {
        "asked": 0,
        "correct": 0,
        "total_time": 0.0,
        "score": 0,
        "streak": 0,
        "max_streak": 0
    }

    if level == "easy":
        base = 10
    elif level == "medium":
        base = 20
    else:
        base = 30

    print()
    print(f"Starting {rounds} rounds on {level} difficulty. Good luck!")
    print("Answer quickly for time bonuses. Type 'quit' to finish early.")
    print("-"*48)
    for i in range(1, rounds+1):
        q, ans = generate_problem(level)
        stats["asked"] += 1
        print(f"Q{i}: {q} = ?")
        start = time.time()
        user = input("Your answer: ").strip()
        if user.lower() == "quit":
            print("Quitting early...")
            break
        try:
            # allow integer input; if division we used integer division
            user_val = int(user)
        except ValueError:
            print("Invalid input — counted as incorrect.")
            stats["streak"] = 0
            stats["max_streak"] = max(stats["max_streak"], stats["streak"])
            continue
        end = time.time()
        elapsed = end - start
        stats["total_time"] += elapsed

        correct = (user_val == ans)
        if correct:
            stats["correct"] += 1
            stats["streak"] += 1
            stats["max_streak"] = max(stats["max_streak"], stats["streak"])
            gained = compute_score(base, True, elapsed, stats["streak"])
            stats["score"] += gained
            print(f"Correct! (+{gained} pts)  Time: {elapsed:.2f}s  Streak: {stats['streak']}")
        else:
            stats["streak"] = 0
            print(f"Wrong. Correct answer was {ans}.  Time: {elapsed:.2f}s")

        print("-"*48)

    return stats

def show_summary(stats):
    accuracy = (stats["correct"] / stats["asked"])*100 if stats["asked"] else 0
    avg_time = (stats["total_time"] / stats["asked"]) if stats["asked"] else 0
    print()
    print("="*28 + " SUMMARY " + "="*28)
    print(f"Questions answered: {stats['asked']}")
    print(f"Correct answers:   {stats['correct']}")
    print(f"Accuracy:          {accuracy:.1f}%")
    print(f"Total score:       {stats['score']}")
    print(f"Average time/q:    {avg_time:.2f}s")
    print(f"Best streak:       {stats['max_streak']}")
    print("="*68)
    print("Thanks for playing! Share this repo and invite friends to compete.")
    print()

def main():
    intro()
    level = choose_difficulty()
    # choose number of rounds
    while True:
        rounds_input = input("How many questions would you like? [10]: ").strip()
        if rounds_input == "":
            rounds = 10
            break
        try:
            rounds = int(rounds_input)
            if rounds <= 0:
                print("Pick a positive number.")
                continue
            break
        except ValueError:
            print("Please type a number (e.g., 10).")

    stats = play_rounds(level, rounds)
    show_summary(stats)

    # option to save results
    save = input("Save results to a text file? (y/N): ").strip().lower()
    if save == "y":
        filename = f"mental_math_results_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write("Mental Math Trainer Results\n")
            f.write(f"Asked: {stats['asked']}\n")
            f.write(f"Correct: {stats['correct']}\n")
            f.write(f"Score: {stats['score']}\n")
            f.write(f"Best streak: {stats['max_streak']}\n")
        print(f"Saved to {filename}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye! (interrupted)")
        sys.exit(0)
