# Written to Spoken Text Conversion

<!-- MarkdownTOC -->

1. [Motivation](#motivation)
1. [Problem Statement](#problem-statement)
1. [Input and Output formats](#input-and-output-formats)
1. [Evaluation Metric](#evaluation-metric)
1. [Running the code](#running-the-code)
    1. [Main part](#main-part)
    1. [Evaluation](#evaluation)
    1. [Tests](#tests)
1. [Results](#results)
1. [Footnotes](#footnotes)

<!-- /MarkdownTOC -->


<a id="motivation"></a>
## Motivation
The motivation of this assignment is to get an insight into writing rule-based NLP engines. It will also, hopefully, showcase the sheer number of corner cases that arise in NLP, and, thus, the subsequent importance of data-driven machine learning systems.


<a id="problem-statement"></a>
## Problem Statement
The goal of the assignment is to write a written to spoken text converter. The input of the code will be a set of tokenized sentences, and the output will be conversions where date, time, and numerical quantities are rewritten in the way they will be spoken.

At a high level, the guidelines for text conversion are as follows:
1. **All abbreviations are separated as they are spoken**. Example, *“U.S.”* or *“US”* is converted to *“u s”*.
2. **All dates are converted into words**. Example, *“29 March 2012”* will be converted to *“the twenty ninth of march twenty twelve”*. *“2011-01-25”* will be converted to *“the twenty fifth of january twenty eleven”*.
3. **All times are converted into words**. Example, *“04:40 PM”* is converted to *“four forty p m”*. *“21:30:12”* is converted to *“twenty one hours thirty minutes and twelve seconds”*
4. **All numeric quantities are converted to words using Western numbering system**. Example, *“10345”* is converted to *“ten thousand three hundred forty five”*. *“24349943”* is converted to *“twenty four million three hundred forty nine thousand nine hundred forty three”*. *“184.33”* is converted to *“one hundred eighty four point three three”*. *“-20”* is converted to *“minus twenty”*.
5. **All units are spelled out as spoken.** *“53.77 mm”* is converted to *“fifty three point seven seven millimeters”*, *“3 mA”* is converted to *“three milliamperes”*, and *“14 sq m”* is converted to *“fourteen square meters”*.
6. **Currency is also spelled out**. *“$15.24”* is converted to *“fifteen dollars and twenty four cents”*. *“£11”* is converted to *“eleven pounds”*.

This is not an exhaustive list of patterns that occur in the provided data. Example, there can be phone numbers, years, roman numbers (~~abbreviations?~~), ISBN codes, (mixed) fractions, to mention a few.

**Note:** All conversions to be made in lowercase only.




<a id="input-and-output-formats"></a>
## Input and Output formats
The input file is in the *json* format. Each entry in the input file has the following structure.
```
__sid__: A unique identifier for each sentence. (Type: String)
__input_tokens__: A list of tokens in the input sentence. (Type: List[String])
```

For each entry in the input file, the program converts the `input_tokens` into their spoken form. For tokens which do not need conversion, the program outputs `<self>` token. For punctuations, the program outputs a `sil` token. Final output of program will be a new *json* file. Each entry in the file will have the following structure.
```
__sid__: A unique identifier corresponding to an input sentence. (Type: String)
__output_tokens__: A list of converted tokens corresponding to input_tokens from the input sentence. (Type: List[String])
```

<a id="evaluation-metric"></a>
## Evaluation Metric
**Metric:** F-measure.

Consider the following categories:
1. An input token (that is not a `sil` or a `<self>` token) is correctly converted. For this a 1 will be added to both the numerator and denominator of both precision and recall.
2. An input token (that is a `sil` or a `<self>` token) is correctly converted. This will not affect the precision/recall computation.
3. An input token (that is not a `sil` or a `<self>` token) should have been converted but the program missed it (i.e., converted it to `sil` or `<self>`). For this a 1 will be added to the denominator of recall.
4. An input token should not have been converted (i.e., it should have been `sil` or `<self>`), but the program erroneously converted it. For this a 1 will be added to the denominator of precision.
5. An input token (non-`sil`, non-`<self>`) should have been converted but the program converted it incorrectly (to a non-`sil`, non-`<self>`). For this, a 1 will be added to the denominator of both the precision and recall.

F-score is the Harmonic mean of precision and recall.




<a id="running-the-code"></a>
## Running the code
<a id="main-part"></a>
### Main part
The synopsis for [`run_assignment1.py`](run_assignment1.py) is
```bash
python run_assignment1.py [-i <path_to_input>] [-o <path_to_solution>]
                          [-g <path_to_gold_output>]
```
where
```
  -i <path_to_input>, --input_path <path_to_input>
                        path to input data
  -o <path_to_solution>, --solution_path <path_to_solution>
                        path to store output


optional arguments:

  -g <path_to_gold_output>, --gold_path <path_to_gold_output>
                        path to gold output
```



<a id="evaluation"></a>
### Evaluation
For evaluation, use [`run_checker.py`](run_checker.py) whose synopisis is:
```bash
python run_checker.py -sol_path SOLUTION_PATH -grn_path GROUND_TRUTH
```
where
```
  -sol_path SOLUTION_PATH, --solution_path SOLUTION_PATH
                        Output file to be scored
  -grn_path GROUND_TRUTH, --ground_truth GROUND_TRUTH
                        Gold Output file
```
Above program will check the format of the output file and compute metrics against gold outputs.

<a id="tests"></a>
### Tests
[`pytest`](https://pypi.org/project/pytest/) library is required for running tests. If not installed already, get it *via* `pip`:
```bash
pip install pytest
```

To run tests, simply use the following command:
```bash
pytest tests.py
```

<a id="results"></a>
## Results
**Given data:**
```
Precision: 0.9864 Recall: 0.9754 F1: 0.9809
```

**Test data:**
```
F1: 0.9794
```


<a id="footnotes"></a>
## Footnotes
- *This was one of the best performing systems in the entire class*
- Checkout [`tests.py`](tests.py) to get an idea of different cases this system can handle.
- GitHub Action runs (in this repo) also has logs of evaluation scores.



----
*This README uses texts from the assignment problem document provided in the course.*