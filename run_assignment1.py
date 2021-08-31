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
      #if re.match(r"^[A-Z]{1,}$",ii) and re.match(r"^[A-Z][A-Z. ]{0,}$",ii):
      #if REGEX["roman"].match(ii):
      if re.match(r"[0-9]",ii) and not re.match(r"^[0-9\.\,]+$", ii.strip()):
      #if re.match(r"\d+\s*:\s*\d+",ii):
      #if re.match(r"[012]{0,1}[0-9]\s*:\s*[0-5][0-9]",ii):
      #if re.match(r"\d",ii) and not re.match(r"[012]{0,1}[0-9]\s*:\s*[0-5][0-9]",ii):
      #if re.match(r"\d?\d (january|february|march|april|may|june|july|august|september|october|november|december) \d\d\d\d", ii.lower()):
      #if re.match(r"^\d\d\d\d[\/\-\.]\d\d[\/\-\.]\d\d$",ii):
      #if re.match(r"\(?\d+[\-\( ]+\d+" , ii):
      #if not re.match(r"[^A-Z0-9]",ii) and re.match(r"^[0-9\.\,]+$", ii.strip()):
        #ii = re.sub(r"([012]{0,1}[0-9])\s*:\s*([0-5][0-9])",r" \1:\2 ",ii).strip()
        print(ii,"\t:\t",oo)



"""# Solution"""

