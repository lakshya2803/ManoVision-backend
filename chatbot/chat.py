import random
import pickle
import numpy as nm
# import tensorflow as tf

# Positive response function
def positive_response():
    suggestions = [
        "Keep up the great work! Continue practicing mindfulness and self-care.",
        "You're doing amazing! Stay consistent with your routines to maintain your positive state.",
        "Excellent! Stay connected with friends and family to maintain your well-being."
    ]
    return random.choice(suggestions)

# Neutral response function
def neutral_response():
    suggestions = [
        "You're safe, but be cautious. It's easy to slide into a negative state.",
        "Remember, it's okay to not feel great every day. Take time to focus on self-care.",
        "Take a moment to check in with yourself and consider some mindfulness exercises."
    ]
    return random.choice(suggestions)

# Negative response function
def negative_response():
    sympathy_quotes = [
        "It's okay to feel this way, you're not alone. Take it one step at a time.",
        "You matter. It's okay to seek help when you're feeling down.",
        "This too shall pass. Take care of yourself and reach out to someone if you need support."
    ]
    remedies = [
        "Consider engaging in some light physical activity or relaxation exercises.",
        "Try journaling or talking to someone you trust. It's important to express how you're feeling.",
        "Consider reaching out to a mental health professional to help guide you through this tough time."
    ]
    return f"{random.choice(sympathy_quotes)} Here's a remedy: {random.choice(remedies)}"

def evaluate_score(score):
    if score >= 70:
        return "positive"
    elif 30 <= score < 70:
        return "neutral"
    else:
        return "negative"

def chatbot(score):
    # Evaluate the mental health state based on the score
    mental_state = evaluate_score(score)
    
    if mental_state == "positive":
        print("Congratulations! You are in a good mental state.")
        print(positive_response())
    elif mental_state == "neutral":
        print("You're in a neutral state. Be cautious as your mental health can fluctuate.")
        print(neutral_response())
    else:
        print("It seems like you're struggling right now. It's okay to feel this way.")
        print(negative_response())