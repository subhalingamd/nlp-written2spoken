from run_assignment1 import *

def test_self():
	assert to_spoken("Hi") == "<self>"

def test_sil():
	assert to_spoken(".") == "sil"
	assert to_spoken(",") == "sil"
	assert to_spoken("(") == "sil"
	assert to_spoken("Hi") != "sil"

def test_roman():
	assert to_spoken("II") == "two"
	assert to_spoken("VII") == "seven"
	assert to_spoken("CD") == "c d"

def test_abbreviation():
	assert to_spoken("U.S.") == "u s"
	assert to_spoken("F.") == "f"
	assert to_spoken("F") == "<self>"
	assert to_spoken("ISBN") == "i s b n"

	assert to_spoken("am") == "<self>"
	assert to_spoken("AlphaZeta") == "<self>"

	assert to_spoken("IISc.") == "i i s c"
	assert to_spoken("a.m.") == "a m"
	
	assert to_spoken("IIT") == "i i t"
	
	assert to_spoken("asCII") == "a s c i i"
	assert to_spoken("It") == "<self>"

	assert to_spoken("US-") == "u s"
	assert to_spoken("IITs") == "i i t's"

def test_time():
	assert to_spoken("00:00") == "zero hundred"
	assert to_spoken("9:00") == "nine o'clock"
	assert to_spoken("10:05") == "ten five"
	assert to_spoken("11:30") == "eleven thirty"
	assert to_spoken("12:00") == "twelve o'clock"
	assert to_spoken("19:00") == "nineteen hundred"
	assert to_spoken("06:00pm") == "six p m"
	assert to_spoken("06:00p m.") == "six p m"
	assert to_spoken("12:30p.m.") == "twelve thirty p m"
	assert to_spoken("1:00 am") == "one a m"
	assert to_spoken("02:00 a.m.") == "two a m"
	assert to_spoken("03:00 AM IST") == "three a m i s t"
	assert to_spoken("04:30 P.M. IST") == "four thirty p m i s t"
	assert to_spoken("20:30 hrs") == "twenty thirty hours"
	assert to_spoken("6:00 hrs IST") == "six hundred hours i s t"
	assert to_spoken("7:00hrs. IST") == "seven hundred hours i s t"

	assert to_spoken("6:00:00") == "six hours zero minutes and zero seconds"
	assert to_spoken("6:20:56") == "six hours twenty minutes and fifty six seconds"
	assert to_spoken("48:00") == "forty eight hours and zero minutes"
	assert to_spoken("36:11") == "thirty six hours and eleven minutes"


def test_handle_number_to_words():
	assert handle_number_to_words("0") == "zero"
	assert handle_number_to_words("1") == "one"
	assert handle_number_to_words("11") == "eleven"
	assert handle_number_to_words("50") == "fifty"
	assert handle_number_to_words("100") == "one hundred"
	assert handle_number_to_words("110") == "one hundred ten"
	assert handle_number_to_words("101") == "one hundred one"
	assert handle_number_to_words("1234") == "one thousand two hundred thirty four"
	assert handle_number_to_words("123456") == "one hundred twenty three thousand four hundred fifty six"
	assert handle_number_to_words("987654321") == "nine hundred eighty seven million six hundred fifty four thousand three hundred twenty one"
	assert handle_number_to_words("9780252076725") == "nine trillion seven hundred eighty billion two hundred fifty two million seventy six thousand seven hundred twenty five"


