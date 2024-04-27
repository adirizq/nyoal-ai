import os
import sys

from model_inference import ModelInference
from dotenv import load_dotenv

from flask import Blueprint, render_template, request
from flask_login import login_required

load_dotenv()

dashboard = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/dashboard')

model_inference = ModelInference(
    project_id=os.getenv('MODEL_PROJECT_ID'),
    endpoint_id=os.getenv('MODEL_END_POINT_ID'),
)

@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        context = request.form['context']
        sentences = model_inference.split_sentence(context)

        input_data = []
        for sentence in sentences:
            sentence_highlighted_context = context.replace(sentence, f'<hl>{sentence}<hl>')
            input_data.append(sentence_highlighted_context)

        prediction_results = []        
        for data in input_data:
            inference_result = model_inference.predict(data)
            prediction_results.append(inference_result)

        return render_template('dashboard/index.html', predictions=prediction_results, context=context)

    title = 'uji_coba'
    return render_template('dashboard/index.html', title=title)


@dashboard.route('/qa-pack')
@login_required
def qa_pack():
    title = 'paket_soal'
    return render_template('dashboard/qa_pack.html', title=title)


@dashboard.route('/tag')
@login_required
def tag():
    title = 'tag'
    return render_template('dashboard/tag.html', title=title)