from src.classifier import Classifier
from src.evaluator import Evaluator
from src.solver import Solver
from src.preprocess import *
import json


if __name__ == "__main__":
   grammar = get_grammar()
   classifier = Classifier(grammar=grammar)
   evaluator = Evaluator(grammar=grammar)
   solver = Solver(classifier, evaluator)
   sample = {
<<<<<<< HEAD
<<<<<<< HEAD
         "id": "01-0243",
         "question": "Chữ số 5 trong số 254. 836 chỉ:",
         "choices": [
            "A. 50 000",
            "B. 500 000",
            "C. 5 000",
            "D. 50 000 000"
         ],
         "answer": "A. 50 000"
=======
=======
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
         "id": "01-0275",
         "question": "Phân số \\frac{3}{4} được viết dưới dạng số thập phân là:",
         "choices": [
            "A. 3,4",
            "B. 0,75",
            "C. 4,3",
            "D. 0,57"
         ],
         "answer": "B. 0,75"
<<<<<<< HEAD
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
=======
>>>>>>> 89333f4d9d28df144e9976956821627747715b30
      }
   solver.solve(sample, True)