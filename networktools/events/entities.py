import os, sys
os.environ['JAVA_HOME'] = '/usr/share/java'

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree


try: 
    SNER_ROOT = os.environ['SNER_ROOT']     #'/home/rahuezo/Downloads/stanford-ner-2018-02-27'
except: 
    print """You must set SNER_ROOT env variable first.\nYou need to download SNER from https://nlp.stanford.edu/software/stanford-ner-2018-02-27.zip.
    Extract the folder and change add os.environ['SNER_ROOT'] = <PATH OF stanford-ner-2018-02-27>\n"""
    sys.exit()

CLASSIFIER = os.path.join(SNER_ROOT, 'classifiers/english.muc.7class.distsim.crf.ser.gz')
JAR_FILE = os.path.join(SNER_ROOT, 'stanford-ner.jar')


def stanford_ner(text): 
    sner = StanfordNERTagger(CLASSIFIER, JAR_FILE)
    return sner.tag(word_tokenize(text))


def stanford_ner_to_bio(ner_tagged_text): 
    bio_tagged = []
    prev_tag = 'O'

    for token, tag in ner_tagged_text: 
        if tag == 'O': 
            bio_tagged.append((token, tag))
            prev_tag = tag
            continue
        if tag != 'O' and prev_tag == 'O': 
            bio_tagged.append((token, 'B-{}'.format(tag)))
            prev_tag = tag
        elif prev_tag != 'O' and prev_tag == tag: 
            bio_tagged.append((token, 'I-{}'.format(tag)))
            prev_tag = tag
        elif prev_tag != 'O' and prev_tag != tag: 
            bio_tagged.append((token, 'B-{}'.format(tag)))
            prev_tag = tag
    return bio_tagged


def stanford_ner_to_tree(text): 
    bio_tagged = stanford_ner_to_bio(stanford_ner(text))
    sentence_tokens, sentence_ne_tags = zip(*bio_tagged)
    sentence_pos_tags = [pos for token, pos in pos_tag(sentence_tokens)]

    sentence_conlltags = [(token, pos, ne) 
        for token, pos, ne in zip(sentence_tokens, sentence_pos_tags, sentence_ne_tags)]

    return conlltags2tree(sentence_conlltags)


def get_people(text): 
    tree = stanford_ner_to_tree(text)
    people = set()

    for subtree in tree: 
        if type(subtree) == Tree: 
            if subtree.label() == 'PERSON': 
                people.add(' '.join([token for token, pos in subtree.leaves()]))
    return sorted(list(people))
