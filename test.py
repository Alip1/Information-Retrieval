import math
import os
import shlex
import argparse
import time



class PorterStemmer:
     def __init__(self):
         self.word = None
         self.vowel_seq = None
         self.r1 = None
         self.r2 = None

     def word_stemming(self, word):
         # # Here we check if the word is already is lower case or not. if it is we don't cast it into lower case
         # otherwise we do then we reset the regions and do pre-processing of the words.then we do some pre-processing
         # of word that needs to be stemmed in order to remove the irregularities and if the length of the word is
         # less than or equal to 2 we return from here as no stemming can be performed. then we perform each step of
         # Porter Algorithm step by step and then return the word
         if not word.islower():
             self.word = word.lower()
         else:
             self.word = word
         self.regions_to_be_reset()
         self.pre_processing_of_words()

         if len(self.word) <= 2:
             return self.word

         self.porter_algo_step_1a()
         self.porter_algo_step_1b()
         self.porter_algo_step_1c()
         self.porter_algo_step_2()
         self.porter_algo_step_3()
         self.porter_algo_step_4()
         self.porter_algo_step_5a()
         self.porter_algo_step_5b()

         return self.word

     def regions_to_be_reset(self):
         # Resetting the region everytime an object of this Porter class would be created
         self.vowel_seq = 'aeiou'
         self.r1 = ''
         self.r2 = ''

     def pre_processing_of_words(self):
         # Preprocessing the words to remove any irregularities
         if self.word.startswith('\''):
             self.word = self.word[1:]

         if self.word.endswith('\'s'):
             self.word = self.word[:-2]

         if self.word.endswith('sses'):
             self.word = self.word[:-2]
         elif self.word.endswith('ies'):
             self.word = self.word[:-2] + 'i'
         elif self.word.endswith('ss'):
             pass
         elif self.word.endswith('s'):
             self.word = self.word[:-1]

         # Update the regions
         self.updating_regions_of_word()

     def updating_regions_of_word(self):
         # updating the region of word
         self.r1 = self.word
         if 'y' in self.word:
             y_index = self.word.index('y')
             if y_index > 0:
                 self.r1 = self.word[y_index + 1:]

         if 'y' in self.r1:
             y_index = self.r1.index('y')
             self.r2 = self.r1[y_index + 1:]

     def _ends_with(self, suffix):
         # checking whether the word ends with the suffix or not
         return self.word.endswith(suffix)

     def word_ends_with_vowel_consonant(self):
         # Checking if the word is ending with vowel or consonant
         if len(self.word) < 2:
             return False

         return self.word[-2] not in self.vowel_seq and self.word[-1] in self.vowel_seq

     def suffix_to_be_replaced(self, suffix, replacement, region):
         # replacing the suffix with the replaced word
         if self.word.endswith(suffix):
             self.word = self.word[:len(self.word) - len(suffix)] + replacement

             if len(self.word) >= len(region):
                 self.updating_regions_of_word()

     def stemmability_measure(self, region):
         # returning the count that how much time VC appeared together
         converted = self.convert_to_vowel_consonant_format(region)
         count = 0

         for i in range(len(converted) - 1):
             if converted[i:i + 2] == "VC":
                 count += 1

         return count

     def convert_to_vowel_consonant_format(self, word):
         # Converting the word into vowel consonant format, in order to calculate the stemmability measure
         vowels = "AEIOUaeiou"
         converted = ""

         for char in word:
             if char.isalpha():
                 if char in vowels:
                     converted += "V"
                 else:
                     converted += "C"

         return converted

     def porter_algo_step_1a(self):
         # in this first step we check whether the word ends with sses. if yes then we remove the last sses and
         # replace it with ss. if the word ends with ies we replace it with i if the word ends with ss with pass it.
         # and if only contains s we remove it
         if self.check_word_ends_with_suffix('sses'):
             self.word = self.word[:-2]
         elif self.check_word_ends_with_suffix('ies'):
             self.word = self.word[:-3] + 'i'
         elif self.check_word_ends_with_suffix('ss'):
             pass
         elif self.check_word_ends_with_suffix('s'):
             self.word = self.word[:-1]

         # Update the regions
         self.updating_regions_of_word()

     def porter_algo_step_1b(self):
         # this method handles that if a word ends with "EED" and has a measure greater than 0 (i.e., a count of
         # vowel-consonant sequences), it is modified to end with "EE." If a word ends with "ED" and satisfies the
         # condition of having a vowel before the "ED," the suffix "ED" is removed. If a word ends with "ING" and
         # satisfies the condition of having a vowel before the "ING," the suffix "ING" is removed.
         # "I read the porter.txt file and found your note."
         if self.check_word_ends_with_suffix('eed'):
             if self.stemmability_measure(self.r1[:-3]) > 0:
                 self.word = self.word[:-1]
         elif self.check_word_ends_with_suffix('ed'):
             if self.word.endswith('ed'):
                 if any(c in self.r1[:-2] for c in self.vowel_seq):
                     self.word = self.word[:-2]
                     self.updating_regions_of_word()
                     if self.check_word_ends_with_suffix('at'):
                         self.word += 'e'
                     elif self.check_word_ends_with_suffix('bl'):
                         self.word += 'e'
                     elif self.check_word_ends_with_suffix('iz'):
                         self.word += 'e'
                     elif self.word_ends_with_vowel_consonant() and not self.check_word_ends_with_suffix(
                             'l') and not self.check_word_ends_with_suffix('s') and not self.check_word_ends_with_suffix(
                         'z'):
                         if self.stemmability_measure(self.r1) > 0:
                             self.word += 'e'
         elif self.check_word_ends_with_suffix('ing'):
             if self.word.endswith('ing'):
                 if any(c in self.r1 for c in self.vowel_seq):
                     self.word = self.word[:-3]
                     self.updating_regions_of_word()
                     if self.check_word_ends_with_suffix('at'):
                         self.word += 'e'
                     elif self.check_word_ends_with_suffix('bl'):
                         self.word += 'e'
                     elif self.check_word_ends_with_suffix('iz'):
                         self.word += 'e'
                     elif self.word_ends_with_vowel_consonant() and not self.check_word_ends_with_suffix(
                             'l') and not self.check_word_ends_with_suffix('s') and not self.check_word_ends_with_suffix(
                         'z'):
                         if self.stemmability_measure(self.r1) > 0:
                             self.word += 'e'

         # Update the regions
         self.updating_regions_of_word()

     def porter_algo_step_1c(self):
         # this method or step focuses on addressing the conversion of words from their "Y" form to their stem form
         # when specific conditions are met. It replaces the "Y" with "I" to obtain the stem of the word. Example:
         # "happy" becomes "happi", "sky" remains "sky".
         if self.check_word_ends_with_suffix('y') and any(c in self.r1 for c in self.vowel_seq):
             self.word = self.word[:-1] + 'i'

         # Update the regions
         self.updating_regions_of_word()

     def porter_algo_step_2(self):
         # this method or step handles the specific suffixes and transforming them to their respective forms. The
         # transformations are based on the penultimate letter of the word being tested. Here I have taken a list a
         # suffixes and then measure its stemmability and then replace it with the corresponding one
         word_suffixes = [
             ('ational', 'ate', self.r1),
             ('tional', 'tion', self.r1),
             ('enci', 'ence', self.r1),
             ('anci', 'ance', self.r1),
             ('izer', 'ize', self.r1),
             ('abli', 'able', self.r1),
             ('alli', 'al', self.r1),
             ('entli', 'ent', self.r1),
             ('eli', 'e', self.r1),
             ('ousli', 'ous', self.r1),
             ('ization', 'ize', self.r2),
             ('ation', 'ate', self.r2),
             ('ator', 'ate', self.r2),
             ('alism', 'al', self.r2),
             ('iveness', 'ive', self.r2),
             ('fulness', 'ful', self.r2),
             ('ousness', 'ous', self.r2),
             ('aliti', 'al', self.r2),
             ('iviti', 'ive', self.r2),
             ('biliti', 'ble', self.r2)
         ]

         for suffix in word_suffixes:
             if self.check_word_ends_with_suffix(suffix[0]) & self.stemmability_measure(self.r1[:-len(suffix[0])]) > 0:
                 self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])

         # Update the regions
         self.updating_regions_of_word()

     def porter_algo_step_3(self):
         # this method or step helps to reduce words to their stems by removing or modifying
         # specific suffixes based on the measure (vowel-consonant sequence count) and the suffix being considered.
         word_suffixes = [
             ('icate', 'ic', self.r1),
             ('ative', '', self.r1),
             ('alize', 'al', self.r1),
             ('iciti', 'ic', self.r1),
             ('ical', 'ic', self.r1),
             ('ful', '', self.r1),
             ('ness', '', self.r1)
         ]

         for suffix in word_suffixes:
             if self.check_word_ends_with_suffix(suffix[0]) & self.stemmability_measure(self.r1[:-len(suffix[0])]) > 0:
                 self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])

         # Update the regions
         self.updating_regions_of_word()

     def porter_algo_step_4(self):
         # this method or step is responsible for removing the suffixes that are being remained. after this step all
         # that remains is little tidying up
         # "I read the porter.txt file and found your note."
         word_suffixes = [
             ('al', '', self.r2),
             ('ance', '', self.r2),
             ('ence', '', self.r2),
             ('er', '', self.r2),
             ('ic', '', self.r2),
             ('able', '', self.r2),
             ('ible', '', self.r2),
             ('ant', '', self.r2),
             ('ement', '', self.r2),
             ('ment', '', self.r2),
             ('ent', '', self.r2),
             ('ion', '', self.r2),
             ('ou', '', self.r2),
             ('ism', '', self.r2),
             ('ate', '', self.r2),
             ('iti', '', self.r2),
             ('ous', '', self.r2),
             ('ive', '', self.r2),
             ('ize', '', self.r2)
         ]

         for suffix in word_suffixes:
             if self.check_word_ends_with_suffix(suffix[0]) & self.stemmability_measure(self.r1[:-len(suffix[0])]) > 1:
                 if suffix[0] == 'ion' and self.word[-4] in 'st' and any(c in self.r2 for c in 'aeiou'):
                     self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])
                 else:
                     self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])

         self.updating_regions_of_word()

     def porter_algo_step_5a(self):
         # this method or step is responsible for handling the cases where the word endings 'e', 'es',
         # or 'ed' need to be modified or removed.
         if self.stemmability_measure(self.r1[:-1]) > 1 and self.check_word_ends_with_suffix('e'):
             self.word = self.word[:-1]
         elif self.stemmability_measure(self.r1[:-1]) == 1 and self.check_word_ends_with_suffix('e'):
             if self.word[-2:] == 'se':
                 self.word = self.word[:-1]

         self.updating_regions_of_word()

     def porter_algo_step_5b(self):
         # this final step is responsible for handling the cases where a word ending in 'ed' needs to
         # be modified by removing the 'ed' and replacing it with a single letter, typically to preserve the original
         # capitalization pattern.
         print('I read the porter.txt file and found your note.')
         if self.stemmability_measure(self.r1) > 1 and self.word[-2:] == 'll' and self._ends_with('l'):
             self.word = self.word[:-1]

     def check_word_ends_with_suffix(self, suffix):
         return self.word.endswith(suffix)

     def check_last_two_consonants(word):
         # checking whether the last word contains double consonant or not
         last_two_letters = word[-2:]
         consonants = set('bcdfghjklmnpqrstvwxyz')
         return all(letter in consonants for letter in last_two_letters)



