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
      #if not re.match(r"^[A-Z]{1,}$",ii) and re.match(r"^[A-Z ]{1,}$",ii):
      if re.match(r"^[A-Z]{1,}$",ii) and re.match(r"^[A-Z][A-Z. ]{0,}$",ii):
      #if REGEX["roman"].match(ii):
      #if re.match(r"[0-9]",ii):
      #if re.match(r"\d+\s*:\s*\d+",ii):
      #if re.match(r"[012]{0,1}[0-9]\s*:\s*[0-5][0-9]",ii):
        #ii = re.sub(r"([012]{0,1}[0-9])\s*:\s*([0-5][0-9])",r" \1:\2 ",ii).strip()
        print(ii,"\t:\t",oo)



"""# Solution"""

REGEX={
  "punctuation": re.compile(r"[^A-Z0-9]"),
  "roman_exception": re.compile(r"^(CC|CD|CV|DC|MC|MD|I|MI)$"), # Adapted from: http://www.web40571.clarahost.co.uk/roman/quiza.htm
  "roman": re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"), # Adapted from: https://www.geeksforgeeks.org/validating-roman-numerals-using-regular-expression/
  "abbreviation": re.compile(r"^[A-Z][A-Z. ]{0,}$"),
  "time": re.compile(r"[0-9]{1,}\s*:\s*[0-5][0-9]")
}


def handle_number_to_words(token: str) -> bool:
  # Adapted from: https://www.codesansar.com/python-programming-examples/number-words-conversion-no-library-used.htm

  # Main Logic
  ones = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
  twos = ('ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen')
  tens = ('twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred')
  suffixes = ('', 'thousand', 'million', 'billion')

  def process(number, index):
      
      if number=='0':
          return 'zero'
      
      length = len(number)
      
      if(length > 3):
          return False
      
      number = number.zfill(3)
      words = ''
   
      hdigit = int(number[0])
      tdigit = int(number[1])
      odigit = int(number[2])
      
      words += '' if number[0] == '0' else ones[hdigit]
      words += ' hundred ' if not words == '' else ''
      
      if(tdigit > 1):
          words += tens[tdigit - 2]
          words += ' '
          words += ones[odigit]
      
      elif(tdigit == 1):
          words += twos[(int(tdigit + odigit) % 10) - 1]
          
      elif(tdigit == 0):
          words += ones[odigit]

      if(words.endswith('zero')):
          words = words[:-len('zero')]
      else:
          words += ' '
       
      if(not len(words) == 0):    
          words += suffixes[index]
          
      return words;
      
  def getWords(number):
      length = len(str(number))
      
      if length>12: # cannot handle currently
          return str(number)
      
      count = length // 3 if length % 3 == 0 else length // 3 + 1
      copy = count
      words = []
   
      for i in range(length - 1, -1, -3):
          words.append(process(str(number)[0 if i - 2 < 0 else i - 2 : i + 1], copy - count))
          count -= 1;

      final_words = ''
      for s in reversed(words):
          temp = s + ' '
          final_words += temp
      
      return final_words
  # End Main Logic
  return getWords(int(token)).strip()



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
  return handle_number_to_words(int_val)


def is_abbreviation(token: str) -> bool:
  return REGEX['abbreviation'].match(token);

def handle_abbreviation(token: str) -> str:
  return " ".join(list(token.replace(".","").replace(" ","").lower()))


def is_time(token: str) -> bool:
  return REGEX['time'].match(token)

def handle_time(token: str) -> str:
  token = re.sub(r"([0-9]{1,})\s*:\s*([0-5][0-9])",r" \1:\2 ",token).strip()
  token = re.sub(r"([0-9]{1,}:[0-5][0-9])\s*:\s*([0-5][0-9])",r" \1:\2 ",token).strip() # seconds
  tokens = token.split()
  times = tokens[0].split(':')

  token = [handle_number_to_words(times[0])]  # output

  if len(times)==3:
    token.extend(['hours', handle_number_to_words(times[1]), 'minutes and', handle_number_to_words(times[2]), 'seconds'])
  elif int(times[0]) >= 24: # if hrs > 24 => countdown
    token.extend(['hours and', handle_number_to_words(times[1]), 'minutes'])
  else:
    if times[1] == "00":
      if int(times[0]) > 12:  # adding "hundred" if min == "00"  :: TODO
      #if len(tokens) <= 1 or tokens[1].lower().replace(".","") not in ["am","pm"]:  # if no am/pm
        token.append("hundred")
    else:
      token.append(handle_number_to_words(times[1]))


  for i in range(1,len(tokens)):
    # handle "hrs" text :: TODO
    if tokens[i].lower().replace(".","") in ["hrs","hr"]:
      token.append('hours')
      continue
    token.append(handle_abbreviation(tokens[i]))

  token = " ".join(token)
  return token



def solution(input_tokens: [str]) -> [str]:
  sol = []
  for token in input_tokens:
    token = token.strip()
    if is_punctuation(token):
      sol.append(handle_punctuation(token))
    elif is_roman_exception(token): # TODO:: what about V,X,L,C,M ??
      sol.append(handle_abbreviation(token))
    elif is_roman(token):
      sol.append(handle_roman_to_numeral(token))
    elif is_abbreviation(token):
      sol.append(handle_abbreviation(token))
    elif is_time(token):
      sol.append(handle_time(token))
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
  print('\n\n-----------\n\n')
  analyze(in_path=args.input_path,gold_path=args.solution_path)

