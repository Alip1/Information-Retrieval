import os
import time

from porter_stemmer import PorterStemmer


class BooleanSearch:
    # Methods For Boolean Retrival Method Starts Here

    # Create an inverted index to store the terms and their corresponding document IDs.
    # Iterate over the text files in the "collection" folder, read the contents of each file,
    # tokenize the text into terms, and build the inverted index.
    def inverted_index(folder_path, use_stopwords=False):
        if use_stopwords:
            folder_path = 'collection_no_stopwords'
        else:
            folder_path = 'collection_original'
        inverted_index = {"_all_documents": {}}

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
    def boolean_and(self, terms, inverted_index):
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
    def boolean_not(self, term, inverted_index, total_documents):
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
        results = []
        operators = ["&", "|", "!"]
        split_list = []
        current_word = ""

        for char in query:
            if char in operators:
                if current_word:
                    split_list.append(current_word)
                    current_word = ""
                split_list.append(char)
            else:
                current_word += char

        if current_word:
            split_list.append(current_word)

        if '&' in split_list:
            result = self.boolean_and(split_list, inverted_index)
        elif '|' in split_list:
            result = self.boolean_or(split_list, inverted_index)
        elif '!' in split_list:
            result = self.boolean_not(split_list[1], inverted_index, total_documents)
        else:
            result = inverted_index.get(split_list[0], set())

        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

        results.append(result)
        # Append the query processing time to the results list
        results.append(f"T={elapsed_time}ms")

        print("Relevant Documents:")
        for doc_id in results:
            print(doc_id)
