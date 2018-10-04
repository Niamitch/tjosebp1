import sys
import nltk
import numpy as np
nltk.download('punkt')

class ProverbeCompletor:

    PROVERBE_LANGUAGE = "french"
    UNKNOWN_SEQUENCE = "***"

    nb_of_words_in_corpus = 0
    grammes = {}
    historical_grammes = {}

    def __init__(self, corpus, n_gramme=1):
        self.__create_model(corpus, n_gramme)

    def __create_model(self, corpus, n_gramme):
        self.grammes = self.__calculate_n_gramme_occurence(corpus, n_gramme)
        if n_gramme > 1:
            corpus.seek(0)
            self.historical_grammes = self.__calculate_n_gramme_occurence(corpus, n_gramme - 1)
        corpus.seek(0)
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
                for word_index in range(len(tokenized_proverbe) - (n_gramme - 1)):
                    gramme = tuple(tokenized_proverbe[word_index + tuple_index] for tuple_index in range(n_gramme))
                    if gramme not in grammes:
                        grammes[gramme] = 1
                    else:
                        grammes[gramme] = grammes[gramme] + 1
        return grammes

    def complete(self, incomplete_proverbe, candidate_words, n_gramme):
        last_proverbe_words = nltk.word_tokenize(incomplete_proverbe.split(self.UNKNOWN_SEQUENCE)[0], self.PROVERBE_LANGUAGE)[-(n_gramme-1):]
        historic_proverbe_part = tuple(last_proverbe_words)
        best_candiate = None
        best_candidate_probability = 0
        for candidate_word in candidate_words:
            probability = 0
            if n_gramme > 1:
                copy_of_candidate_proverbe = np.append(last_proverbe_words,candidate_word)
                proverbe_part = tuple(copy_of_candidate_proverbe)
                if proverbe_part in self.grammes and historic_proverbe_part in self.historical_grammes:
                    probability = self.grammes[proverbe_part] / self.historical_grammes[historic_proverbe_part]
                if probability > best_candidate_probability:
                    best_candidate_probability = probability
                    best_candiate = candidate_word
            else:
                if (candidate_word,) in self.grammes:
                    probability = self.grammes[(candidate_word,)] / self.nb_of_words_in_corpus
                if probability > best_candidate_probability:
                    best_candidate_probability = probability
                    best_candiate = candidate_word
        return incomplete_proverbe.replace(self.UNKNOWN_SEQUENCE, best_candiate)

def main(argv):
    n_gramme = 3
    corpus = open('./resources/proverbes.txt')
    proverbe_completor = ProverbeCompletor(corpus, n_gramme)
    returned_proverbe = proverbe_completor.complete("a beau mentir qui *** de loin", ["vient", "part", "mange", "programme"], n_gramme)
    print(returned_proverbe)



if __name__ == "__main__":
   main(sys.argv[1:])