def test_preprocess_date():
	assert preprocess_date("31 January 1900") == "31 january 1900"
	assert preprocess_date("6th July 2021") == "6 july 2021"
	assert preprocess_date("14 th February, 2020") == "14 february 2020"
	assert preprocess_date("August 20, 2020") == "august 20 2020"
	assert preprocess_date("May 21st, 1854") == "may 21 1854"
	assert preprocess_date("July 20  , '20") == "july 20 '20"

	assert preprocess_date("11 Dec., 2010") == "11 december 2010"
	assert preprocess_date("10.Nov.1893") == "10 november 1893"
	assert preprocess_date("5th Jun., 1987") == "5 june 1987"
	assert preprocess_date("7th Jun, 1987") == "7 june 1987"
	assert preprocess_date("15th.Aug.1947") == "15 august 1947"

	assert preprocess_date("Jun 1st, 2012") == "june 1 2012"
	assert preprocess_date("Mar. 3rd 2009") == "march 3 2009"
	assert preprocess_date("Jan.26.1950") == "january 26 1950"
	assert preprocess_date("Apr.13th.1908") == "april 13 1908"

	assert preprocess_date("2004-03-01") == "01 march 2004"
	assert preprocess_date("2004/03.01") == "01 march 2004"
	assert preprocess_date("2004 / 3 / 1") == "1 march 2004"
	assert preprocess_date("2004 / 31 / 1") == "31 january 2004"

	assert preprocess_date("01-03-1956") == "january 03 1956"
	assert preprocess_date("1/03.1956") == "january 03 1956"
	assert preprocess_date("1 / 3 / 1956") == "january 3 1956"
	assert preprocess_date("31 / 01 / 1956") == "31 january 1956"
	assert preprocess_date("13-32-1956") == "13-32-1956"
	assert preprocess_date("12-32-1956") == "december 32 1956"


	assert preprocess_date("1st September 900") == "1 september 900"
	assert preprocess_date("1 Sept., 900") == "1 september 900"
	assert preprocess_date("September 1st, 900") == "september 1 900"
	assert preprocess_date("Sept 1, 900") == "september 1 900"
	assert preprocess_date("900-9-1") == "1 september 900"
	assert preprocess_date("1.9.900") == "january 9 900"

	assert preprocess_date("September, 2000") == "00 september 2000"
	assert preprocess_date("Jul., 2014") == "00 july 2014"

	assert preprocess_date("9th August") == "9 august 0000"
	assert preprocess_date("March 9") == "march 9 0000"
	assert preprocess_date("March 9th") == "march 9 0000"
	assert preprocess_date("21st Dec.") == "21 december 0000"
	assert preprocess_date("Oct. 05") == "october 05 0000"
	assert preprocess_date("Oct 3rd") == "october 3 0000"

	#assert preprocess_date("08 / 2000") == "00 august 2000"
	assert preprocess_date("08-2000") == "00 august 2000"
	assert preprocess_date("14-2099") == "14-2099"
	#assert preprocess_date("9/11") == "september 11 0000"
	assert preprocess_date("9-11") == "september 11 0000"
	assert preprocess_date("26-10") == "26 october 0000"
	assert preprocess_date("26-14") == "26-14"


def test_handle_date__year():
	assert handle_date__year("2000") == "two thousand"
	assert handle_date__year("1000") == "one thousand"
	assert handle_date__year("1200") == "twelve hundred"
	assert handle_date__year("2100") == "twenty one hundred"
	assert handle_date__year("2006") == "two thousand six"
	assert handle_date__year("2010") == "twenty ten"
	assert handle_date__year("1201") == "twelve o one"
	assert handle_date__year("1950") == "nineteen fifty"
	assert handle_date__year("1198") == "eleven ninety eight"
	assert handle_date__year("2014") == "twenty fourteen"
	assert handle_date__year("2010") == "twenty ten"
	assert handle_date__year("1999") == "nineteen ninety nine"
	
	assert handle_date__year("900") == "nine hundred"
	assert handle_date__year("'20") == "twenty"



def test_handle_date():
	assert to_spoken("14th February 2000") == "the fourteenth of february two thousand"
	assert to_spoken("Oct. 2, 1950") == "october second nineteen fifty"
	assert to_spoken("May 29, 2013") == "may twenty ninth twenty thirteen"
	assert to_spoken("January 14, 2008") == "january fourteenth two thousand eight"
	#assert to_spoken("January, 2008") == "january two thousand eight"
	assert to_spoken("2009-11-08") == "the eighth of november two thousand nine"
	assert to_spoken("1|5|1907") == "january fifth nineteen o seven"

	assert handle_date("2008-13-21") == handle_number_spoken_as_digits("2008-13-21") == to_spoken("2008-13-21") == "two o o eight sil one three sil two one"
	assert handle_date("21/13/2008") == handle_number_spoken_as_digits("21/13/2008") == to_spoken("21/13/2008") == "two one sil one three sil two o o eight"
	
	assert to_spoken("March 2011") == "march twenty eleven"
	assert to_spoken("Jun. 2005") == "june two thousand five"
	assert to_spoken("August 17") == "august seventeenth"

	assert to_spoken("08 - 2000") == "august two thousand"
	assert to_spoken("14-2099") == "one four sil two o nine nine"
	assert to_spoken("9-11") == "september eleventh"
	assert to_spoken("26-10") == "the twenty sixth of october"
	assert to_spoken("26-14") == "two six sil one four"

	## TODO::
	assert to_spoken("21 janu 2008") == "<self>"

