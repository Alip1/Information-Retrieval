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