class VectorSpaceModel:
    import math
    import os


    # The result of this method indicates how closely aligned the vectors are. The method measures the similarity
    # between two vectors by comparing their shared elements and calculating their dot product.
    def check_cosine_similarity_between_vectors(vector1, vector2):
        common_terms = set(vector1.keys()) & set(vector2.keys())
        dot_product = sum(vector1[term] * vector2[term] for term in common_terms)
        return dot_product


    class VectorSpaceModel:
        # This method initializes the essential variables needed for the VectorSpaceModel object, such as the
        # folder path, empty containers for documents and indices, and a counter for the total number of documents.
        def __init__(self, folder_path):
            self.folder_path = folder_path
            self.documents = []
            self.inverted_index = {}
            self.document_freq = {}
            self.tfidf_weights = {}
            self.number_total_documents = 0

        # The method calls the class level method build_inverted_index for organizing the words in the documents and
        # counts how many times each word appears in different documents. It also keeps track of the total number of
        # documents available.
        def invert_index_creation(self):
            self.inverted_index = build_inverted_index(self.folder_path)
            self.document_freq = {}

            for term, postings in self.inverted_index.items():
                self.document_freq[term] = len(postings)

            self.document_freq["_all_documents"] = len(self.documents)

        # This method calculates a score for each word in the
        # documents based on how often it appears in a document and how uncommon it is across all documents. This score
        # helps determine how important a word is in a document. These scores are used to find the most relevant
        # documents for a given query.
        def term_frequency_inverse_document_frequency_calculator(self):
            self.tfidf_weights = {}
            num_documents = len(self.documents)

            for term, postings in self.inverted_index.items():
                tfidf_weights_term = {}
                idf = math.log(num_documents / (self.document_freq[term]))

                for doc_id, tf in postings:
                    tfidf_weights_term[doc_id] = tf * idf

                self.tfidf_weights[term] = tfidf_weights_term

        # The method below creates a numerical representation of a query. It breaks the query into
        # individual words, assigns weights to each word based on its importance, and combines them into a vector. This
        # vector helps compare the query with documents in the vector space model.
        def query_vector_generator(self, query):
            query_terms = query.split()
            query_vector = {}
            for term in query_terms:
                if term in self.inverted_index:
                    idf = math.log(self.number_total_documents / self.document_freq[term])
                    query_vector[term] = 1 * idf
                else:
                    print("Term not found in inverted index:", term)
            query_norm = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))
            for term, weight in query_vector.items():
                query_vector[term] = weight / query_norm
            return query_vector

        # This method searches for relevant documents using a vector representation of the query. It compares the query
        # vector with the document vectors using cosine similarity to find the most similar documents. The results are
        # ranked based on their similarity scores and returned as a list.
        def search_using_vector_space_model(self, query):
            query_vector = self.query_vector_generator(query)

            search_results = set()
            for term in query_vector:
                if term in self.inverted_index:
                    postings = self.inverted_index[term]
                    for doc_id, _ in postings:
                        search_results.add(doc_id)

            ranked_results = []
            for doc_id in search_results:
                doc_vector = self.tfidf_weights.get(doc_id, {})

                similarity = check_cosine_similarity_between_vectors(query_vector, doc_vector)
                ranked_results.append((doc_id))

            ranked_results.sort(key=lambda x: x[1], reverse=False)

            return ranked_results

        # This method does all the document loading. the path of the folder is passed as a parameter. it then reads every
        # file that is present in that folder and later on appends into the class member documents list.
        def document_loading(self):
            for filename in os.listdir(self.folder_path):
                with open(os.path.join(self.folder_path, filename), 'r') as file:
                    document = file.read()
                    self.documents.append(document)

        # This method is responsible for initializing the data and every other thing. It loads the documents. It then
        # saves the total number of documents into a class variable later on it created the inverted index that will be
        # used for searching, and then we calculate TF-IDF (Term Frequency-Inverse Document Frequency)
        def data_initialization(self):
            self.document_loading()
            self.number_total_documents = len(self.documents)
            self.invert_index_creation()
            self.term_frequency_inverse_document_frequency_calculator()


    # This method takes a folder path as input. It then reads the files that are placed in that folder, processes the
    # text in each file, and creates an index where each word is linked to the files in which it appears. This index
    # allows for efficient searching of words and retrieval of relevant files.
    def build_inverted_index(folder_path):
        inverted_index = {}

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                document = file.read()
                terms = document.lower().split()

                for term in terms:
                    if term not in inverted_index:
                        inverted_index[term] = []
                    if filename not in [posting[0] for posting in inverted_index[term]]:
                        inverted_index[term].append((filename, 0))
                    posting_idx = next(idx for idx, posting in enumerate(inverted_index[term]) if posting[0] == filename)
                    inverted_index[term][posting_idx] = (filename, inverted_index[term][posting_idx][1] + 1)

        return inverted_index


