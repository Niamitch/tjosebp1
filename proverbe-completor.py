# -*- coding: utf-8 -*-
import sys
import nltk
import numpy as np
import io
import math
nltk.download('punkt')

class ProverbeCompletor:

    PROVERBE_LANGUAGE = "french"
    UNKNOWN_SEQUENCE = "***"

    nb_of_words_in_corpus = 0
    grammes = {}
    delta_value = 0
    backoff_constant = 0


    def __init__(self, corpus, probability_function, n_gramme=1, delta=1.0, backoff=0.4,):
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

    def calculate_probability(self,tuple,probabilities):
        grammeLength = len(tuple)
        if grammeLength == 1:
            probabilities.append(self.grammes[grammeLength][tuple]/ float(self.nb_of_words_in_corpus))
        elif tuple in self.grammes[grammeLength] and tuple[:grammeLength-1] in self.grammes[grammeLength-1]:
            probabilities.append(self.grammes[grammeLength][tuple]/self.grammes[grammeLength-1][tuple[:grammeLength-1]])
            self.calculate_probability(tuple[:grammeLength - 1],probabilities)
        else:
            probabilities.append(0)
        return probabilities

    def calculate_probability_with_delta(self,tuple,probabilities):
        grammeLength = len(tuple)
        if grammeLength == 1:
            probabilities.append((self.grammes[grammeLength][tuple]+self.delta_value) / float(len(self.grammes[grammeLength])*self.delta_value+self.nb_of_words_in_corpus))
        else:
            initial_probabiblity = self.grammes[grammeLength][tuple] if tuple in self.grammes[grammeLength] else 0
            initial_probability_historical = self.grammes[grammeLength - 1][tuple[:grammeLength - 1]] if tuple[:grammeLength - 1] in self.grammes[grammeLength - 1] else 0
            probabilities.append(
                (initial_probabiblity+self.delta_value) / (len(self.grammes[grammeLength])*self.delta_value+initial_probability_historical))
            self.calculate_probability_with_delta(tuple[:grammeLength - 1], probabilities)
        return probabilities

    def complete(self, incomplete_proverbe, candidate_words, n_gramme):
        last_proverbe_words = nltk.word_tokenize(incomplete_proverbe.split(self.UNKNOWN_SEQUENCE)[0], self.PROVERBE_LANGUAGE)[-(n_gramme-1):]
        historic_proverbe_part = tuple(last_proverbe_words)
        best_candiate = None
        best_candidate_probability = 0
        best_candidate_tuple = None
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
                    best_candidate_tuple = proverbe_part
            else:
                if (candidate_word,) in self.grammes[n_gramme]:
                    probability = self.grammes[n_gramme][(candidate_word,)] / float(self.nb_of_words_in_corpus)
                if probability >= best_candidate_probability:
                    best_candidate_probability = probability
                    best_candiate = candidate_word
                    best_candidate_tuple = (candidate_word,)
        completed_proverbe = incomplete_proverbe.replace(self.UNKNOWN_SEQUENCE, best_candiate, 1)
        perplexity = self.calculate_perplexity(best_candidate_tuple)
        should_be_ignore_for_perplexity = False if perplexity >=1 else True
        if self.UNKNOWN_SEQUENCE in completed_proverbe:
            completed_proverbe, next_perplexity, next_should_be_ignore_for_perplexity = self.complete(completed_proverbe, candidate_words, n_gramme)
            return completed_proverbe, (next_perplexity + perplexity), should_be_ignore_for_perplexity or next_should_be_ignore_for_perplexity
        else:
            return completed_proverbe, perplexity, should_be_ignore_for_perplexity

    def calculate_perplexity(self, tuple):
        tuple_probability = self.probability_function(self, tuple)
        return tuple_probability ** (-1.0 / len(tuple)) if tuple_probability > 0 else 0

def execute_proverbe_completor_on_file(file, n_gramme, proverbe_completor, corpus):
    print("Executing proverbe completor on file " + file + " using a model trained with " + str(n_gramme) + " grammes.")
    nb_correct_proverbe = 0
    perplexities = []
    with io.open(file, mode="r", encoding="utf-8") as file_content:
        for file_line in file_content:
            incomplet_proverbe = file_line.split(": ")[0].replace("{", "").replace("\"", "").replace(" }", "").lstrip().rstrip()
            if len(incomplet_proverbe) > 0:
                candidate_words = eval(file_line.split(": ")[1])
                if type(candidate_words) is tuple:
                    candidate_words = candidate_words[0]
                returned_proverbe, perplexity_sum, should_be_ignore_for_perplexity = proverbe_completor.complete(incomplet_proverbe, candidate_words, n_gramme)
                if not should_be_ignore_for_perplexity:
                    perplexity = perplexity_sum / incomplet_proverbe.count(proverbe_completor.UNKNOWN_SEQUENCE)
                    perplexities.append(perplexity)
                print(returned_proverbe + "  Candidat choice: " + str(candidate_words))
                corpus.seek(0)
                for corpus_line in corpus:
                    corpus_line = corpus_line.rstrip()
                    if corpus_line == returned_proverbe:
                        nb_correct_proverbe = nb_correct_proverbe + 1

    print("Number of correct proverbe: " + str(nb_correct_proverbe))
    print("Mean perplexity: " + str(np.mean(perplexities)))

def calculate_logprob(probabilities):
    return math.exp(np.sum(np.log10(probabilities)))

def calculate_probability_stupid_backoff(self, tuple):
    probability = 0
    grammeLength = len(tuple)
    if (grammeLength >= 1):
        if (grammeLength == 1 and tuple in self.grammes[grammeLength]):
            probability = self.grammes[grammeLength][tuple] / float(self.nb_of_words_in_corpus)
        else:
            historicalTuple = tuple[:grammeLength - 1]
            if historicalTuple in self.grammes[grammeLength -1]:
                probability = calculate_standard_probability(self,tuple)
            else:
                newTuple = tuple[1:]
                probability = self.backoff_constant * calculate_probability_stupid_backoff(self,newTuple)
    return probability

def calculate_probability_add_delta(self, tuple):
    return calculate_logprob(self.calculate_probability_with_delta(tuple,[]))


def calculate_standard_probability(self,tuple):
    return calculate_logprob(self.calculate_probability(tuple,[]))


def main(argv):
    # Parameters
    n_gramme = 3
    add_delta_value = 0.1
    backoff_constant = 0.1
    probability_function = calculate_standard_probability

    corpus = io.open('./resources/proverbes.txt', mode="r", encoding="utf-8")
    proverbe_completor = ProverbeCompletor(corpus, probability_function, n_gramme, add_delta_value, backoff_constant)
    execute_proverbe_completor_on_file("./resources/test2.txt", n_gramme, proverbe_completor, corpus)



if __name__ == "__main__":
   main(sys.argv[1:])