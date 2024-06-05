from models.qa_pack import QAPack, QA
from models.tag import Tag

from flask import Blueprint, render_template, redirect, request, flash, url_for, jsonify, send_file
from flask_login import login_required, current_user

qa_pack = Blueprint('qa_pack', __name__, template_folder='templates', url_prefix='/dashboard/qa_pack')


@qa_pack.route('/detail/<string:id>')
@login_required
def detail(id):
    qa_pack, qa_pack_tags = QAPack.get_by_id(id)
    tags = Tag.get_all_dict(current_user)
    title = 'paket_soal'
    return render_template('dashboard/qa_pack_detail.html', title=title, qa_pack=qa_pack, qa_pack_tags=qa_pack_tags, tags=tags)


@qa_pack.route('/get-general-info/<string:id>', methods=['GET'])
@login_required
def get_general_info(id):
    qa_pack, qa_pack_tags = QAPack.get_by_id(id)
    qa_pack_tags = [{'name': tag.name, 'color': tag.color} for tag in qa_pack_tags]

    return jsonify(name=qa_pack.name, tags=qa_pack_tags, total_qas=qa_pack.total_qas, status="success"), 200


@qa_pack.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form['name']
    tags_id = request.form.getlist('tags_id')

    try:
        qa_pack = QAPack(name = name, tags_id = tags_id)
        qa_pack.save(current_user)

        flash('Paket soal berhasil dibuat', 'success')
        return redirect(url_for('dashboard.qa_pack'))

    except Exception as e:
        print('[ERROR] [CREATE QA PACK]: ', e)
        flash('Terjadi kesalahan server saat membuat paket soal', 'error')
        return redirect(url_for('dashboard.qa_pack'))


@qa_pack.route('/update-general-info', methods=['POST'])
@login_required
def update_general_info():
    qa_pack_id = request.get_json().get('qa_pack_id')
    name = request.get_json().get('name')
    tags_id = request.get_json().get('tags_id')

    try:
        qa_pack = QAPack(id=qa_pack_id, name=name, tags_id=tags_id)
        qa_pack.update()

        return jsonify(message='Informasi paket soal berhasil diubah', status="success"), 200
        
    except Exception as e:
        print('[ERROR] [UPDATE QA PACK GENERAL INFO]: ', e)
        return jsonify(message='Terjadi kesalahan server saat mengubah informasi paket soal', status="error"), 500


@qa_pack.route('/update-qa', methods=['POST'])
@login_required
def update_qa():
    qa_pack_id = request.get_json().get('qa_pack_id')
    qas_data = request.get_json().get('data')

    qas = []
    for qa_data in qas_data:
        if qa_data['question'] == '' or qa_data['answer'] == '':
            continue
        qa = QA(id=qa_data['id'], question=qa_data['question'], answer=qa_data['answer'])
        qas.append(qa)

    try:
        qa_pack = QAPack(id=qa_pack_id, name=None, qas=qas)
        qa_pack.update_qas()

        return jsonify(message='Pertanyaan dan jawaban berhasil disimpan', status="success"), 200

    except Exception as e:
        print('[ERROR] [UPDATE QA]: ', e)
        return jsonify(message='Terjadi kesalahan server saat menyimpan pertanyaan dan jawaban', status="error"), 500


@qa_pack.route('/delete', methods=['POST'])
@login_required
def delete():
    qa_pack_id = request.form['qa_pack_id']

    try:
        qa_pack = QAPack(id=qa_pack_id, name=None)
        qa_pack.delete()

        flash('Paket soal berhasil dihapus', 'success')
        return redirect(request.referrer, code=302)
    
    except Exception as e:
        print('[ERROR] [DELETE QA PACK]: ', e)
        flash('Terjadi kesalahan server saat menghapus paket soal', 'error')
        return redirect(request.referrer, code=302)
    

@qa_pack.route('/export-docx', methods=['POST'])
@login_required
def export_docx():
    qa_pack_id = request.get_json().get('qa_pack_id')

    try:
        qa_pack = QAPack.get_by_id_no_tags(qa_pack_id)
        docx_path = qa_pack.export_docx()
        return jsonify(message=qa_pack.name, status="success"), 200
    
    except Exception as e:
        print('[ERROR] [EXPORT DOCX]: ', e)
        return jsonify(message='Terjadi kesalahan server saat export docx', status="error"), 500
    

@qa_pack.route('/export-pdf', methods=['POST'])
@login_required
def export_pdf():
    qa_pack_id = request.get_json().get('qa_pack_id')

    try:
        qa_pack = QAPack.get_by_id_no_tags(qa_pack_id)
        docx_path = qa_pack.export_pdf()
        return jsonify(message=qa_pack.name, status="success"), 200
    
    except Exception as e:
        print('[ERROR] [EXPORT PDF]: ', e)
        return jsonify(message='Terjadi kesalahan server saat export PDF', status="error"), 500
    

@qa_pack.route('/export-gift', methods=['POST'])
@login_required
def export_gift():
    qa_pack_id = request.get_json().get('qa_pack_id')

    try:
        qa_pack = QAPack.get_by_id_no_tags(qa_pack_id)
        docx_path = qa_pack.export_gift()
        return jsonify(message=qa_pack.name, status="success"), 200
    
    except Exception as e:
        print('[ERROR] [EXPORT PDF]: ', e)
        return jsonify(message='Terjadi kesalahan server saat export Moodle GIFT', status="error"), 500
    

@qa_pack.route('/download-export/<string:file_type>/<string:name>', methods=['GET'])
@login_required
def download_export(file_type, name):
    try:
        if file_type == 'docx':
            return send_file('./export/export.docx', as_attachment=True, download_name=name + '.docx')
        
        elif file_type == 'pdf':
            return send_file('./export/export.pdf', as_attachment=True, download_name=name + '.pdf')
        
        elif file_type == 'gift':
            return send_file('./export/export.txt', as_attachment=True, download_name=name + '.txt')
        
        else:
            return jsonify(message='Tipe file tidak ditemukan', status="error"), 404
    
    except Exception as e:
        print('[ERROR] [DOWNLOAD EXPORT]: ', e)
        return jsonify(message='Terjadi kesalahan server saat download file', status="error"), 500