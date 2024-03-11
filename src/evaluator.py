from src.constants import Constants
from src.preprocess import *
import math

class Evaluator:
    def __init__(self, grammar):
        self.grammar = grammar
        self.unit_set = get_var_dict()
        self.allowed_error = 1e-5

    def __call__(self, sample, question_type, verbose=False):
        if question_type == Constants.MIN_VALUE_QUESTION:
            return self.__solve_min_question(sample, verbose)
        elif question_type == Constants.MAX_VALUE_QUESTION:
            return self.__solve_max_question(sample, verbose)
        elif question_type == Constants.ARRANGE_INCREASING_QUESTION:
            return self.__solve_arrange_monotonic_question(sample, increasing=True, verbose=verbose)
        elif question_type == Constants.ARRANGE_DECREASING_QUESTION:
            return self.__solve_arrange_monotonic_question(sample, verbose=verbose)
        elif question_type == Constants.FILL_IN_BLANK_QUESTION:
            return self.__solve_fill_in_blank_question(sample, verbose)
        elif question_type == Constants.CALCULATE_QUESTION:
            return self.__solve_calculate_question(sample, verbose)
        elif question_type == Constants.DIGIT_MEANING_IN_NUMBER_QUESTION:
            return self.__solve_digit_meaning_in_number_question(sample, verbose)
        else:
            raise NotImplementedError

    def evaluate(self, sample, question_type, verbose=False):
        return self.__call__(sample, question_type, verbose)

    @staticmethod
    def print_stat(sample, correct_idx):
        print("Question:", sample["question"])
        print("Options:", sample["choices"])
        print("Prediction:", sample['choices'][correct_idx])
        print("Ground truth:", sample["answer"])
        print('-' * 50)

    def __solve_min_question(self, sample, verbose=False):
        question = sample["question"]
        choices = sample["choices"]

        choices_content = [get_option_content(choice) for choice in choices]
        choices_number = [
            normalize_vietnamese_numbers(choice_content)
            for choice_content in choices_content
        ]
        choices_number = [
            float(choice_number.strip()) for choice_number in choices_number
        ]

        min_choice_index = choices_number.index(min(choices_number))
        if verbose:
            self.print_stat(sample, min_choice_index)
        return min_choice_index

    def __solve_max_question(self, sample, verbose=False):
        question = sample["question"]
        choices = sample["choices"]

        choices_content = [get_option_content(choice) for choice in choices]
        choices_number = [
            normalize_vietnamese_numbers(choice_content)
            for choice_content in choices_content
        ]
        choices_number = [
            float(choice_number.strip()) for choice_number in choices_number
        ]

        max_choice_index = choices_number.index(max(choices_number))
        if verbose:
            self.print_stat(sample, max_choice_index)
        return max_choice_index
    
    def __solve_arrange_monotonic_question(self, sample, increasing=False, verbose=False):
        question = sample["question"]
        choices = sample["choices"]

        choices_content = [get_option_content(choice) for choice in choices]
        choices_seq = [
            parse_expression(
                normalize_vietnamese_numbers(choice_content),
                grammar=self.grammar
            )
            for choice_content in choices_content
        ]

        def is_monotonic(seq, increasing=False):
            prev = math.inf * (-1 if increasing else 1)
            for ele in seq:
                now = float(ele)
                if (increasing and now < prev) or (not increasing and now > prev): 
                    return False
                else:
                    prev = now
            return True

        for i, (seq, _, _) in enumerate(choices_seq):
            if is_monotonic(seq[0], increasing=increasing):
                if verbose:
                    self.print_stat(sample, i)
                return i
        raise Exception("No answer found")

    def __solve_fill_in_blank_question(self, sample, verbose=False):
        question = sample["question"]
        choices = sample["choices"]

        choices_content = [get_option_content(choice) for choice in choices] + [question]
        choices_seq = [
            parse_expression(
                normalize_vietnamese_numbers(choice_content),
                grammar=self.grammar
            )
            for choice_content in choices_content
        ]

        qseq, qtyps, _ = choices_seq[-1]
        for i, (s, t) in enumerate(zip(qseq, qtyps)):
            if t == 'Equation':
                eq_idx = i
                break
        else: # final attempt to solve using calculate question
            print("No blank in question, try to solve as calculate question")
            return self.__solve_calculate_question(sample, verbose) 
            # raise Exception("No blank in question")

        # fill in a blank to correct format when no blank but an equation is found
        if "blank" not in qseq[eq_idx]: 
            qseq = qseq[eq_idx].asList()
            compare_idx = [qseq.index(p) for p in ['==', '>', '<'] if p in qseq][0]
            qseq = qseq[:compare_idx+1] + ['...'] + qseq[compare_idx+1:]
            print(qseq)
        else: # normal case
            qseq = qseq[eq_idx].asList()
        blank_idx = qseq.index('...')

        for i, (seq, _, _) in enumerate(choices_seq[:-1]):
            seq = seq[0].asList() # the first sub-sequence is equation  
            if seq[-2:] == qseq[-2:] and seq[-1] in self.unit_set:
                seq.pop(), seq.pop() # remove redundant units

            # substitute choice into the blank and evaluate the truth value
            to_subtitute = ''.join(seq)
            if to_subtitute == '=': 
                to_subtitute = '==' # convert rare case of '=' to '=='
            
            new_eq = qseq.copy()
            new_eq[blank_idx] = to_subtitute
            if "<" in new_eq:
                eq_idx = new_eq.index("<")
                new_eq = f"({''.join(new_eq[:eq_idx])}) - ({''.join(new_eq[eq_idx+1:])}) < -{self.allowed_error}"
            elif "==" in new_eq: # avoid floating point error when equating two expression
                eq_idx = new_eq.index("==")
                new_eq = f"abs(({''.join(new_eq[:eq_idx])}) - ({''.join(new_eq[eq_idx+1:])})) <= {self.allowed_error}"
            elif ">" in new_eq:
                eq_idx = new_eq.index(">")
                new_eq = f"({''.join(new_eq[:eq_idx])}) - ({''.join(new_eq[eq_idx+1:])}) > {self.allowed_error}"
            else:
                raise Exception("No operator found")
            result = eval(new_eq, self.unit_set)

            if result:
                if verbose:
                    self.print_stat(sample, i)
                return i

        raise Exception("No answer found")

    def __solve_calculate_question(self, sample, verbose):
        question = sample["question"]
        choices = sample["choices"]

        choices_content = [get_option_content(choice) for choice in choices] + [question]
        choices_seq = [
            parse_expression(
                normalize_vietnamese_numbers(choice_content),
                grammar=self.grammar
            )
            for choice_content in choices_content
        ]

        qseq, qtyps, _ = choices_seq[-1]
        for i, (s, t) in enumerate(zip(qseq, qtyps)):
            if t == 'Expression':
                eq_idx = i
                break
        else:
            raise Exception("No expression in question")
        qseq = ''.join(qseq[eq_idx].asList())

        for i, (seq, _, _) in enumerate(choices_seq[:-1]):
            seq = seq[0].asList() # the first sub-sequence is expression
            # append the choice expression to the question expression via operator ==
            new_eq = f"abs(({qseq}) - ({''.join(seq)})) <= {self.allowed_error}" # avoid floating point error
            result = eval(new_eq, self.unit_set)
            if result:
                if verbose:
                    self.print_stat(sample, i)
                return i

        raise Exception("No answer found")
    
    def __solve_digit_meaning_in_number_question(self, sample, verbose):
        question = sample["question"]
        choices = sample["choices"]

        choices_content = [get_option_content(choice) for choice in choices] + [question]
        choices_seq = [
            parse_expression(
                normalize_vietnamese_numbers(choice_content),
                grammar=self.grammar
            )
            for choice_content in choices_content
        ]

        expressions = []
        qseq, qtyps, _ = choices_seq[-1]
        for s, t in zip(qseq, qtyps):
            if t == 'Expression':
                expressions.append(s[0])
        assert len(expressions) == 2, "Only support 2 expressions in question"
        assert any(len(p) == 1 for p in expressions), "Exist 1 digit for template"

        a, b = expressions
        if len(a) > 1: # b is the digit -> swap
            a, b = b, a

        if "thuộc hàng" in question.lower():
            # TODO: digit to text
            pass
        else:
            # preprocess the expressions in question
            qnumber = a
            if a != "0":
                idx = b.index(a)
                if '.' in b[:idx]:
                    dot_idx = b[:idx].index('.')
                    qnumber = '0.' + '0'*(idx -dot_idx -1) + a
                qnumber += ''.join(dg if not dg.isdigit() else "0" for dg in b[idx + 1 :])
            
            # process the choices
            for i, (seq, _, _) in enumerate(choices_seq[:-1]):
                seq = seq[0].asList() # the first sub-sequence is expression
                # append the choice expression to the question expression via operator ==
                new_eq = f"abs(({qnumber}) - ({''.join(seq)})) <= {self.allowed_error}" # avoid floating point error
                result = eval(new_eq, self.unit_set)
                if result:
                    if verbose:
                        self.print_stat(sample, i)
                    return i
        
        raise Exception("No answer found")