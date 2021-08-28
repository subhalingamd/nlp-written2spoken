'''
We expect a .py file which takes as input the input file path and the solution file path:

python run_assignment1.py --input_path <path_to_input> --solution_path <path_to_solution>

Once the solution file is generated, we will run a checker script to get the performance metrics:

python run_checker.py --solution_path <path_to_solution> --ground_truth_path <path_to_ground_truth>

'''

"""# Imports"""
import json
import re
import argparse

"""# Compare Input/Output"""
def analyze(in_path: str,gold_path: str) -> None:
  with open(in_path,'r') as input_file:
    input_data = json.load(input_file)
    input_file.close()

  with open(gold_path,'r') as output_file:
    output_data = json.load(output_file)
    output_file.close()


  for i,o in zip(input_data,output_data):
    for ii,oo in zip(i["input_tokens"],o["output_tokens"]):
      #if len(ii)==1 and re.match(r"[^A-Z0-9]",ii) and oo!="sil":
      #if re.match(r"^[A-Z]{1,}$",ii) and re.match(r"^[A-Z ]{1,}$",ii):
      #if REGEX["roman"].match(ii):
      if re.match(r"[0-9]",ii):
        print(ii,"\t:\t",oo)



"""# Solution"""

REGEX={
  "punctuation": re.compile(r"[^A-Z0-9]"),
  "roman_exception": re.compile(r"^(CC|CD|CV|DC|MC|MD|I|MI)$"), # Adapted from: http://www.web40571.clarahost.co.uk/roman/quiza.htm
  "roman": re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"), # Adapted from: https://www.geeksforgeeks.org/validating-roman-numerals-using-regular-expression/
  "abbreviation": re.compile(r"^[A-Z]{1,}$"),
}


def is_punctuation(token: str) -> bool:
  return len(token)==1 and REGEX['punctuation'].match(token)

def handle_punctuation(token: str) -> str:
  return "sil"

def is_roman_exception(token: str) -> bool:
  return REGEX['roman_exception'].match(token)

def is_roman(token: str) -> bool:
  return REGEX['roman'].match(token)

def handle_roman_to_numeral(token: str) -> str:
  # Adapted from: https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-2.php
  rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
  int_val = rom_val[token[0]]
  for i in range(1,len(token)):
      if rom_val[token[i]] > rom_val[token[i - 1]]:
          int_val += rom_val[token[i]] - 2 * rom_val[token[i - 1]]
      else:
          int_val += rom_val[token[i]]
  return int_val


def is_abbreviation(token: str) -> bool:
  return REGEX['abbreviation'].match(token);

def handle_abbreviation(token: str) -> str:
  return " ".join(list(token.lower()))

def solution(input_tokens: [str]) -> [str]:
  sol = []
  for token in input_tokens:
    if is_punctuation(token):
      sol.append(handle_punctuation(token))
    elif is_roman_exception(token):
      sol.append(handle_abbreviation(token))
    elif is_roman(token):
      sol.append(handle_roman_to_numeral(token))
    elif is_abbreviation(token):
      sol.append(handle_abbreviation(token))
    else:
      sol.append('<self>')

  return sol
  

def main(in_path: str, out_path: str) -> None:
  with open(in_path,'r') as input_file:
    input_data = json.load(input_file)
    input_file.close()

  solution_data = []
  for input_sentence in input_data:
    solution_sid = input_sentence['sid']
    solution_tokens = solution(input_sentence['input_tokens'])
    solution_data.append({'sid':solution_sid,
                          'output_tokens':solution_tokens})

  with open(out_path,'w') as solution_file:
    json.dump(solution_data, solution_file, indent=2, ensure_ascii=False)
    solution_file.close()

 

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(description='Rule-based Written-to-Spoken Text Conversion')
  parser.add_argument('-i','--input_path', metavar="<path_to_input>", default="data/input train.json",
                    help='path to input data')
  parser.add_argument('-o','--solution_path', metavar="<path_to_solution>", default="out/output train.json",
                    help='path to store output')
  parser.add_argument('-g','--gold_path', metavar="<path_to_gold_output>", default="data/output train.json",
                    help='path to gold output')

  args = parser.parse_args()
  
  analyze(in_path=args.input_path,gold_path=args.gold_path)
  main(in_path=args.input_path,out_path=args.solution_path)