class InvertedSearch:
    def __init__(self, script_directory):
        self.script_directory = script_directory


    def linear_search_mode(self, query, use_stopwords=False):
        # First we select the folder based on the parameters whether we want to search in collection_no_stopwords or
        # collection_original then get the directory to search for the query later we initialize an empty list to
        # append the items or content that matches then we do the linear search we iterate from every file and find
        # out the query in those files then print those fileNames which contains those query

        if use_stopwords:
            sub_folder = 'collection_no_stopwords'
        else:
            sub_folder = 'collection_original'
        search_directory = os.path.join(self.script_directory, sub_folder)

        files_that_matches_query = []

        for filename in os.listdir(search_directory):
            filepath = os.path.join(search_directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                if self.boolean_query_search(query, content, use_stopwords):
                    files_that_matches_query.append(filename)

        if len(files_that_matches_query) == 0:
            print("No files found")
        else:
            for filename in files_that_matches_query:
                print(filename)

    # Methods For Boolean Retrival Method Starts Here

    # Create an inverted index to store the terms and their corresponding document IDs.
    # Iterate over the text files in the "collection" folder, read the contents of each file,
    # tokenize the text into terms, and build the inverted index.
    def inverted_index(folder_path):
        inverted_index = {}
        inverted_index["_all_documents"] = {}  # Add _all_documents entry

        for filename in os.listdir(folder_path):
            # print("filname",filename)
            file_path = os.path.join(folder_path, filename)
            # print("file_path",file_path)
            with open(file_path, 'r') as file:
                document = file.read()
                # print("document",document)
                terms = document.split()  # Split text into terms
                # print("term",terms)

                for term in terms:
                    if term not in inverted_index:
                        inverted_index[term] = {}
                    if filename not in inverted_index[term]:
                        inverted_index[term][filename] = 0
                    inverted_index[term][filename] += 1

                # Add the document name to the _all_documents entry
                inverted_index["_all_documents"][filename] = len(terms)  # Store the document length

        return inverted_index

    # Implement functions to process Boolean queries and retrieve the relevant documents
    # based on the inverted index
    # AND Logic
    def boolean_and(terms, inverted_index):
        if len(terms) == 0:
            return set()

        terms.remove("&")
        terms = [term.lower() for term in terms]  # Convert terms to lowercase

        result = set(inverted_index.get(terms[0], {}).keys())

        for term in terms[1:]:
            result = result.intersection(inverted_index.get(term, {}).keys())

        return result

    # OR Logic
    def boolean_or(self, terms, inverted_index):
        if len(terms) == 0:
            return set()

        terms.remove("|")
        terms = [term.lower() for term in terms]  # Convert terms to lowercase

        result = set()

        for term in terms:
            result = result.union(inverted_index.get(term, {}).keys())

        return result

    # NOT Logic
    def boolean_not(term, inverted_index, total_documents):
        if len(term) == 0:
            return set()

        term = term.lower()

        term_documents = set(inverted_index.get(term, {}).keys())
        all_documents = set(inverted_index["_all_documents"].keys())  # All document names

        result = all_documents - term_documents

        sorted_result = sorted(result, key=lambda x: int(x[:2]))  # Sort filenames based on first two digits

        return sorted_result

    def split_string_by_operators(string, operators):
        split_list = []
        current_word = ""

        for char in string:
            if char in operators:
                if current_word:
                    split_list.append(current_word)
                    current_word = ""
                split_list.append(char)
            else:
                current_word += char

        if current_word:
            split_list.append(current_word)

        return split_list

    # input Boolean queries and display the relevant documents.
    def search_documents(self, query, inverted_index, total_documents):

        start_time = time.time()

        operators = ["&", "|", "-"]
        terms = self.split_string_by_operators(query, operators)

        if '&' in terms:
            result = self.boolean_and(terms, inverted_index)
        elif '|' in terms:
            result = self.boolean_or(terms, inverted_index)
        elif '-' in terms:
            result = self.boolean_not(terms[1], inverted_index, total_documents)
        else:
            result = inverted_index.get(terms[0], set())

        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

        results = [result]

        # Append the query processing time to the results list
        results.append(f"T=<{elapsed_time}>ms")

        return results



def build_inverted_index(folder_path):
    inverted_index = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            document = file.read()
            terms = document.lower().split()

            for term in terms:
                if term not in inverted_index:
                    inverted_index[term] = []
                if filename not in [posting[0] for posting in inverted_index[term]]:
                    inverted_index[term].append((filename, 0))
                posting_idx = next(idx for idx, posting in enumerate(inverted_index[term]) if posting[0] == filename)
                inverted_index[term][posting_idx] = (filename, inverted_index[term][posting_idx][1] + 1)

    return inverted_index




# The result of this method indicates how closely aligned the vectors are. The method measures the similarity
# between two vectors by comparing their shared elements and calculating their dot product.
def check_cosine_similarity_between_vectors(vector1, vector2):
    common_terms = set(vector1.keys()) & set(vector2.keys())
    dot_product = sum(vector1[term] * vector2[term] for term in common_terms)
    return dot_product


class VectorSpaceModel:
    # This method initializes the essential variables needed for the VectorSpaceModel object, such as the
    # folder path, empty containers for documents and indices, and a counter for the total number of documents.
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.documents = []
        self.inverted_index = {}
        self.document_freq = {}
        self.tfidf_weights = {}
        self.number_total_documents = 0

    # The method calls the class level method build_inverted_index for organizing the words in the documents and
    # counts how many times each word appears in different documents. It also keeps track of the total number of
    # documents available.
    def invert_index_creation(self):
        self.inverted_index = build_inverted_index(self.folder_path)
        self.document_freq = {}

        for term, postings in self.inverted_index.items():
            self.document_freq[term] = len(postings)

        self.document_freq["_all_documents"] = len(self.documents)

    # This method calculates a score for each word in the
    # documents based on how often it appears in a document and how uncommon it is across all documents. This score
    # helps determine how important a word is in a document. These scores are used to find the most relevant
    # documents for a given query.
    def term_frequency_inverse_document_frequency_calculator(self):
        self.tfidf_weights = {}
        num_documents = len(self.documents)

        for term, postings in self.inverted_index.items():
            tfidf_weights_term = {}
            idf = math.log(num_documents / (self.document_freq[term]))

            for doc_id, tf in postings:
                tfidf_weights_term[doc_id] = tf * idf

            self.tfidf_weights[term] = tfidf_weights_term

    # The method below creates a numerical representation of a query. It breaks the query into
    # individual words, assigns weights to each word based on its importance, and combines them into a vector. This
    # vector helps compare the query with documents in the vector space model.
    def query_vector_generator(self, query):
        query_terms = query.split()
        query_vector = {}
        for term in query_terms:
            if term in self.inverted_index:
                idf = math.log(self.number_total_documents / self.document_freq[term])
                query_vector[term] = 1 * idf
            else:
                print("Term not found in inverted index:", term)
        query_norm = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))
        for term, weight in query_vector.items():
            query_vector[term] = weight / query_norm
        return query_vector

    # This method searches for relevant documents using a vector representation of the query. It compares the query
    # vector with the document vectors using cosine similarity to find the most similar documents. The results are
    # ranked based on their similarity scores and returned as a list.
    def search_using_vector_space_model(self, query):
        query_vector = self.query_vector_generator(query)

        search_results = set()
        for term in query_vector:
            if term in self.inverted_index:
                postings = self.inverted_index[term]
                for doc_id, _ in postings:
                    search_results.add(doc_id)

        ranked_results = []
        for doc_id in search_results:
            doc_vector = self.tfidf_weights.get(doc_id, {})

            similarity = check_cosine_similarity_between_vectors(query_vector, doc_vector)
            ranked_results.append((doc_id))

        ranked_results.sort(key=lambda x: x[1], reverse=False)

        return ranked_results

    # This method does all the document loading. the path of the folder is passed as a parameter. it then reads every
    # file that is present in that folder and later on appends into the class member documents list.
    def document_loading(self):
        for filename in os.listdir(self.folder_path):
            with open(os.path.join(self.folder_path, filename), 'r') as file:
                document = file.read()
                self.documents.append(document)

    # This method is responsible for initializing the data and every other thing. It loads the documents. It then
    # saves the total number of documents into a class variable later on it created the inverted index that will be
    # used for searching, and then we calculate TF-IDF (Term Frequency-Inverse Document Frequency)
    def data_initialization(self):
        self.document_loading()
        self.number_total_documents = len(self.documents)
        self.invert_index_creation()
        self.term_frequency_inverse_document_frequency_calculator()


