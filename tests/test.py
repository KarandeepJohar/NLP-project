import unittest
import os
import sys
from src import answer
from src.tfidf import TF_IDF
from src.init import logger
class SimplisticTest(unittest.TestCase):

    def test(self):
        """Is five successfully determined to be prime?"""
        self.assertTrue(True)

    def test_answers(self):
        args = ["tests/wiki.txt","tests/questions.txt","tests/answers.txt"]
        logger.critical('This message should go to the log file')
        with open(args[0], "r") as article , open(args[1],"r") as questions:
            data = article.read()
            questionsList = questions.read().split('\n')
            objTfidf = TF_IDF(data, questionsList)
            # print questionsList
            for question in questionsList:
                #fluency check
                #interestingText can be a list of tuples of (sentence,score)
                print 'Q: '+question
                interestingText = objTfidf.getInterestingText(question)
                for it in interestingText:
                    print 'IT: ' + ' '.join(it[1])
                for answer in objTfidf.getAnswer(question, interestingText):
                    print 'PA: '+answer
        self.assertTrue(True)
if __name__ == '__main__':

    unittest.main()