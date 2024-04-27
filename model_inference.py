import re

from typing import Dict, List, Union

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


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
    def __init__(self, 
                 project_id: str, 
                 endpoint_id: str,
                 location: str = "asia-southeast1",
                 api_endpoint: str = "asia-southeast1-aiplatform.googleapis.com"):
        
        self.project_id = project_id
        self.endpoint_id = endpoint_id
        self.location = location
        self.api_endpoint = api_endpoint

        self.client_options = {"api_endpoint": self.api_endpoint}
        self.client = aiplatform.gapic.PredictionServiceClient(client_options=self.client_options)

        self.sentence_splitter = SentenceSplitter()


    def split_sentence(self, sentence: str):
        return self.sentence_splitter.split_sentence(sentence)
    

    def predict(self, instances: Union[Dict, List[Dict]]):
        instances = instances if isinstance(instances, list) else [instances]
        instances = [
            json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
        ]
        parameters_dict = {}
        parameters = json_format.ParseDict(parameters_dict, Value())
        endpoint = self.client.endpoint_path(
            project=self.project_id, location=self.location, endpoint=self.endpoint_id
        )
        response = self.client.predict(
            endpoint=endpoint, instances=instances, parameters=parameters
        )

        prediction = response.predictions[0][0]['generated_text']

        try:
            question = prediction.split("pertanyaan:")[1].split(" jawaban:")[0]
            answer = prediction.split("jawaban:")[1]

            if question and answer:
                return {
                    "question": question,
                    "answer": answer
                }

            return None
        
        except:
            return None
    

