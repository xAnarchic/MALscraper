import pandas as pd
import numpy as np
import csv
import re

genres = str('["hello?", "jomi", "opnok"]')
print(genres.translate(str.maketrans('', '', '"?,][')))
length = len(genres)
print(genres.strip()[2: length-2])
print(genres[2: (length-2)])
genres = genres.strip("]")
print(genres)
genres = re.sub("[ [ ]", '', genres)
print(genres)


