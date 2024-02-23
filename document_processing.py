import os
import re

from porter_stemmer import PorterStemmer

import time

from precision_recall_calculator import PrecisionRecallCalculator


def stops_words_removal(text, stop_words):
    # Removing punctuation and line breaks from text
    # Then converting them into lowerCase
    # after than splitting into separate words
    # filtering stop words out of separate words
    # later we are converting the words into a string and returning them
    text = re.sub(r'[^\w\s\']', '', text)
    text = text.lower()
    words = text.split()
    cleaned_words = [word for word in words if word not in stop_words]
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text


def boolean_query_search(query, content, use_stopwords=False, use_stemming=False):
    # Splitting the query as this one is for boolean model then later on checking if all query terms that are passed
    # are present in the content by doing Performing boolean retrieval if it is present true will be returned
    # otherwise false
    stemmer = PorterStemmer()
    if use_stemming:
        query = stemmer.word_stemming(query)
    query_to_be_searched = query.lower().split()
    if use_stopwords:
        with open('englishST.txt', 'r') as stopwords_file:
            stopwords = [word.strip() for word in stopwords_file]
        query_to_be_searched = stops_words_removal(query_to_be_searched, stopwords)

    content_terms = [stemmer.word_stemming(word) if use_stemming else word for word in content.lower().split()]
    for term in query_to_be_searched:
        if term not in content_terms:
            return False

    return True


class DocumentProcessor:
    def __init__(self):
        # This class is responsible for the processing for the documents initially we get the path for the script
        # After that we open that file and read the content from it. as we need to break down the whole content into
        # fables we are doing that fist, so we can get individual fables to be stored. then as we don't need the
        # introduction part and table of content, so we do that by only taking the content from the 2nd index As we
        # need to create 2 folders one for original fables and one for the ones without stop words we create an empty
        # list for stopwords and append the stop words we already have in englishST file after opening it and reading
        # data from it then after this we create a sub folder named as collection_original as it was asked we first
        # check whether it has been created before or not then we create it. Same goes for collection_no_stopwords we
        # need to create a separate sub folder for the fables after removing stopwords from them. and check if that
        # has been created already or not. Then we iterate through the fables we have read and take out the name and
        # text from them and store them into a separate folder. We then store it in the collection_original first and
        # later remove the stop words from those fables and save them into a separate folder named as
        # collection_no_stopwords

        self.script_directory = os.path.dirname(os.path.abspath(__file__))

    def extract_fables_from_text_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read()

        all_fables = content.split('\n\n\n\n')

        selected_fables = all_fables[2:]

        list_of_stop_words = []
        with open('englishST.txt', 'r') as stop_words_file:
            for stop_word in stop_words_file:
                list_of_stop_words.append(stop_word.strip())

        sub_folder_with_stop_words = os.path.join(self.script_directory, 'collection_original')
        if not os.path.exists(sub_folder_with_stop_words):
            os.makedirs(sub_folder_with_stop_words)

        sub_folder_without_stop_words = os.path.join(self.script_directory, 'collection_no_stopwords')
        if not os.path.exists(sub_folder_without_stop_words):
            os.makedirs(sub_folder_without_stop_words)

        for items_fables, single_fable in enumerate(selected_fables, start=1):
            lines_of_fable = single_fable.strip().split('\n')
            title_of_fable = lines_of_fable[0]
            text_of_fable = '\n'.join(lines_of_fable[3:])

            specific_fable_number = str(items_fables).zfill(2)
            specific_fable_name = title_of_fable.lower().replace(' ', '_').strip('_,\'')
            original_filename = f"{specific_fable_number}_{specific_fable_name}.txt"
            original_filepath = os.path.join(sub_folder_with_stop_words, original_filename)

            if not os.path.exists(original_filepath):
                with open(original_filepath, 'w') as f:
                    f.write(text_of_fable)

            text_without_stop_words = stops_words_removal(text_of_fable, list_of_stop_words)

            file_name_of_after_removing_stop_words = f"{specific_fable_number}_{specific_fable_name}.txt"
            filepath_without_stop_words = os.path.join(sub_folder_without_stop_words,
                                                       file_name_of_after_removing_stop_words)

            if not os.path.exists(filepath_without_stop_words):
                with open(filepath_without_stop_words, 'w') as f:
                    f.write(text_without_stop_words)

    def linear_search_mode(self, query, use_stopwords=False, use_stemming=False):
        # First we select the folder based on the parameters whether we want to search in collection_no_stopwords or
        # collection_original then get the directory to search for the query later we initialize an empty list to
        # append the items or content that matches then we do the linear search we iterate from every file and find
        # out the query in those files then print those fileNames which contains those query
        start_time = time.time()
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
                if boolean_query_search(query, content, use_stopwords, use_stemming):
                    files_that_matches_query.append(filename)

        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 2)
        if len(files_that_matches_query) == 0:
            print("No files found")
        else:
            for filename in files_that_matches_query:
                print(filename)
                print(elapsed_time)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        ground_truth_file = os.path.join(script_directory, 'groundtruth.txt')
        precision_recall_calculator = PrecisionRecallCalculator(ground_truth_file)
        precision, recall = precision_recall_calculator.calculate_precision_recall(query, files_that_matches_query)

        print(f"P={precision},R={recall},T={elapsed_time}ms")

