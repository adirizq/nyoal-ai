import os
import sys

from model_inference import ModelInference
from dotenv import load_dotenv

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

load_dotenv()

inference = Blueprint('inference', __name__, template_folder='templates', url_prefix='/inference')

qag_model = ModelInference(
    project_id=os.getenv('MODEL_PROJECT_ID'),
    endpoint_id=os.getenv('MODEL_END_POINT_ID'),
)


@inference.route('/', methods=['POST'])
@login_required
def predict():
    if request.method == 'POST':
        context = request.get_json().get('context')
        sentences = qag_model.split_sentence(context)

        input_data = []
        for sentence in sentences:
            sentence_highlighted_context = context.replace(sentence, f'<hl>{sentence}<hl>')
            input_data.append(sentence_highlighted_context)

        prediction_results = []        
        for data in input_data:
            inference_result = qag_model.predict(data)
            prediction_results.append(inference_result)

        if all(result is None for result in prediction_results):
            return jsonify(message={'error': 'Server error'}, status="error"), 500

        return jsonify(message={'predictions': prediction_results}, status="success"), 200
        