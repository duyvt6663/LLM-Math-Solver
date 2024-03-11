from src.constants import Constants
from src.preprocess import *
from nltk import sent_tokenize

class Classifier:
    def __init__(self, grammar):
        self.grammar = grammar

    def __call__(self, sample):
        # some order is important
        if is_min_question(sample):
            return Constants.MIN_VALUE_QUESTION
        elif is_max_question(sample):
            return Constants.MAX_VALUE_QUESTION
        elif is_arrange_increasing_question(sample):
            return Constants.ARRANGE_INCREASING_QUESTION
        elif is_arrange_decreasing_question(sample):
            return Constants.ARRANGE_DECREASING_QUESTION
        elif is_fill_in_blank_question(self, sample):
            return Constants.FILL_IN_BLANK_QUESTION
        elif is_calculate_question(self, sample):
            return Constants.CALCULATE_QUESTION
        elif is_digit_meaning_in_number_question(sample):
            return Constants.DIGIT_MEANING_IN_NUMBER_QUESTION
        else:
            raise NotImplementedError

    def classify(self, sample):
        return self.__call__(sample)


def is_arrange_increasing_question(sample: dict):
    q = sample["question"]
    return "từ bé đến lớn" in q.lower() or "tăng dần" in q.lower()

def is_arrange_decreasing_question(sample: dict):
    q = sample["question"]
    return "từ lớn đến bé" in q.lower() or "giảm dần" in q.lower()

def is_min_question(sample: dict):
    q = sample["question"]
    return "nhỏ nhất" in q.lower() or "bé nhất" in q.lower()

def is_max_question(sample):
    q = sample["question"]
    return (
        "lớn nhất" in q.lower()
        or "nhiều nhất" in q.lower()
        or "cao nhất" in q.lower()
        or "to nhất" in q.lower()
    )

def is_calculate_question(cls, sample):
    q = sample["question"]
    sents = sent_tokenize(q)

    contain_expression = False
    seqs, typs, _ = parse_expression(
        normalize_vietnamese_numbers(q), 
        cls.grammar
    )
    for _, typ in zip(seqs, typs):
        if typ == "Expression":
            contain_expression = True
            break

    return (
        (any("phép " + p in q.lower() for p in ["cộng", "trừ", "nhân", "chia", "tính"])
        or "biểu thức" in q.lower()
        or "dưới dạng" in q.lower())
        and len(sents) == 1
        and contain_expression
    )

def is_fill_in_blank_question(cls, sample):
    q = sample["question"]

    contain_blank = False
    seqs, typs, _ = parse_expression(
        normalize_vietnamese_numbers(q), 
        cls.grammar
    )
    for seq, typ in zip(seqs, typs):
        if typ == "Equation" and "blank" in seq:
            contain_blank = True
            break

    return (
        "chỗ trống" in q.lower() 
        or "chỗ chấm" in q.lower() 
        or "ô trống" in q.lower()
    ) or contain_blank

def is_math_word_question(sample):
    q = sample["question"]
    sents = sent_tokenize(q)

    if len(sents) == 1:
        return False
    else:
        return True

def is_digit_meaning_in_number_question(sample):
    q = sample["question"]
    print(normalize_vietnamese_numbers(q))
    sents = sent_tokenize(normalize_vietnamese_numbers(q))
    return (
        "chữ số" in q.lower() 
        and "trong số" in q.lower()
        and len(sents) == 1
    )
