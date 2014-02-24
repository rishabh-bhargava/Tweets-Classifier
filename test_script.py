import project1_code as p1
from string import punctuation, digits


def extract_words(input_string):
    """
      Returns a list of lowercase words in a strong.
      Punctuation and digits are separated out into their own words.
    """


    for c in punctuation.replace('@', "") + digits :
        input_string = input_string.replace(c, "")

    print input_string
    splitted_string = input_string.lower().split()

    return [x for x in splitted_string if not (x.startswith("http") or x.startswith("@"))]

print extract_words("Lego Movie' Blocks Rivals to Lead Box Office @jhsdffor Third Weekend - Bloomberg http://t.co/YgpH0ZX3Nc")