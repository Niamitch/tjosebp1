import sys

class ProverbeCompletor:

    grammes = {}

    def __init__(self, corpus, n_gramme=1):
        self.__create_model(corpus, n_gramme)

    def __create_model(self, corpus, n_gramme):
        pass

    def complete(self, incomplete_proverbe, candidate_words):
        pass

def main(argv):
    corpus = open('./resources/proverbes.txt')
    proverbe_completor = ProverbeCompletor(corpus, 2)
    returned_proverbe = proverbe_completor.complete("a beau mentir qui *** de loin", ["vient", "part", "mange", "programme"])
    print(returned_proverbe)



if __name__ == "__main__":
   main(sys.argv[1:])