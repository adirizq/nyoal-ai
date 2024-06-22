import re
import json
import requests


class SentenceSplitter:
    def __init__(self):
        self.acronym = [line.strip() for line in open('./resources/acronym.txt', 'r')]
        self.delimiter = [line.strip() for line in open('./resources/delimiter.txt', 'r')]


    def split_sentence(self, sentences):
        sentence_list = []
        sentence_buffer = ""
        sentences = sentences.replace("–", "-")
        sentences = re.sub("[^\x00-\x7F]", "", sentences)
        sentences = re.sub("\s+", " ", sentences)
        sentences = re.sub("\.\s*\.", ".", sentences)
        sentences = re.sub("\?\?+", "-", sentences)
        tokens = sentences.split(" ")

        for token in tokens:
            if not any(char in token for char in self.delimiter):
                sentence_buffer += token + " "
            elif any(char in token for char in self.delimiter):
                if token in self.acronym:
                    sentence_buffer += token + " "
                else:
                    last = token.rfind(".")
                    if last != -1:
                        token = token[:last] + "."
                    sentence_buffer += token + " "
                    sentence_list.append(sentence_buffer.strip())
                    sentence_buffer = ""

        if sentence_buffer:
            sentence_list.append(sentence_buffer + " .")

        return sentence_list
    

class ModelInference:
    def __init__(self, api_base_url: str):
        
        self.api_base_url = api_base_url
        self.sentence_splitter = SentenceSplitter()


    def split_sentence(self, sentence: str):
        return self.sentence_splitter.split_sentence(sentence)
    

    def predict(self, text: str):

        url = f"{self.api_base_url}/predict"

        headersList = {
            "Content-Type": "application/json" 
        }

        payload = json.dumps({
            "text": text
        })

        response = requests.post(url, data=payload,  headers=headersList)
        prediction = response.json()

        try:
            question = prediction['question']
            answer = prediction['answer']

            if question and answer:
                return {
                    "question": question,
                    "answer": answer
                }

            return None

        except:
            return None

