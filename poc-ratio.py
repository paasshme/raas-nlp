import spacy

nlp = spacy.load("fr_core_news_md")

def phrase_to_ratio(phrase):
    doc = nlp(phrase)
    for token in doc:
        if token.pos_ == "VERB":
            verb = token.text
            conjugated_verb = token.lemma_
            break
    return "Et ce ratio il {} {} ???".format(conjugated_verb, " ".join([token.text for token in doc if token.pos_ != "VERB"]))
