import sys
import nltk
nltk.download('punkt')

class ProverbeCompletor:

    PROVERBE_LANGUAGE = "french"

    nb_of_words_in_corpus = 0
    grammes = {}
    historical_grammes = {}

    def __init__(self, corpus, n_gramme=1):
        self.__create_model(corpus, n_gramme)

    def __create_model(self, corpus, n_gramme):
        self.grammes = self.__calculate_n_gramme_occurence(corpus, n_gramme)
        if n_gramme > 1:
            self.historical_grammes = self.__calculate_n_gramme_occurence(corpus, n_gramme - 1)
        self.__calculate_nb_of_words_in_corpus(corpus)

    def __calculate_nb_of_words_in_corpus(self, corpus):
        for proverbe in corpus:
            tokenized_proverbe = nltk.word_tokenize(proverbe, self.PROVERBE_LANGUAGE)
            self.nb_of_words_in_corpus = self.nb_of_words_in_corpus + len(tokenized_proverbe)

    def __calculate_n_gramme_occurence(self, corpus, n_gramme):
        grammes = {}
        for proverbe in corpus:
            tokenized_proverbe = nltk.word_tokenize(proverbe, self.PROVERBE_LANGUAGE)
            if len(tokenized_proverbe) >= n_gramme:
                for word_index in range(len(tokenized_proverbe) - 1):
                    gramme = tuple(tokenized_proverbe[word_index + tuple_index] for tuple_index in range(n_gramme))
                    if gramme not in grammes:
                        grammes[gramme] = 1
                    else:
                        grammes[gramme] = grammes[gramme] + 1
        return grammes

    def complete(self, incomplete_proverbe, candidate_words):
        pass

def main(argv):
    corpus = open('./resources/proverbes.txt')
    proverbe_completor = ProverbeCompletor(corpus, 2)
    returned_proverbe = proverbe_completor.complete("a beau mentir qui *** de loin", ["vient", "part", "mange", "programme"])
    print(returned_proverbe)



if __name__ == "__main__":
   main(sys.argv[1:])