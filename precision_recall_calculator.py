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
