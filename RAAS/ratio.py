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

def preprocess_phrase(phrase):
    phrase = phrase.replace("jsuis ", "je suis ")
    phrase = phrase.replace("Jsuis ", "Je suis ")
    phrase = phrase.replace("jsais ", "je sais ")
    phrase = phrase.replace("Jsais ", "Je sais ")
    phrase = phrase.replace("jui ", "je suis ")
    phrase = phrase.replace("Jui ", "Je suis ")
    phrase = phrase.replace(".", "")
    phrase = phrase.replace(",", "")
    phrase = phrase.replace("!", "")
    phrase = phrase.replace(";", "")
    phrase = phrase.replace("?", "")
    return phrase

def phrase_to_ratio(phrase):

    first_person_pronoums = ["j'", "je ", "jui ", "jsuis ", "jsais "]

    if not any(pronoum in phrase.lower() for pronoum in first_person_pronoums):
        return ""

    phrase = preprocess_phrase(phrase)

    doc = nlp(phrase)
    print([(token.pos_, token.text) for token in doc])
    verb_token = None
    i = 0
    b = 0
    docElemToPop = 0
    cod_index = 0
    cod_before_verb = False
    
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
            cod_index = i
            break
        if token.pos_ == "VERB":
            verb_token = token
            cod_index = i

            break
        i+=1

    # if adv between PRON and AUX handle it diff
    if cod_index > 1 and doc[cod_index - 2].pos_ == "PRON" and doc[cod_index - 1].pos_ == "ADV":
        cod_before_verb = True
     
    if cod_index > 1 and doc[cod_index - 2].pos_ == "PRON" and doc[cod_index - 1].pos_ == "PRON":
        cod_before_verb = True
       
    if cod_before_verb and doc[cod_index - 1].text not in  ["t'", "l'"]:
        cod_before_verb =  False

    

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
        elif cod_before_verb:
            phraseSplit = phrase.split(" ")
            phraseSplit[cod_index-1] = phraseSplit[cod_index-1][:2] + conjugated_verb
            print("COD found")
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


