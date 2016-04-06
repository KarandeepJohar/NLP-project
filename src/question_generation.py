import init

class generateQuestions:

    def __init__(self, data, n = 1):
        self.corpus = data
        self.numQues = n
        self.questions = []
        self.generate()
        # self.generate()

    def __str__(self):
        return str(self.questions)

    def getQues(self,parsed):
        questions = []
        for s in parsed['sentences']:
            pos = s['pos']
            ner = s['ner']
            parse = s['parse']
            tokens = s['tokens']
            #TODO improve this Who noted " Fate put me in the movie to show me I was talking out of my ass . ?
            tokens[-1] ="?"
            k = -1
            count = 0
            for i in range(0,len(parse)):
                if count == 0 and parse[i-1:i+1] == 'NP':
                    count = 2
                if count > 1:
                    if parse[i] == '(':
                        count = count + 1
                    elif parse[i] == ')':
                        count = count - 1
                        k = k+1
                if count == 1:
                    break
            i = 0
            tag = pos[i]
            if tokens[i] == "It":
                questions.append('What '+' '.join(tokens[1:]))
            if tag[0:2] == 'NN':
                # TODO: Check for What questions first
                # TODO: Replace whole NP, not just the noun
                if ner[i] == 'PERSON':
                    questions.append('Who '+' '.join(tokens[k:]))
                elif ner[i] == 'LOCATION':
                    questions.append('Where '+' '.join(tokens[k:]))
                elif ner[i] == 'DATE':
                    questions.append('When '+' '.join(tokens[k:]))
                else:
                    questions.append('What '+' '.join(tokens[k:]))
        return questions
    def get_questions(self):
        return self.questions
    def generate(self):
        proc = init.proc1
        pp = init.pprint.PrettyPrinter(indent=2)
        parsed = proc.parse_doc(self.corpus)
        # pp.pprint(parsed)
        self.questions = self.getQues(parsed)
