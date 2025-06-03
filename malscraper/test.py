import pandas as pd
import numpy as np
import csv
import re
import sys

# genres = str('["hello?", "jomi", "opnok"]')
# print(genres.translate(str.maketrans('', '', '"?,][')))
# length = len(genres)
# print(genres.strip()[2: length-2])
# print(genres[2: (length-2)])
# genres = genres.strip("]")
# print(genres)
# genres = re.sub("[ [ ]", '', genres)
# print(genres)


# desc = response.css('p[itemprop=description] br::text').getall()


#x.translate(str.maketrans('', '', '\n\r'))

test = ("Frieren: Beyond Journey's End",)
print((test[0]))

check = ['hello1']
print(type('-'.join(check)))

if re.search('^\n..[a-z]+.[0-9]+..[0-9]+', '\n  Dec 17, 2022\n  ', flags=re.IGNORECASE) is not None:
    print('True')
else:
    print('False')
sys.exit()

print(150%29)

