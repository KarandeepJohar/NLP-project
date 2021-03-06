#! /usr/bin/env python
# -*- coding: utf8 -*-
#
# Link Grammar example usage
#

# sudo apt-get install python-dev
# ./configure --enable-python-bindings --disable-java-bindings
# make
# sudo make install
# sudo ldconfig


import locale

from linkgrammar import Sentence, ParseOptions, Dictionary
# from linkgrammar import _clinkgrammar as clg

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

po = ParseOptions()
#po = ParseOptions(linkage_limit=3)

def desc(lkg):
    print lkg.diagram()
    print 'Postscript:'
    print lkg.postscript()
    print lkg.violation_name()
    # print lkg.senses()
    print '---'

def s(q):
    return '' if q == 1 else 's'

def linkage_stat(psent, lang):
    """
    This function mimics the linkage status report style of link-parser
    """
    random = ' of {0} random linkages'. \
             format(psent.num_linkages_post_processed()) \
             if psent.num_valid_linkages() < psent.num_linkages_found() else ''

    print '{0}: Found {1} linkage{2} ({3}{4} had no P.P. violations)'. \
          format(lang, psent.num_linkages_found(),
                 s(psent.num_linkages_found()),
                 psent.num_valid_linkages(), random)

dictionary = Dictionary()
def is_grammatical(ques):
    sent = Sentence(ques, dictionary, po)
    linkages = sent.parse()
    if sent.num_valid_linkages()==0:
        return False
    linkage_stat(sent, 'English')
    # for linkage in linkages:
    #     desc(linkage)
    #     print linkage.link_cost()
    return True
# English is the default language
sent = Sentence("What recalled the actor gave a 'Who are you guys' ?", Dictionary(), po)
# sent = Sentence("Who , the Kelvin's first officer , orders the ship's personnel , including his pregnant wife Winona , to abandon ship while he pilots the Kelvin on a collision course with the Narada , as the auto-pilot function is damaged ?", Dictionary(), po)
# how is you doing
print is_grammatical("Did John play chess or checkers ?")
# linkages = sent.parse()
# print is_grammatical(sent, 'English')
# linkage_stat(sent, 'English')
# c=0
# for linkage in linkages:
#     c+=1
#     desc(linkage)

# print c