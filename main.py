from pprint import pprint

import spacy
from spacy import displacy
from spacy.tokens import Doc, Token, Span
from spacy.matcher import Matcher

# // SPACY SETUP // 
# Load the installed model "en_core_web_lg"
nlp = spacy.load("en_core_web_lg")

questions_list = [
    "Should I buy GME stock?", # sentiment, rating, yes/no -> 5 documents that had to do with "should buy", "fundamentals"
    "Who are top electric car makers?", # Tesla, Nio, Li auto
    "How did Apple perform in 2021?", #revenue, profit & loss, tearsheet?
    "Who are competitors to Nano Dimension?",
    "Should I buy AMC stock?",
]

nlp_docs = []
matched_sents = [] # collect data of matched sentences to be visualized

for question in questions_list:
    ####################
    # NLP object setup:
    ####################
    # // PIPELINE // tune pipeline for speed
    # nlp.add_pipe("html_merger", last=True) # add component
    # print(nlp.pipe_names)

    # // NLP OBJ //
    doc = nlp(question)
    print('\n Query: ', doc)
    nlp_docs.append(doc)


    # // MATCHER //
    matcher = Matcher(nlp.vocab)

    # Define rule for text extraction
    # whenever "buy" is followed by "proper noun (name of company)" and "noun", matcher finds pattern in text
    pattern_upgrade_downgrade = [{'TEXT': 'buy'}, {'POS': 'PROPN'}, {'POS': 'NOUN'}] # upgrade/downgrades
    matcher.add('upgrade_downgrades', [pattern_upgrade_downgrade])

    pattern_performance = [{'POS': 'PROPN'}, {'TEXT': 'perform'}] # tearsheet/ sentiment
    matcher.add('performance', [pattern_performance])

    pattern_competitors = [{'TEXT': 'competitors'}, {'DEP': 'prep'}, {'POS': 'PROPN'}] # peer competitors, secondary ticker?
    matcher.add('competitors', [pattern_competitors])

    matches = matcher(doc)
    print('matches: ', matches)

    for match_id, start, end in matches:
        # get matched span
        matched_span = doc[start:end]
        span = Span(doc, start, end, label=match_id)
        sentence = span.sent # sentence containing matched span
        print('matched spans: ', span.text, ' | rule:', span.label_)

        # for manual viz only.
        # match_ents = [{
        #     "start": span.start_char - sentence.start_char,
        #     "end": span.end_char - sentence.start_char,
        #     "label": "MATCH",
        # }]
        # matched_sents.append({"text": sentence.text, "ents": match_ents})


    # // POS // text -> part-of-speech tagging
    # spacy.explain("nsubj") - if you need expansion
    pprint([(token.text, "-->", token.pos_, "-->", token.dep_) for token in doc])
    # word embeddings check
    # pprint([has_vector: ", token.has_vector, "vector_norm: ", token.vector_norm, "is_oov: ", token.is_oov) for token in doc])

    # // NER // for all entities
    # extract ORGS for ticker searches?
    # extract DATE for timeframe? 24 hr filter?
    for ent in doc.ents:
        print('NER: ', ent.text, ' -->', ent.label_)


# // VIS // localhost:5000
displacy.serve(nlp_docs, style="dep")
# displacy.serve(nlp_docs, style="ent")
# displacy.serve(matched_sents, style="ent", manual=True)