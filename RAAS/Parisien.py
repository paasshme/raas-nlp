import re
import random

def transform_phrase(phrase):
  words_to_replace = ["le", "la", "les", "un", "une", "des", "aller", "faire", "prendre"]
  replacement_words = ["the", "a", "some", "a", "an", "some", "go", "do", "have"]
  verbs_to_replace = ["aller", "faire", "prendre"]
  replacement_verbs = ["go", "do", "have"]

  for i in range(len(words_to_replace)):
    phrase = re.sub(r"\b" + words_to_replace[i] + r"\b", replacement_words[i], phrase)
  for i in range(len(verbs_to_replace)):
    phrase = re.sub(r"\b" + verbs_to_replace[i] + r"\b", replacement_verbs[i], phrase)

  if random.random() < 0.2:
    phrase += " " + random.choice(["brunch", "asap", "meet", "rooftop", "cocktail"])

  phrase = re.sub(r"([^\s])\s+([^\s])", r"\1 \2", phrase)


  return phrase

print(transform_phrase("Je suis en train de preparer un projet pour mon boss demain."))
