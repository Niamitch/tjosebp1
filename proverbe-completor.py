# -*- coding: utf-8 -*-
import sys
import nltk
import numpy as np
import io
nltk.download('punkt')

class ProverbeCompletor:

    PROVERBE_LANGUAGE = "french"
    UNKNOWN_SEQUENCE = "***"

    nb_of_words_in_corpus = 0
    grammes = {}
    historical_grammes = {}
    delta_value = 0
    backoff_constant = 0


    def __init__(self, corpus, probability_function, n_gramme=1, delta=1, backoff=0.4,):
        self.backoff_constant = backoff
        self.delta_value = delta
        self.probability_function = probability_function
        self.__create_model(corpus, n_gramme)


    def __create_model(self, corpus, n_gramme):
        self.grammes = self.__calculate_n_gramme_occurence(corpus, n_gramme)
        corpus.seek(0)
        self.__calculate_nb_of_words_in_corpus(corpus)

    def __calculate_nb_of_words_in_corpus(self, corpus):
        for proverbe in corpus:
            tokenized_proverbe = nltk.word_tokenize(proverbe, self.PROVERBE_LANGUAGE)
            self.nb_of_words_in_corpus = self.nb_of_words_in_corpus + len(tokenized_proverbe)

    def __calculate_n_gramme_occurence(self, corpus, n_gramme):
        grammes = {}
        for i in range(n_gramme):
            grammes[i+1] = {}
        for proverbe in corpus:
            tokenized_proverbe = nltk.word_tokenize(proverbe, self.PROVERBE_LANGUAGE)
            if len(tokenized_proverbe) >= n_gramme:
                for word_index in range(len(tokenized_proverbe)-1):
                    for i in range(1,n_gramme+1):
                        if word_index+i-1 < len(tokenized_proverbe):
                            gramme = tuple(tokenized_proverbe[word_index + tuple_index] for tuple_index in range(i))
                            if gramme not in grammes[i]:
                                grammes[i][gramme] = 1
                            else:
                                grammes[i][gramme] = grammes[i][gramme] + 1
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
                if proverbe_part in self.grammes[n_gramme] and historic_proverbe_part in self.grammes[n_gramme-1]:
                    probability = self.probability_function(self,proverbe_part)
                if probability >= best_candidate_probability:
                    best_candidate_probability = probability
                    best_candiate = candidate_word
            else:
                if (candidate_word,) in self.grammes[n_gramme]:
                    probability = self.grammes[n_gramme][(candidate_word,)] / float(self.nb_of_words_in_corpus)
                if probability >= best_candidate_probability:
                    best_candidate_probability = probability
                    best_candiate = candidate_word
        completed_proverbe = incomplete_proverbe.replace(self.UNKNOWN_SEQUENCE, best_candiate, 1)
        if self.UNKNOWN_SEQUENCE in completed_proverbe:
            return self.complete(completed_proverbe, candidate_words, n_gramme)
        else:
            return completed_proverbe

def execute_proverbe_completor_on_file(file, n_gramme, proverbe_completor):
    print("Executing proverbe completor on file " + file + " using a model trained with " + str(n_gramme) + " grammes.")
    with io.open(file, mode="r", encoding="utf-8") as file_content:
        for file_line in file_content:
            incomplet_proverbe = file_line.split(": ")[0].replace("{", "").replace("\"", "").replace(" }", "")
            if len(incomplet_proverbe) > 0:
                candidate_words = eval(file_line.split(": ")[1])
                if type(candidate_words) is tuple:
                    candidate_words = candidate_words[0]
                returned_proverbe = proverbe_completor.complete(incomplet_proverbe, candidate_words, n_gramme)
                print(returned_proverbe + "  Candidat choice: " + str(candidate_words))


def __calculate_probability_stupid_backoff(self, tuple):
    probability = 0
    grammeLength = len(tuple)
    if (grammeLength >= 1):
        if (grammeLength == 1 and tuple in self.grammes[grammeLength]):
            probability = self.grammes[grammeLength][tuple] / float(self.nb_of_words_in_corpus)
        else:
            historicalTuple = tuple[:grammeLength - 1]
            if historicalTuple in self.grammes[grammeLength]:
                probability = self.grammes[grammeLength][tuple] / float(self.grammes[grammeLength - 1][historicalTuple])
            else:
                newTuple = tuple[1:]
                probability = self.backoff_constant * __calculate_probability_stupid_backoff(self,newTuple)
    return probability


def __calculate_probability_add_delta(self, tuple):
    grammeLength = len(tuple)
    if (grammeLength == 1):
        probability = (self.grammes[grammeLength][tuple] + self.delta_value) / float(
            self.nb_of_words_in_corpus + (self.delta_value * len(self.grammes[grammeLength])))
    else:
        newTuple = tuple[1:]
        probability = (self.grammes[grammeLength][tuple] + self.delta_value) / float(
            self.grammes[grammeLength - 1][newTuple] + (self.delta_value * len(self.grammes[grammeLength])))

    return probability


def __calculate_standard_probability(self,tuple):
    grammeLength = len(tuple)
    historicalTuple = tuple[:grammeLength - 1]
    return self.grammes[grammeLength][tuple] / float(self.grammes[grammeLength - 1][historicalTuple])

def main(argv):
    n_gramme = 3
    add_delta_value = 1
    backoff_constant = 0.4
    corpus = io.open('./resources/proverbes.txt', mode="r", encoding="utf-8")
    proverbe_completor = ProverbeCompletor(corpus, __calculate_probability_stupid_backoff, n_gramme, add_delta_value, backoff_constant)
    execute_proverbe_completor_on_file("./resources/test2.txt", n_gramme, proverbe_completor)



if __name__ == "__main__":
   main(sys.argv[1:])