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
      #if re.match(r"[0-9]",ii) and not re.match(r"^[0-9\.\,]+$", ii.strip()):
      #if re.match(r"\d+\s*:\s*\d+",ii):
      #if re.match(r"[012]{0,1}[0-9]\s*:\s*[0-5][0-9]",ii):
      #if re.match(r"\d",ii) and not re.match(r"[012]{0,1}[0-9]\s*:\s*[0-5][0-9]",ii):
      #if re.match(r"\d?\d (january|february|march|april|may|june|july|august|september|october|november|december) \d\d\d\d", ii.lower()):
      #if re.match(r"^\d\d\d\d[\/\-\.]\d\d[\/\-\.]\d\d$",ii):
      #if re.match(r"\(?\d+[\-\( ]+\d+" , ii):
      #if not re.match(r"[^A-Z0-9]",ii) and re.match(r"^[0-9\.\,]+$", ii.strip()):
      #if is_abbreviation(ii):
        #ii = re.sub(r"([012]{0,1}[0-9])\s*:\s*([0-5][0-9])",r" \1:\2 ",ii).strip()
        #print(ii,"\t:\t",oo)
        print(ii,"\t:\t",oo) if oo not in ["<self>"] else None



"""# Solution"""

VOWELS = set(('a','e','i','o','u'))
MONTHS = ("january","february","march","april","may","june","july","august","september","october","november","december")
DAYS = ("sunday","monday","tuesday","wednesday","thursday","friday","saturday")
DIGITS = ('o', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
ORDINALS = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth", "nine": "ninth", "twelve": "twelfth"}
CURRENCIES = {"Re": (("rupee","rupees"),("paise","paise")), "Rs": (("rupee","rupees"),("paise","paise")), "₹": (("rupee","rupees"),("paise","paise")), "$": (("dollar","dollars"),("cent","cents")), "£": (("pound","pounds"),("penny","pence")) ,"€": (("euro","euros"),("cent","cents"))}
CURRENCY_SUFFIXES = {"k": "thousand", "m": "million", "b": "billion", "tr": "trillion", "l": "lakh", "cr": "crore"}
UNITS = {"%": ("percent","percent"), "pc": ("percent","percent"), "m": ("meter","meters"), "s": ("second","seconds"), "g": ("gram","grams"), "A": ("ampere","amperes"), "mol": ("mole","moles"), "mole": ("mole","moles"), "K": ("kelvin","kelvins"), "cd": ("candela","candelas"), "°": ("degree","degrees"), "°C": ("degree celsius","degrees celsius"), "°F": ("degree fahrenheit","degrees fahrenheit"), "V": ("volt","volts"), "W": ("watt","watts"), "N": ("newton","newtons"), "Pa": ("pascal","pascals"), "l": ("liter","liters"), "B": ("byte","bytes"), "b": ("bit","bits"), "mi": ("mile","miles"), "ha": ("hectare","hectares"), "hz": ("hertz","hertz"), "pm": ("p m","p m"), "am": ("a m","a m"), "sq": ("square","square"), "cu": ("cubic","cubic")}
UNITS_PREFIX = {"n": "nano", "m": "milli", "c": "centi", "k": "kilo", "K": "kilo", "M": "mega", "G": "giga", "T": "terra", "P": "peta"}
UNITS_SUFFIX = {"2": "square", "3": "cubic", "²": "square", "³": "cubic"}

REGEX={
  "punctuation": re.compile(r"[^A-Za-z0-9]"),
  "roman_exception": re.compile(r"^(CC|CD|CV|DC|MC|MD|MI)$"), # Adapted from: http://www.web40571.clarahost.co.uk/roman/quiza.htm
  "roman": re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"), # Adapted from: https://www.geeksforgeeks.org/validating-roman-numerals-using-regular-expression/
  "abbreviation": re.compile(r"^(?:(?:[A-Z]\.?)|(?:[A-Z]+[A-Za-z .]*[A-Z]+[A-Za-z .]*)|(?:[a-z .]+[A-Z]+[A-Za-z .]*)|(?:(?:[a-z]+\.+\s*)+))\-?$"),
  "time": re.compile(r"[0-9]{1,}\s*:\s*[0-5][0-9]"),

  "date__wo_date": re.compile(r"^((?:"+ r'|'.join(MONTHS) +r"))\s*\,?\s+((?:\'|\d?\d)\d\d)$"),
  "date__wo_date_abbr": re.compile(r"^((?:"+ r'|'.join([m[:3] for m in MONTHS]) +r"|sept))\s*\.?\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date__wo_date_3": re.compile(r"^(\d?\d)\s*[\-]\s*(\d?\d\d\d)$"), ## NOTE: ignoring '/' for fractions; '.' for decimals
  "date__wo_year": re.compile(r"^(\d?\d)\s*([a-z]{0,2}?)\s+((?:"+ r'|'.join(MONTHS) +r"))$"),
  "date__wo_year_1": re.compile(r"^((?:"+ r'|'.join(MONTHS) +r"))\s+(\d?\d)\s*([a-z]{0,2}?)$"),
  "date__wo_year_abbr": re.compile(r"^(\d?\d)\s*([a-z]{0,2}?)\s*\.?\s*\,?\s*((?:"+ r'|'.join([m[:3] for m in MONTHS]) +r"|sept))\.?$"),
  "date__wo_year_abbr_1": re.compile(r"^((?:"+ r'|'.join([m[:3] for m in MONTHS]) +r"|sept))\s*\.?\s*\,?\s*(\d?\d)\s*([a-z]{0,2}?)$"),
  "date__wo_year_3": re.compile(r"^(\d?\d)\s*[\-]\s*(\d?\d)$"),
  
  "date": re.compile(r"^(\d?\d)\s*([a-z]{0,2}?)\s+((?:"+ r'|'.join(MONTHS) +r"))\s*\,?\s+((?:\'|\d?\d)\d\d)$"),
  "date_1": re.compile(r"^((?:"+ r'|'.join(MONTHS) +r"))\s*(\d?\d)\s*([a-z]{0,2}?)\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date_abbr": re.compile(r"^(\d?\d)\s*([a-z]{0,2}?)\s*\.?\s*\,?\s*((?:"+ r'|'.join([m[:3] for m in MONTHS]) +r"|sept))\s*\.?\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date_abbr_1": re.compile(r"^((?:"+ r'|'.join([m[:3] for m in MONTHS]) +r"|sept))\s*\.?\s*\,?\s*(\d?\d)\s*([a-z]{0,2}?)\s*\.?\s*\,?\s*((?:\'|\d?\d)\d\d)$"),
  "date_2": re.compile(r"^(\d?\d\d\d)\s*[\/\-\.\|]\s*(\d?\d)\s*[\/\-\.\|]\s*(\d?\d)$"),
  "date_3": re.compile(r"^(\d?\d)\s*[\/\-\.\|]\s*(\d?\d)\s*[\/\-\.\|]\s*(\d?\d\d\d)$"),

  "number_by_digits" : re.compile(r"^\(?\s*\d+\s*\)?\s*[\-\(\) ]+\s*\d+\s*[0-9\-\(\) ]*$"),
  "decimal_number_only": re.compile(r"^(?:(?:\d[0-9\,]*(\.\d*)?)|(?:\.\d+))$"),   # spaces removed in function
  "ordinal_number": re.compile(r"^(\d[0-9\,]{0,})\s*(st|nd|rd|th)$"),
  "fraction_only": re.compile(r"^(\d[0-9\,]{0,})\s*\/\s*(\d[0-9\,]{0,})$"),
  "mixed_fraction": re.compile(r"^(\d[0-9\,]{0,})\s+(\d[0-9\,]{0,})\/(\d[0-9\,]{0,})$"),
  "currency" : re.compile(r"^((?:"+ "|".join([c for c in CURRENCIES.keys() if c!="$"]) +r"|\$))\.?\s*([0-9\.\, ]+?)\s*([a-zA-Z .]*)$"),
  "year_with_s": re.compile(r"^([1-2]\d\d\d)s$"),   # maybe accept only YYYYs => others "seconds"?
  "measurement": re.compile(r"^([0-9][0-9 \.\,]*)\s*?([a-zA-Z \-\/234\%\.\°²³]+)$")
}


def handle_number_to_words(token: str) -> str:
  # Adapted from: https://www.codesansar.com/python-programming-examples/number-words-conversion-no-library-used.htm

  ones = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen')
  tens = ('', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred')
  suffixes = ('', 'thousand', 'million', 'billion', 'trillion', 'quadrillion')

  def process(num: str, idx: int) -> str:
    
    if num == "0":
      return "zero"
    
    length = len(num)
    
    if(length > 3):   # this shouldn't happen
      raise Exception
    
    num = num.zfill(3)    # pad with 0s
    h, t, o = int(num[0]), int(num[1]), int(num[2])

    words = ones[h] + " hundred " if h != 0 else ""
    
    if t == 0:
      words += ones[o]
    elif t == 1:
      words += ones[10 + o]
    else:   # t > 1
      words += tens[t] + " " + ones[o]

    if words.endswith('zero'):
        words = words[ : -len('zero') ]
    else:
        words += " "
     
    if words != "":
        words += suffixes[idx]

    # "" is returned if '000'
    # ends with " " for idx = 0
    return words.strip()

  
  token = str(int(token))
  length = len(token)
  
  if length>18:   # cannot handle currently
    # raise NotImplementedError
    return token
  
  idx = 0
  words = []
  
  for i in range(length-1, -1, -3):
    w = process(token[max(i-2,0) : i+1], idx)
    words.append(w) if w != "" else None
    idx += 1
  
  return " ".join(reversed(words)).strip()


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
      if rom_val[token[i]] > rom_val[token[i-1]]:
          int_val += rom_val[token[i]] - 2*rom_val[token[i-1]]
      else:
          int_val += rom_val[token[i]]
  return handle_number_to_words(int_val)


def is_abbreviation(token: str) -> bool:
  upper_lower = 0         # In abbreviations, upper>lower (observation)
  for ch in token:
    if ch.isupper():
      upper_lower+=1
    elif ch.islower():
      upper_lower-=1
  return len(token)>1 and ('.' in token or token.endswith("-") or upper_lower>0) and REGEX['abbreviation'].match(token);

def handle_abbreviation(token: str) -> str:
  ans = " ".join(list(token.replace(".","").replace("-","").replace(" ","").lower()))
  return ans if not token.endswith("s") else ans[:-2]+"'"+ans[-1]


def is_time(token: str) -> bool:
  return REGEX['time'].match(token)

def handle_time(token: str) -> str:
  token = re.sub(r"([0-9]{1,})\s*:\s*([0-5][0-9])",r" \1:\2 ",token).strip()
  token = re.sub(r"([0-9]{1,}:[0-5][0-9])\s*:\s*([0-5][0-9])",r" \1:\2 ",token).strip() # seconds
  tokens = token.split()
  times = tokens[0].split(':')

  token = [handle_number_to_words(times[0])]  # output

  if len(times)==3:
    token.append('hours') if token[-1] != "one" else token.append('hour')
    token.append(handle_number_to_words(times[1]))
    token.append('minutes and') if token[-1] != "one" else token.append('minute and')
    token.append(handle_number_to_words(times[2]))
    token.append('seconds') if token[-1] != "one" else token.append('second')
  elif int(times[0]) >= 24: # if hrs > 24 => countdown
    token.extend(['hours and', handle_number_to_words(times[1])])
    token.append('minutes') if token[-1] != "one" else token.append('minute')
  else:
    if times[1] == "00":
      if int(times[0]) > 12 or int(times[0]) == 0:
        token.append("hundred")
      elif "hr" in "".join(tokens).lower().replace(".",""):
        token.append("hundred")
      elif "am" not in "".join(tokens).lower().replace(".","").replace("amst","").replace("amt","") and "pm" not in "".join(tokens).lower().replace(".","").replace("pmdt","").replace("pmst","") and "noon" not in " ".join(tokens).lower() and "midnight" not in " ".join(tokens).lower():
        token.append("o'clock")
    else:
      token.append(handle_number_to_words(times[1]))


  for i in range(1,len(tokens)):
    if "hr" in tokens[i].lower().replace(".",""):
      token.append('hours')
    elif "noon" in tokens[i].lower().replace(".",""):
      token.append('noon')
    elif "midnight" in tokens[i].lower().replace(".",""):
      token.append('midnight')
    else:
      token.append(handle_abbreviation(tokens[i]))

  token = " ".join(token)
  return token


def is_date(token: str) -> bool:
  token = token.lower()
  return REGEX['date__wo_date'].match(token) or REGEX['date__wo_date_abbr'].match(token) or REGEX['date__wo_date_3'].match(token) or REGEX['date__wo_year'].match(token) or REGEX['date__wo_year_1'].match(token) or REGEX['date__wo_year_abbr'].match(token) or REGEX['date__wo_year_abbr_1'].match(token) or REGEX['date__wo_year_3'].match(token) or REGEX['date'].match(token) or REGEX['date_abbr'].match(token) or REGEX['date_1'].match(token) or REGEX['date_abbr_1'].match(token) or REGEX['date_2'].match(token) or REGEX['date_3'].match(token)

def preprocess_date(token: str) -> str:
  token = token.lower()
  if REGEX['date__wo_date'].match(token):
    return REGEX['date__wo_date'].sub(r"00 \1 \2",token)
  elif REGEX['date__wo_date_abbr'].match(token):
    s = REGEX['date__wo_date_abbr'].sub(r"00 \1 \2",token).split()
    for m in MONTHS:
      if m.startswith(s[1]):
        s[1] = m
        break
    return " ".join(s)
  elif REGEX['date__wo_date_3'].match(token):
    s = REGEX['date__wo_date_3'].sub(r"00 \1 \2",token).split()
    try:
      s[1] = MONTHS[int(s[1])-1]
      return " ".join(s)
    except:
      return token


  if REGEX['date__wo_year'].match(token):
    return REGEX['date__wo_year'].sub(r"\1 \3 0000",token)
  elif REGEX['date__wo_year_1'].match(token):
    return REGEX['date__wo_year_1'].sub(r"\1 \2 0000",token)
  elif REGEX['date__wo_year_abbr'].match(token):
    s = REGEX['date__wo_year_abbr'].sub(r"\1 \3 0000",token).split()
    for m in MONTHS:
      if m.startswith(s[1]):
        s[1] = m
        break
    return " ".join(s)
  elif REGEX['date__wo_year_abbr_1'].match(token):
    s = REGEX['date__wo_year_abbr_1'].sub(r"\1 \2 0000",token).split()
    for m in MONTHS:
      if m.startswith(s[0]):
        s[0] = m
        break
    return " ".join(s)
  elif REGEX['date__wo_year_3'].match(token):
    s = REGEX['date__wo_year_3'].sub(r"\1 \2 0000",token).split()
    if int(s[0]) > 12:
      try:
        s[1] = MONTHS[int(s[1])-1]
        return " ".join(s)
      except:
        return token
    else:
      try:
        s[0] = MONTHS[int(s[0])-1]
        return " ".join(s)
      except:
        return token

  if REGEX['date'].match(token):
    return REGEX['date'].sub(r"\1 \3 \4",token)
  elif REGEX['date_1'].match(token):
    return REGEX['date_1'].sub(r"\1 \2 \4",token)
  elif REGEX['date_abbr'].match(token):
    s = REGEX['date_abbr'].sub(r"\1 \3 \4",token).split()
    for m in MONTHS:
      if m.startswith(s[1]):
        s[1] = m
        break
    return " ".join(s)
  elif REGEX['date_abbr_1'].match(token):
    s = REGEX['date_abbr_1'].sub(r"\1 \2 \4",token).split()
    for m in MONTHS:
      if m.startswith(s[0]):
        s[0] = m
        break
    return " ".join(s)
  elif REGEX['date_2'].match(token):
    s = REGEX['date_2'].sub(r"\3 \2 \1",token).split()
    if int(s[1]) > 12:
      s[0],s[1] = s[1],s[0]
    try:
      s[1] = MONTHS[int(s[1])-1]
      return " ".join(s)
    except:
      return token
  elif REGEX['date_3'].match(token):
    s = REGEX['date_3'].sub(r"\1 \2 \3",token).split()
    if int(s[0]) > 12:
      try:
        s[1] = MONTHS[int(s[1])-1]
        return " ".join(s)
      except:
        return token
    else:
      try:
        s[0] = MONTHS[int(s[0])-1]
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
  
  MONTH_FIRST = False
  if not token[0].isdigit():
    MONTH_FIRST = True
  elif not REGEX['date'].match(token):
    return handle_number_spoken_as_digits(token)

  tokens = token.split()
  d = handle_ordinal_number(tokens[0] if not MONTH_FIRST else tokens[1], process=False) if tokens[0] != "00" else None
  m = tokens[1] if not MONTH_FIRST else tokens[0]
  y = handle_date__year(tokens[2]) if tokens[2] != "0000" else None

  # --00 thousand; 200- two thousand xx; 1908 --o--; 
  if MONTH_FIRST:
    if d is None:
      return " ".join([m,y])
    elif y is None:
      return " ".join([m,d])
    else:
      return " ".join([m,d,y])
  else:  
    if d is None:
      return " ".join([m,y])
    elif y is None:
      return " ".join(['the',d,'of',m])
    else:
      return " ".join(['the',d,'of',m,y])



def is_number_spoken_as_digits(token: str) -> bool:
  return "/" not in token and REGEX['number_by_digits'].match(token)

def handle_number_spoken_as_digits(token: str) -> str:
  ans = []
  for ch in token:
    if REGEX['punctuation'].match(ch):
      p = handle_punctuation(ch)
      ans.append(p) if len(ans)==0 or ans[-1]!=p else None
    else:
      try:
        ans.append(DIGITS[int(ch)])
      except IndexError:    # Shouldn't happen ideally
        p = "sil"
        ans.append(p) if len(ans)==0 or ans[-1]!=p else None
  return " ".join(ans)

def is_decimal_number_only(token: str) -> bool:
  return REGEX['decimal_number_only'].match(token.replace(" ",""))  # not match space 

def handle_decimal_number_only(token: str, process: bool = True) -> str:
  if process and re.match(r"^[1-9]\d\d\d$",token):  # probably a year (no comma!)
    return handle_date__year(token)
  elif process and token.startswith('0') and len(token) == 10 and ',' not in token and '.' not in token:  # probably to be read digit-wise (phone number, ...)
    return handle_number_spoken_as_digits(token)
  #elif process and len(token) == 10:  # phone number?
  #  return handle_number_spoken_as_digits(token)
  else:
    token = token.replace(",","").split(".")
    ans = []
    ans.append(handle_number_to_words(token[0])) if token[0] != "" else None
    if len(token) > 1:
      ans.append("point")
      if token[1] == "0":
        ans.append("zero")
      elif token[1] != "":
        ans.append(handle_number_spoken_as_digits(token[1]))
    return " ".join(ans)

def is_ordinal_number(token: str) -> bool:
  return REGEX['ordinal_number'].match(token.lower())

def handle_ordinal_number(token: str, process: bool = True) -> str:
  token = REGEX['ordinal_number'].sub(r"\1 \2",token.lower()).split()[0]
  if process:
    token = handle_decimal_number_only(token)
  else:
    token = handle_number_to_words(token)
  tokens = token.split()
  last = tokens[-1]
  try:
      last = ORDINALS[last]
  except KeyError:
      if last[-1] == "y":
          last = last[:-1] + "ie"
      last += "th"
  tokens[-1] = last
  return " ".join(tokens)


def is_fraction_only(token: str) -> bool:
  return REGEX['fraction_only'].match(token)

def handle_fraction_only(token: str) -> str:
  token = token.replace(",","").replace(" ","")

  n, d = token.split("/")
  if d == "2":
    d = "half"
  elif d == "4":
    d = "quarter"
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
    if f[4] in VOWELS:
      f = "an" + f[3:]
    else:
      f = "a" + f[3:]

  return f"{w} and {f}"

def is_currency(token: str) -> bool:
  return REGEX['currency'].match(token)

def handle_currency(token: str) -> str:
  tokens = REGEX['currency'].sub(r"\1;\2;\3",token).split(";")
  ans = []
  unit, val, suffix = CURRENCIES[tokens[0]], tokens[1], " ".join(tokens[2:]).lower()
  val = val.replace(" ","").replace(",","")

  if suffix == "":
    if "." in val:
      vals = val.split(".")
      i,f = "".join(vals[:-1]), vals[-1]
      f = f+"0" if len(f) == 1 else f
      ans.append(handle_number_to_words(i))
      ans.append(unit[0][0] if int(i)==1 else unit[0][1])
      ans.append("and")
      ans = [] if int(i)==0 else ans
      ans.append(handle_number_to_words(f))
      ans.append(unit[1][0] if int(f)==1 else unit[1][1])
    else:
      ans.append(handle_number_to_words(val))
      ans.append(unit[0][0] if int(val)==1 else unit[0][1])
  else:
    ans.append(handle_decimal_number_only(val, process=False))
    for s in CURRENCY_SUFFIXES:
      if suffix.replace(".","") == s:
        suffix = CURRENCY_SUFFIXES[s]
    ans.append(suffix)
    # ans.append(unit[0][0] if int(val)==1 else unit[0][1])
    ans.append(unit[0][1])

  return " ".join(ans)

def is_year_with_s(token: str) -> bool:
  return REGEX['year_with_s'].match(token)

def handle_year_with_s(token: str) -> str:
  token = REGEX['year_with_s'].sub(r"\1",token)
  token = handle_date__year(token)
  if token[-1] == "y":
    token = token[:-1] + "ies"
  elif token[-1] == "x":    # e.g., six
    token = token + "es"
  else:
    token = token + "s"
  return token

def is_measurement(token: str) -> bool:
  return REGEX['measurement'].match(token)

def handle_measurement(token: str) -> str:
  val, units = REGEX['measurement'].sub(r"\1;\2", token).split(";")
  val, units = val.strip().replace(",",""), units.strip().replace(".","").replace("-"," ")
  # print(f"\n{val}")
  ans = [handle_decimal_number_only(val, process=False)]
  units = units.split("/")
  units = [units[0], " ".join(units[1:])] if len(units) > 1 else [units[0]]  # XXX / YYY[/ZZZ...] => [XXX, YYY ZZZ]
  units_ans = []
  FIRST_UNIT = True
  unit_count = 0
  for unit in units:
    curr_units_ans = []
    unit = unit.strip().split()
    if unit_count==0:
      unit = reversed(unit)
    for u in unit:
      u = u.strip()
      curr_unit_words = ""
      if u[-1] in UNITS_SUFFIX.keys():
        curr_unit_words += UNITS_SUFFIX[u[-1]] + " "
        u = u[:-1]

      ## NOTE: `u` first to handle "p.m." case
      if u in UNITS:
        r = UNITS[u]
        r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]
        curr_unit_words += r
      elif u.lower() in UNITS:
        r = UNITS[u.lower()]
        r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]  
        curr_unit_words += r
      elif u[0] in UNITS_PREFIX.keys():
        p = UNITS_PREFIX[u[0]]
        if u[1:] in UNITS:
          r = UNITS[u[1:]]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0] 
          curr_unit_words += p+r
        elif u[1:].lower() in UNITS:
          r = UNITS[u[1:].lower()]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]  
          curr_unit_words += p+r

        elif u in UNITS:
          r = UNITS[u]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0] 
          curr_unit_words += r
        elif u.lower() in UNITS:
          r = UNITS[u.lower()]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]
          curr_unit_words += r
        else:
          curr_unit_words += u.lower()
      elif u[0].lower() in UNITS_PREFIX.keys():
        p = UNITS_PREFIX[u[0].lower()]
        if u[1:] in UNITS:
          r = UNITS[u[1:]]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]
          curr_unit_words += p+r
        elif u[1:].lower() in UNITS:
          r = UNITS[u[1:].lower()]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]
          curr_unit_words += p+r
        
        elif u in UNITS:
          r = UNITS[u]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]
          curr_unit_words += r
        elif u.lower() in UNITS:
          r = UNITS[u.lower()]
          r = (r[0] if float(val)==1 else r[1]) if FIRST_UNIT else r[0]
          curr_unit_words += r
        else:
          curr_unit_words += u.lower()

      else:
        curr_unit_words += u.lower()

      if unit_count > 0:
        units_ans.append(curr_unit_words.strip())
      else:
        curr_units_ans.append(curr_unit_words.strip())
      FIRST_UNIT = False if not FIRST_UNIT or (len(curr_units_ans)>0 and curr_units_ans[0]!="") else True

    if unit_count == 0:
      units_ans.append(" ".join(reversed(curr_units_ans)))
    unit_count+=1
  

  # print(units_ans)
  ans.append(" per ".join(units_ans))
  return re.sub(r"\s{2,}", " " , " ".join(ans)).strip()

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
  elif is_currency(token):
    return handle_currency(token)
  elif is_year_with_s(token):
    return handle_year_with_s(token)
  elif is_measurement(token):
    return handle_measurement(token)
  elif token[0] == "-":
    rec = to_spoken(token[1:])
    if rec == "<self>":
      return "<self>"
    elif rec == "sil":
      return "sil"
    else:
      return "minus " + rec     
  elif token[0] == "+":
    rec = to_spoken(token[1:])
    if rec == "<self>":
      return "<self>"
    elif rec == "sil":
      return "sil"
    else:
      return "plus " + rec
  elif "." in token and not token.endswith('.'):    ## TODO
    tokens = token.split(".")
    ans = []
    for t in tokens:
      if is_decimal_number_only(t):
        s = handle_decimal_number_only(t, process=False)
        if s == "zero":
          s = "o"
      else:
        s = t
      ans.append(s)
    return " dot ".join(ans).strip()
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

