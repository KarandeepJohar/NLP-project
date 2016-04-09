from __future__ import absolute_import
import pprint
import logging
from stanford_corenlp_pywrapper import CoreNLP
from collections import Counter
import os
import chardet
import unicodedata
# dir = "."
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
configFileLoc = os.path.join(dir, 'config.ini')
proc1 = CoreNLP(configfile=configFileLoc, corenlp_jars=[filename])
proc2 = CoreNLP(configfile=os.path.join(dir, 'simple.ini'), corenlp_jars=[filename])
proc3 = CoreNLP(configfile=os.path.join(dir, 'mid.ini'), corenlp_jars=[filename])
puncTags = ['.',',','IN','#','$','CC','SYM','-LRB-','-RRB-',"''",'``',"'","`",'"',':',';','[',']','{','}','-','_','!','?','~','&','*']
LOG_FILENAME = 'log.log'
LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }

MIN_PARA_SIZE = 4
# def removeHeadingsOld(article):
#     data = article.read()
#     data = str(unicode(data, errors='ignore'))
#     splitData = data.split('\n')
#     title = ' '.join(splitData[0].split('_'))+'.'
#     finalParas = []
#     for para in splitData:
#         if len(para.split())>MIN_PARA_SIZE:
#             finalParas.append(para)
#     data = '\n'.join(finalParas)
#     titleLemmas = [w.lower() for w in proc2.parse_doc(title)['sentences'][0]['lemmas']]
#     titleLemmasSet = set(titleLemmas)
#     for tL in titleLemmas:
#         parts = tL.split('_')
#         if len(parts)>1:
#             titleLemmasSet|=set(parts)
#     return data,titleLemmasSet

def removeHeadings(article):
    data = article.read()
    code = chardet.detect(data)
    paragraphs = data.decode(code['encoding'], errors="ignore")
    data = unicodedata.normalize('NFKD', paragraphs).encode('ascii','ignore')
    data = str(unicode(data, errors='ignore'))
    splitData = data.split('\n')
    splitData = [para for para in splitData if para]
    splitData[0] = splitData[0].split('(')[0]
    title = ' '.join(splitData[0].split('_')).strip()
    i=0
    for i in range(1,len(splitData)):
        para = splitData[i]
        if len(para.split())<=MIN_PARA_SIZE:
            break
    pronounCount=Counter()
    for para in splitData[1:i]:
        pronounCount['It'] += para.count('. It')+para.count('. They')+para.count('. Their')
        pronounCount['He'] += para.count('. He')+para.count('. His')
        pronounCount['She'] += para.count('. She')+para.count('. Her')
        pronounCount['It'] += para.count('. It')
    if i>0 and sum(pronounCount.values())>0:
        most_common,_ = pronounCount.most_common(1)[0]
        for j in range(1,i):
            if most_common=='It':
                splitData[j] = splitData[j].replace('. Its','. '+title+'\'s')
                splitData[j] = splitData[j].replace('. It','. '+title)
                splitData[j] = splitData[j].replace('. They','. '+title)
                splitData[j] = splitData[j].replace('. Their','. '+title+'\'s')
            if most_common=='He':
                splitData[j] = splitData[j].replace('. He','. '+title)
                splitData[j] = splitData[j].replace('. His','. '+title+'\'s')
            if most_common=='She':
                splitData[j] = splitData[j].replace('. She','. '+title)
                splitData[j] = splitData[j].replace('. Her','. '+title+'\'s')
    finalParas = []
    for i in range(1,len(splitData)):
        para = splitData[i]
        if len(para.split())>MIN_PARA_SIZE:
            finalParas.append(para)
    data = '.\n '.join(finalParas)
    titleLemmas = [w.lower() for w in proc2.parse_doc(title)['sentences'][0]['lemmas']]
    titleLemmasSet = set(titleLemmas)
    for tL in titleLemmas:
        parts = tL.split('_')
        if len(parts)>1:
            titleLemmasSet|=set(parts)
    return data,titleLemmasSet

logger = logging.getLogger('NLP')
#default is append
fh = logging.FileHandler(LOG_FILENAME, mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'))

logger.addHandler(fh)
logger.info("............STARTING UP...........")