def test_is_number_spoken_as_digits():
	assert is_number_spoken_as_digits("1 1/2") == False
	#assert is_number_spoken_as_digits("(+91) 98") == True
	assert is_number_spoken_as_digits("(91) 98") is not None
	assert is_number_spoken_as_digits("9876-87") is not None
	assert is_number_spoken_as_digits("9876 87") is not None
	assert is_number_spoken_as_digits("9876 (87)") is not None


def test_handle_number_spoken_as_digits():
	assert to_spoken("978-0-304-35252-4") == "nine seven eight sil o sil three o four sil three five two five two sil four"
	assert to_spoken("0-8387-1972-4") == "o sil eight three eight seven sil one nine seven two sil four"
	assert to_spoken("0 7506 0625 8") == "o sil seven five o six sil o six two five sil eight"
	assert to_spoken("978-0753508220") == "nine seven eight sil o seven five three five o eight two two o"
	assert to_spoken("106 (2003) 203-214") == "one o six sil two o o three sil two o three sil two one four"
	assert to_spoken("0 521 400775") == "o sil five two one sil four o o seven seven five"
	assert to_spoken("84-933702-1-5") == "eight four sil nine three three seven o two sil one sil five"


def test_handle_decimal_number_only():
	assert handle_decimal_number_only("1836") == to_spoken("1836") == "eighteen thirty six"
	assert handle_decimal_number_only("1601") == to_spoken("1601") ==  "sixteen o one"
	assert handle_decimal_number_only("2006") == to_spoken("2006") ==  "two thousand six"
	assert handle_decimal_number_only("1,054") == to_spoken("1,054") ==  "one thousand fifty four"
	assert handle_decimal_number_only("1,000") == to_spoken("1,000") ==  "one thousand"
	assert handle_decimal_number_only("2000") == to_spoken("2000") ==  "two thousand"
	assert handle_decimal_number_only("2,587") == to_spoken("2,587") ==  "two thousand five hundred eighty seven"

	assert handle_decimal_number_only("07") == to_spoken("07") == "seven"
	assert handle_decimal_number_only("0252076729") == to_spoken("0252076729") == "o two five two o seven six seven two nine"


	assert handle_decimal_number_only("62.0") == to_spoken("62.0") == "sixty two point zero"
	assert handle_decimal_number_only("62.") == to_spoken("62.") == "sixty two point"
	assert handle_decimal_number_only("1,565.0") == to_spoken("1,565.0") == "one thousand five hundred sixty five point zero"
	assert handle_decimal_number_only("0.88") == to_spoken("0.88") == "zero point eight eight"
	assert handle_decimal_number_only(".88") == to_spoken(".88") == "point eight eight"

	assert handle_decimal_number_only("12,000") == to_spoken("12,000") == "twelve thousand"
	assert handle_decimal_number_only("3.14") == to_spoken("3.14") == "three point one four"
	assert handle_decimal_number_only("100") == to_spoken("100") == "one hundred"
	assert handle_decimal_number_only("102.1") == to_spoken("102.1") == "one hundred two point one"
	assert handle_decimal_number_only("9780252076725") == to_spoken("9780252076725") == "nine trillion seven hundred eighty billion two hundred fifty two million seventy six thousand seven hundred twenty five"
	assert handle_decimal_number_only("900,000") == to_spoken("900,000") == "nine hundred thousand"
	assert handle_decimal_number_only("25.520") == to_spoken("25.520") == "twenty five point five two o"
	assert handle_decimal_number_only("4") == to_spoken("4") == "four"
	assert handle_decimal_number_only("55527") == to_spoken("55527") == "fifty five thousand five hundred twenty seven"
	assert handle_decimal_number_only("13.0088") == to_spoken("13.0088") == "thirteen point o o eight eight"
	assert handle_decimal_number_only("1000000000001") == to_spoken("1000000000001") == "one trillion one"

def test_is_ordinal_number():
	assert is_ordinal_number("1") is None
	assert is_ordinal_number("1st") is not None
	assert is_ordinal_number("12th") is not None
	assert is_ordinal_number("23rd") is not None
	assert is_ordinal_number("1,982rd") is not None
	assert is_ordinal_number("1230 th") is not None