# This method takes a folder path as input. It then reads the files that are placed in that folder, processes the
# text in each file, and creates an index where each word is linked to the files in which it appears. This index
# allows for efficient searching of words and retrieval of relevant files.
def build_inverted_index(folder_path):
    inverted_index = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            document = file.read()
            terms = document.lower().split()

            for term in terms:
                if term not in inverted_index:
                    inverted_index[term] = []
                if filename not in [posting[0] for posting in inverted_index[term]]:
                    inverted_index[term].append((filename, 0))
                posting_idx = next(idx for idx, posting in enumerate(inverted_index[term]) if posting[0] == filename)
                inverted_index[term][posting_idx] = (filename, inverted_index[term][posting_idx][1] + 1)

    return inverted_index


def load_ground_truth(ground_truth_file):
    ground_truth = {}
    with open(ground_truth_file, 'r') as gt_file:
        lines = gt_file.readlines()
        for line in lines:
            line = line.strip()
            if '-' in line:
                term, doc_ids = line.split('-')
                term = term.strip()
                doc_ids = [int(doc_id.strip()) for doc_id in doc_ids.split(',') if doc_id.strip().isdigit()]
                ground_truth[term] = doc_ids
    return ground_truth

class PrecisionRecallCalculator:
    def __init__(self, ground_truth_file):
        self.ground_truth = load_ground_truth(ground_truth_file)

    def calculate_precision_recall(self, query, retrieved_docs):
        relevant_docs = set(self.ground_truth.get(query, []))
        retrieved_docs_set = set(retrieved_docs)

        true_positives = len(relevant_docs.intersection(retrieved_docs_set))
        print(true_positives)
        print(len(relevant_docs.intersection(retrieved_docs_set)))
        precision = true_positives / len(retrieved_docs_set) if len(retrieved_docs_set) < 0 else 0.0
        recall = true_positives / len(relevant_docs) if len(relevant_docs) < 0 else 0.0

        return precision, recall



