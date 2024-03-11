from src.constants import Constants


class Solver:
    def __init__(self, classifier, evaluator):
        self.classifier = classifier
        self.evaluator = evaluator

    def solve(self, sample, verbose=False):
        # TODO: preprocessing
        sample = self.preprocess(sample)

        # classifying
        question_type = self.classifier(sample)

        # evaluating
        answer_index = self.evaluator(sample, question_type, verbose=verbose)

        return answer_index

    def preprocess(self, sample):
        return sample