def test_handle_ordinal_number():
	assert handle_ordinal_number("1") == "first"
	assert handle_ordinal_number("2nd") == to_spoken("2nd") == "second"
	assert handle_ordinal_number("23rd") == to_spoken("23rd") == "twenty third"
	assert handle_ordinal_number("50th") == to_spoken("50th") == "fiftieth"
	assert handle_ordinal_number("11th") == to_spoken("11th") == "eleventh"
	assert handle_ordinal_number("12") == "twelfth"
	assert handle_ordinal_number("28") == "twenty eighth"
	assert handle_ordinal_number("1,805th") == to_spoken("1,805th") == "one thousand eight hundred fifth"
	assert handle_ordinal_number("1859") == "eighteen fifty ninth"

def test_is_fraction_only():
	assert is_fraction_only("1/2/2") is None
	assert is_fraction_only("1,200/2") is not None
	assert is_fraction_only("1/2,000") is not None
	assert is_fraction_only("1 /  2,000") is not None
	assert is_fraction_only("1.0/200") is None


def test_handle_fraction_only():
	assert handle_fraction_only("1/2") == to_spoken("1/2") == "one half" ## check TODO
	assert handle_fraction_only("3/4") == to_spoken("3/4") == "three quarters"
	assert handle_fraction_only("2/3") == to_spoken("2/3") == "two thirds"
	assert handle_fraction_only("1/10") == to_spoken("1/10") == "one tenth"
	assert handle_fraction_only("917/20") == to_spoken("917/20") == "nine hundred seventeen twentieths"
	assert handle_fraction_only("7/281") == to_spoken("7/281") == "seven two hundred eighty firsts"
	assert handle_fraction_only("4/12") == to_spoken("4/12") == "four twelfths"


def test_handle_mixed_fraction():
	assert handle_mixed_fraction("38 57/64") == to_spoken("38 57/64") == "thirty eight and fifty seven sixty fourths"
	assert handle_mixed_fraction("1 1/2") == to_spoken("1 1/2") == "one and a half"
	assert handle_mixed_fraction("2 1/8") == to_spoken("2 1/8") == "two and an eighth"


def test_is_currency():
	assert is_currency("€5.7 million") is not None
	assert is_currency("$10 million") is not None
	assert is_currency("Re. 1 . 00") is not None
	assert is_currency("Rs 1, 000.56") is not None
	assert is_currency("$15 million") is not None
	assert is_currency("$ 1.2m") is not None
	assert is_currency("Rs 1,234 cr") is not None

	assert is_currency("$250M") is not None

def test_handle_currency():
	assert handle_currency("$1") == "one dollar" == to_spoken("$1")
	assert handle_currency("$ 1 . 01") == "one dollar and one cent" == to_spoken("$ 1 . 01")
	assert handle_currency("$0. 11") == "eleven cents" == to_spoken("$0. 11")
	assert handle_currency("€ 2020") == "two thousand twenty euros" == to_spoken("€ 2020")
	assert handle_currency("€  1 m") == "one million euros" == to_spoken("€  1 m")

	assert handle_currency("£ 1.12k") == "one point one two thousand pounds" == to_spoken("£ 1.12k")
	assert handle_currency("£ 1.40") == "one pound and forty pence" == to_spoken("£ 1.40")
	assert handle_currency("Rs. 15crore") == "fifteen crore rupees" == to_spoken("Rs. 15crore")
	assert handle_currency("Rs. 1,000.20") == "one thousand rupees and twenty paise" == to_spoken("Rs. 1,000.20")

	assert handle_currency("$ 1.1") == "one dollar and ten cents" == to_spoken("$ 1.1")
	assert handle_currency("$ 1.0") == "one dollar and zero cents" == to_spoken("$ 1.0")

	assert handle_currency("€5.7 million") == "five point seven million euros" == to_spoken("€5.7 million")
	assert handle_currency("$39,844") == "thirty nine thousand eight hundred forty four dollars" == to_spoken("$39,844")
	assert handle_currency("$900,000") == "nine hundred thousand dollars" == to_spoken("$900,000")
	assert handle_currency("$1.2 million") == "one point two million dollars" == to_spoken("$1.2 million")
	assert handle_currency("Rs 1,000 cr") == "one thousand crore rupees" == to_spoken("Rs 1,000 cr")
	
	assert handle_currency("$250M") == "two hundred fifty million dollars" == to_spoken("$250M")


def test_is_year_with_s():
	assert is_year_with_s("1940s") is not None
	assert is_year_with_s("1941st") is None

def test_handle_year_with_s():
	assert handle_year_with_s("1940s") == to_spoken("1940s") == "nineteen forties"
	assert handle_year_with_s("1900s") == to_spoken("1900s") == "nineteen hundreds"