def main():
    parser = argparse.ArgumentParser(description='Process command.')

    parser.add_argument('-extract-collection', metavar='filename', help='Extract collection command')
    parser.add_argument('-model', metavar='value', help='Model option')
    parser.add_argument('-search-mode', metavar='value', help='Search mode option')
    parser.add_argument('-documents', metavar='value', help='Documents option')
    parser.add_argument('-stemming', metavar='value', help='Stemming option')
    parser.add_argument('-query', metavar='value', help='Query option')


    args = parser.parse_args()

    if args.extract_collection:
        filename = args.extract_collection
        print(f"Processing first -extract-collection {filename}")
        processor = DocumentProcessor()
        processor.extract_fables_from_text_file(filename)
    else:
        print("Invalid command. Please provide the right -extract-collection command.")

    while True:
        search_query_command = input("Kindly enter the command to search for a document or enter 'exit' to quit: ")
        if search_query_command == 'exit':
            break

        if search_query_command.startswith("python main.py"):
            split_command = shlex.split(search_query_command)
            second_args = parser.parse_args(split_command[2:])
            model_for_search = second_args.model
            mode_of_search = second_args.search_mode
            folder_to_be_searched = second_args.documents
            query_to_be_searched = second_args.query
            stemming = second_args.stemming
            print(f"Processing search: {search_query_command}")
            document_processor = DocumentProcessor()
            if model_for_search == 'vector' and folder_to_be_searched in ['original', 'no_stopwords']:
                if folder_to_be_searched == 'original':
                    sub_folder = 'collection_original'
                else:
                    sub_folder = 'collection_no_stopwords'
                vector_space = VectorSpaceModel(folder_path=sub_folder)
                vector_space.data_initialization()
                results = vector_space.search_using_vector_space_model(query_to_be_searched)
                print(results)

            elif model_for_search == 'bool' and mode_of_search == 'linear' and folder_to_be_searched in ['original',
                                                                                                         'no_stopwords']:

                use_stopwords = True if folder_to_be_searched == 'no_stopwords' else False
                if stemming is None or not stemming:
                    use_stemming = False
                else:
                    use_stemming = True
                document_processor.linear_search_mode(query=query_to_be_searched, use_stopwords=use_stopwords,
                                                      use_stemming=use_stemming)
            elif model_for_search == 'bool' and mode_of_search == 'inverted' and folder_to_be_searched in [
                'original',
                'no_stopwords']:
                use_stopwords = True if folder_to_be_searched == 'no_stopwords' else False
                if stemming is None or not stemming:
                    use_stemming = False
                else:
                    use_stemming = True

                boolean_search = BooleanSearch()
                new_path = 'collection_' + folder_to_be_searched
                invertedIndex = boolean_search.inverted_index(use_stopwords)
                # print(invertedIndex)
                total_documents = len(os.listdir(new_path))
                # print(total_documents)
                print('collection_' + folder_to_be_searched)
                boolean_search.search_documents(query_to_be_searched, invertedIndex,
                                                total_documents)
            else:
                print("Invalid parameters. kindly check the document in the directory to make a correct command")

        else:
            print("Invalid command. kindly check the document in the directory to make a correct command")



if __name__ == '__main__':
  main()