MONTHS = ["january","february","march","april","may","june","july","august","september","october","november","december"]
DAYS = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
DIGITS = ('o', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
ORDINALS = {"one": "first", "two": "second", "three": "third", "four": "fourth", "five": "fifth", "six": "sixth", "seven": "seventh", "eight": "eighth", "nine": "ninth", "ten": "tenth", "eleven": "eleventh", "twelve": "twelfth"}

REGEX={
  "punctuation": re.compile(r"[^A-Za-z0-9]"),
  "roman_exception": re.compile(r"^(CC|CD|CV|DC|MC|MD|MI)$"), # Adapted from: http://www.web40571.clarahost.co.uk/roman/quiza.htm
  "roman": re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"), # Adapted from: https://www.geeksforgeeks.org/validating-roman-numerals-using-regular-expression/
  "abbreviation": re.compile(r"^[A-Z][A-Z. ]{0,}$"),
  "time": re.compile(r"[0-9]{1,}\s*:\s*[0-5][0-9]"),

  "date": re.compile(r"^(\d?\d)\s*([a-z]{0,2}?)\s+((?:"+ r'|'.join(MONTHS) +r"))\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date_1": re.compile(r"^((?:"+ r'|'.join(MONTHS) +r"))\s*(\d?\d)\s*([a-z]{0,2}?)\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date_abbr": re.compile(r"^(\d?\d)\s*([a-z]{0,2}?)\s*\.?\s*\,?\s*((?:"+ r'|'.join([m[:3] for m in MONTHS]) +r"|sept))\s*\.?\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date_abbr_1": re.compile(r"^((?:"+ r'|'.join([m[:3] for m in MONTHS]) +r"|sept))\s*\.?\s*\,?\s*(\d?\d)\s*([a-z]{0,2}?)\s*\.?\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date_2": re.compile(r"^(\d?\d\d\d)\s*[\/\-\.\|]\s*(\d?\d)\s*[\/\-\.\|]\s*(\d?\d)$"),
  "date_3": re.compile(r"^(\d?\d)\s*[\/\-\.\|]\s*(\d?\d)\s*[\/\-\.\|]\s*(\d?\d\d\d)$"),

  "number_by_digits" : re.compile(r"^\(?\s*\d+\s*\)?\s*[\-\(\) ]+\s*\d+\s*[0-9\-\(\) ]*$"),
  "decimal_number_only": re.compile(r"^[0-9\.\,]+$"),   # space? :: TODO
  "ordinal_number": re.compile(r"^(\d[0-9\,]{0,})\s*(st|nd|rd|th)$"),
  "fraction_only": re.compile(r"^(\d[0-9\,]{0,})\s*\/\s*(\d[0-9\,]{0,})$"),
  "mixed_fraction": re.compile(r"^(\d[0-9\,]{0,})\s+(\d[0-9\,]{0,})\/(\d[0-9\,]{0,})$")
}


def handle_number_to_words(token: str) -> bool:
  # Adapted from: https://www.codesansar.com/python-programming-examples/number-words-conversion-no-library-used.htm

  # Main Logic
  ones = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
  twos = ('ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen')
  tens = ('twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred')
  suffixes = ('', 'thousand', 'million', 'billion', 'trillion', 'quadrillion')

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
      
      if length>18: # cannot handle currently
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
  return len(token)>1 and REGEX['roman_exception'].match(token)

def is_roman(token: str) -> bool:
  return len(token)>1 and REGEX['roman'].match(token)

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
  return len(token)>1 and REGEX['abbreviation'].match(token);

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
    if "hr" in tokens[i].lower().replace(".",""):
      token.append('hours')
      continue
    token.append(handle_abbreviation(tokens[i]))

  token = " ".join(token)
  return token


def is_date(token: str) -> bool:
  token = token.lower()
  return REGEX['date'].match(token) or REGEX['date_abbr'].match(token) or REGEX['date_1'].match(token) or REGEX['date_abbr_1'].match(token) or REGEX['date_2'].match(token) or REGEX['date_3'].match(token)

def preprocess_date(token: str) -> str:
  token = token.lower()
  if REGEX['date'].match(token):
    return REGEX['date'].sub(r"\1 \3 \4",token)
  elif REGEX['date_1'].match(token):
    return REGEX['date_1'].sub(r"\2 \1 \4",token)
  elif REGEX['date_abbr'].match(token):
    s = REGEX['date_abbr'].sub(r"\1 \3 \4",token).split()
    for m in MONTHS:
      if m.startswith(s[1]):
        s[1] = m
        break
    return " ".join(s)
  elif REGEX['date_abbr_1'].match(token):
    s = REGEX['date_abbr_1'].sub(r"\2 \1 \4",token).split()
    for m in MONTHS:
      if m.startswith(s[1]):
        s[1] = m
        break
    return " ".join(s)
  elif REGEX['date_2'].match(token):
    s = REGEX['date_2'].sub(r"\3 \2 \1",token).split()
    # try..except if index error.. maybe telephone number :: TODO
    if int(s[1]) > 12:
      s[0],s[1] = s[1],s[0]
    try:
      s[1] = MONTHS[int(s[1])-1]
      return " ".join(s)
    except:
      return token
  elif REGEX['date_3'].match(token):
    s = REGEX['date_3'].sub(r"\1 \2 \3",token).split()
    if int(s[1]) > 12:
      s[0],s[1] = s[1],s[0]
    try:
      s[1] = MONTHS[int(s[1])-1]
      return " ".join(s)
    except:
      return token
  else:
    return token

def handle_date__year(token: str) -> str:
  if token == "0000": # ?
    return "zero"

  if token[0] == "'":
    token = token[1:]

  if len(token) <= 3:
    return handle_number_to_words(token)

  if token[1:] == "000":
    return handle_number_to_words(token)
  elif token[2:] == "00":
    return handle_number_to_words(token[:2])+" hundred"
  elif token[1:3] == "00":
    return handle_number_to_words(token)
  elif token[2] == "0":
    return handle_number_to_words(token[:2])+" o "+handle_number_to_words(token[3])
  else:
    return handle_number_to_words(token[:2]) + " " + handle_number_to_words(token[2:])

def handle_date(token: str) -> str:
  token = preprocess_date(token)
  
  if not REGEX['date'].match(token):
    return handle_number_spoken_as_digits(token)

  tokens = token.split()
  d = handle_ordinal_number(tokens[0], process=False)
  m = tokens[1]
  y = handle_date__year(tokens[2])

  # --00 thousand; 200- two thousand xx; 1908 --o--; 
  return " ".join(['the',d,'of',m,y])



def is_number_spoken_as_digits(token: str) -> bool:
  return "/" not in token and REGEX['number_by_digits'].match(token)

def handle_number_spoken_as_digits(token: str) -> str:
  ans = []
  for ch in token:
    if REGEX['punctuation'].match(ch):
      p = handle_punctuation(ch)
      ans.append(p) if len(ans)==0 or ans[-1]!=p else None
    else: ## TODO:: INDEX ERROR?
      ans.append(DIGITS[int(ch)])
  return " ".join(ans)

def is_decimal_number_only(token: str) -> bool:
  return REGEX['decimal_number_only'].match(token)  # not match space 

def handle_decimal_number_only(token: str) -> str:
  if re.match(r"^[1-9]\d\d\d$",token):  # probably a year (no comma!)
    return handle_date__year(token)
  elif token.startswith('0') and len(token) == 10 and ',' not in token and '.' not in token:  # probably to be read digit-wise (phone number, ...)
    return handle_number_spoken_as_digits(token)
  #elif len(token) == 10:  # phone number?
  #  return handle_number_spoken_as_digits(token)
  else:
    token = token.replace(",","").split(".")
    ans = handle_number_to_words(token[0])
    if len(token) > 1:
      if token[1] == "0":
        ans+= " point zero"
      else:
        ans+= " point " + handle_number_spoken_as_digits(token[1])
    return ans

def is_ordinal_number(token: str) -> bool:
  return REGEX['ordinal_number'].match(token.lower())

def handle_ordinal_number(token: str, process: bool = True) -> str:
  token = REGEX['ordinal_number'].sub(r"\1 \2",token.lower()).split()[0]
  if process:
    token = handle_decimal_number_only(token)
  else:
    token = handle_number_to_words(token)
  tokens = token.split()
  suffixed = tokens[-1]
  try:
      suffixed = ORDINALS[suffixed]
  except KeyError:
      if suffixed[-1] == "y":
          suffixed = suffixed[:-1] + "ie"
      suffixed += "th"
  tokens[-1] = suffixed
  return " ".join(tokens)


def is_fraction_only(token: str) -> bool:
  return REGEX['fraction_only'].match(token)

def handle_fraction_only(token: str) -> str:
  token = token.replace(",","").replace(" ","")

  n, d = token.split("/")
  if d == "2":
    d = "half"
  elif d == "4":
    d = "quater"
  else:
    d = handle_ordinal_number(d, process=False)

  if int(n) != 1:
    if d[-1] == "f": # "half"
      d = d[:-1] + "ves"
    else:
      d += "s"

  ## is it "one half"?? :: TODO <<#1>>
  n = handle_number_to_words(n)

  return f"{n} {d}"

def is_mixed_fraction(token: str) -> bool:
  return REGEX['mixed_fraction'].match(token)

def handle_mixed_fraction(token: str) -> str:
  w, f = token.split()
  w = handle_number_to_words(w)
  f = handle_fraction_only(f)

  if f[:3] == "one":
    f = "a" + f[3:]

  return f"{w} and {f}"

def to_spoken(token: str) -> str:
  token = token.strip()
  if is_punctuation(token):
    return handle_punctuation(token)
  elif is_roman_exception(token): # TODO:: what about V,X,L,C,M ??
    return handle_abbreviation(token)
  elif is_roman(token):
    return handle_roman_to_numeral(token)
  elif is_abbreviation(token):
    return handle_abbreviation(token)
  elif is_time(token):
    return handle_time(token)
  elif is_date(token):
    return handle_date(token)
  elif is_number_spoken_as_digits(token):
    return handle_number_spoken_as_digits(token)
  elif is_decimal_number_only(token):
    return handle_decimal_number_only(token)
  elif is_ordinal_number(token):
    return handle_ordinal_number(token)
  elif is_fraction_only(token):
    return handle_fraction_only(token)
  elif is_mixed_fraction(token):
    return handle_mixed_fraction(token)
  else:
    return '<self>'

def solution(input_tokens: [str]) -> [str]:
  sol = []
  for token in input_tokens:
    sol.append(to_spoken(token))

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

