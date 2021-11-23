from bs4 import BeautifulSoup
import requests
import pymorphy2
import re

def antonymize_text(given_text):
    text = re.findall(r'\w+', given_text)
    url = "https://antonimy-k-slovu.ru/"
    result_text = ""
    for word_ in text:
        morph = pymorphy2.MorphAnalyzer()
        word = morph.parse(word_)[0]
        word = str(word.normal_form)
        data = {'filter[search]': word}
        response = requests.post(url + word, data=data)
        soup = BeautifulSoup(response.content,"lxml")
        res = soup.findAll("div", {"class": "subword"})
        if res == []:
            result_text += word
            result_text += " "
        else:
            for elem in res:
                if elem.a:
                    result_text += re.findall(r'\w+', elem.text)[0]
                    result_text += " "
                    break
    return result_text
