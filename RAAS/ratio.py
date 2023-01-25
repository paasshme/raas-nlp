import mlconjug3
import spacy
import os
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.load(os.getenv("FR_MODEL"))
default_conjugator = mlconjug3.Conjugator(language='fr')

pronoms_reflechis = ["me", "te", "se", "nous", "vous", "m'", "t'", "s'"]
print("Init lemma read")
data = {}
# join cwd with env var
with open(os.path.join(os.getcwd(), os.getenv("LEMMA_FILE")), "r", encoding="utf-8") as f:
    for line in f.readlines():
        splitLine = line.split('\t')
        data[splitLine[1].rstrip()] = splitLine[0]

print("lemma read done!")

def phrase_to_ratio(phrase):

    if "j'" not in phrase.lower() and "je " not in phrase.lower():
        return ""

    phrase = phrase.replace(".", "")
    phrase = phrase.replace(",", "")
    phrase = phrase.replace("!", "")
    phrase = phrase.replace(";", "")
    phrase = phrase.replace("?", "")

    doc = nlp(phrase)
    print([(token.pos_, token.text) for token in doc])
    verb_token = None
    i = 0
    b = 0
    docElemToPop = 0
    
    # find the pronoum
    for token in doc:
        if token.pos_ == "PRON":
            break
        b+=1 + len(token.text)
        docElemToPop += 1

    # find the verb (or aux)
    for token in doc:
        if token.pos_ == "AUX":
            verb_token = token
            break
        if token.pos_ == "VERB":
            verb_token = token
            break
        i+=1

    # if the verb is pronominal
    if verb_token.text in pronoms_reflechis:
        verb_token = doc[i+1]
        i+=1
    


    phrase = phrase[b:]
    i -= docElemToPop

    if verb_token:
     
        try:
            conjugated_verb =  default_conjugator.conjugate(verb_token.lemma_).conjug_info['Indicatif']['Présent']['3s']
        except:
            if verb_token.text in data:
                verb = data[verb_token.text]
                conjugated_verb =  default_conjugator.conjugate(verb).conjug_info['Indicatif']['Présent']['3s']
            else:
                print("no lemma found for " + verb_token.text)
                conjugated_verb = verb_token.text

        print(f"p>>>  '{phrase}'")
        if "j'" in phrase or "J'" in phrase:
            phraseSplit = phrase.split(" ")
            print(f" in j >>> {phraseSplit[i-1]}")
            phraseSplit[i-1] = "il " + conjugated_verb
        else:
            phraseSplit = phrase.split(" ")
            phraseSplit[i] = conjugated_verb


        phrase = " ".join(phraseSplit)
        phrase = phrase.replace(" je "," il ")
        phrase = phrase.replace("je ","il ")
        phrase = phrase.replace("Je ","il ")
        phrase = phrase.replace("J'","il ")
        phrase = phrase.replace(" j'","il ")
        phrase = phrase.replace(" m'"," s'")
        phrase = phrase.replace(" me "," se ")
        phrase = phrase.rstrip()

    res = f"Et ce ratio {phrase} ???"
    print("res" + res)
    return res




if __name__ == "__main__":

    # Test 1
    assert phrase_to_ratio("Je mange du pain") == "Et ce ratio il mange du pain ???"

    # Test 2
    assert phrase_to_ratio("Je vais à la piscine") == "Et ce ratio il va à la piscine ???"

    # Test 3
    assert phrase_to_ratio("Je suis en train de travailler") == "Et ce ratio il est en train de travailler ???"

    # Test 4
    assert phrase_to_ratio("Je suis heureux") == "Et ce ratio il est heureux ???"

    # Test 5
    assert phrase_to_ratio("Je parle français") == "Et ce ratio il parle français ???"

    # Test 6
    assert phrase_to_ratio("Je joue au football") == "Et ce ratio il joue au football ???"

    # Test 7
    assert phrase_to_ratio("Je fais du shopping") == "Et ce ratio il fait du shopping ???"

    # Test 8
    assert phrase_to_ratio("Je vais à l'école") == "Et ce ratio il va à l'école ???"

    # Test 9
    assert phrase_to_ratio("Je prends un café") == "Et ce ratio il prend un café ???"

    # Test 10
    assert phrase_to_ratio("Je lis un livre") == "Et ce ratio il lit un livre ???"

    # Test 11
    assert phrase_to_ratio("J'ai fait des pâtes") == "Et ce ratio il a fait des pâtes ???"

    # Test 12
    assert phrase_to_ratio("Hier j'ai fait des pâtes") == "Et ce ratio il a fait des pâtes ???"

    # Test 13
    assert phrase_to_ratio("Et au fait, hier j'ai fait du riz") == "Et ce ratio il a fait du riz ???"

    # Test 14
    assert phrase_to_ratio("Et au fait, demain je pense à toi") == "Et ce ratio il pense à toi ???"

    # Test 15
    assert phrase_to_ratio("Et oui, hier j'ai fait du jus") == "Et ce ratio il a fait du jus ???"

    
    # Test 16: pronominaux
    assert phrase_to_ratio("Je te déteste") == "Et ce ratio il te déteste ???"
    assert phrase_to_ratio("Je te mange fort") == "Et ce ratio il te mange fort ???"
    #assert phrase_to_ratio("Je m'en fou") == "Et ce ratio il s'en fou ???"
    assert phrase_to_ratio("Je me vois pas faire ça") == "Et ce ratio il se voit pas faire ça ???"