def test_is_measurement():
	assert is_measurement("0.22%") is not None
	assert is_measurement("15 m") is not None
	assert is_measurement("604.2 /km²") is not None
	assert is_measurement("1,570 mm") is not None
	assert is_measurement("100Gb/s") is not None
	assert is_measurement("1 percent") is not None

def test_handle_measurement():
	assert handle_measurement("57 percent") == "fifty seven percent" == to_spoken("57 percent")
	assert handle_measurement("99.05%") == "ninety nine point o five percent" == to_spoken("99.05%")
	assert handle_measurement("7/km²") == "seven per square kilometers" == to_spoken("7/km²")
	assert handle_measurement("1,908 mi") == "one thousand nine hundred eight miles" == to_spoken("1,908 mi")
	assert handle_measurement("179.4 / km2 ") == "one hundred seventy nine point four per square kilometers" == to_spoken("179.4 / km2 ")
	assert handle_measurement("9 PM") == "nine p m" == to_spoken("9 PM")
	assert handle_measurement("8 a.m.") == "eight a m" == to_spoken("8 a.m. ")
	assert handle_measurement("11 cm") == "eleven centimeters" == to_spoken("11 cm")
	assert handle_measurement("1,047ha ") == "one thousand forty seven hectares" == to_spoken("1,047ha ")
	assert handle_measurement("7.5KB") == "seven point five kilobytes" == to_spoken("7.5KB")
	assert handle_measurement("100Gb/s") == "one hundred gigabits per second" == to_spoken("100Gb/s")
	assert handle_measurement("3,070 km") == "three thousand seventy kilometers" == to_spoken("3,070 km")
	assert handle_measurement("11 m") == "eleven meters" == to_spoken("11 m")
	assert handle_measurement("101 s") == "one hundred one seconds" == to_spoken("101 s")
	assert handle_measurement("101ms") == "one hundred one milliseconds" == to_spoken("101 ms")
	assert handle_measurement("44.1 kHz") == "forty four point one kilohertz" == to_spoken("44.1 kHz")
	assert handle_measurement("101 KHz") == "one hundred one kilohertz" == to_spoken("101 KHz")
	assert handle_measurement("40°C") == "forty degrees celsius" == to_spoken("40°C")
	assert handle_measurement("1,500 K") == "one thousand five hundred kelvins" == to_spoken("1,500 K")
	assert handle_measurement("101 cu. cm") == "one hundred one cubic centimeters" == to_spoken("101 cu. cm")

	assert handle_measurement("9.8 m / s2") == "nine point eight meters per square second" == to_spoken("9.8 m / s2")
	assert handle_measurement("1000 kg/m³") == "one thousand kilograms per cubic meter" == to_spoken("1000 kg/m³")
	assert handle_measurement("1g/l") == "one gram per liter" == to_spoken("1g/l")
	assert handle_measurement("1.23 kg m") == "one point two three kilograms meters" == to_spoken("1.23 kg m")
	assert handle_measurement("1 Newton /s") == "one newton per second" == to_spoken("1 Newton /s")


def test_plus_minus():
	assert to_spoken("- 3/5") == "minus three fifths"
	assert to_spoken("- 2,020") == "minus two thousand twenty"
	# assert to_spoken("- 2020") == "minus two thousand twenty"
	assert to_spoken("-4 3/5") == "minus four and three fifths"
	assert to_spoken(" +3.14") == "plus three point one four"



def test_assignment_examples():
	assert to_spoken("U.S") == "u s" == to_spoken("US")
	
	assert to_spoken("29 March 2012") == "the twenty ninth of march twenty twelve"
	assert to_spoken("2011-01-25") == "the twenty fifth of january twenty eleven"

	assert to_spoken("04:40 PM") == "four forty p m"
	assert to_spoken("21:30:12") == "twenty one hours thirty minutes and twelve seconds"

	assert to_spoken("10345") == "ten thousand three hundred forty five"
	assert to_spoken("24349943") == "twenty four million three hundred forty nine thousand nine hundred forty three"
	assert to_spoken("184.33") == "one hundred eighty four point three three"
	assert to_spoken("-20") == "minus twenty"

	assert to_spoken("53.77 mm") == "fifty three point seven seven millimeters"
	assert to_spoken("3 mA") == "three milliamperes"
	assert to_spoken("14 sq m") == "fourteen square meters"

	assert to_spoken("$15.24") == "fifteen dollars and twenty four cents"
	assert to_spoken("£11") == "eleven pounds"

