from datetime import datetime
from distutils.util import convert_path
import locale

class dates:
    def __init__(self):
        pass

    @staticmethod
    def date2text(date):
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
        date = datetime.strptime(date, "%d/%m/%Y")
        converted_date = date.strftime("%d de %B de %Y")
        return converted_date

    def convert_Cap(self, txt):
        words = txt.split(" ")
        convert_words = []
        for word in words:
            convert_words.append(word.capitalize())
        
        return " ".join(convert_words)



# date_instance = dates()
# converted_date = date_instance.date2text("26/05/2023")
# print(converted_date)