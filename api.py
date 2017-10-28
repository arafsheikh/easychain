import jsonify

from flask import Flask, request
from blockchain import Blockchain, Block, Message

chain = None
app = Flask(__name__)


def create_app():
    global chain
    chain = Blockchain()
    return app


@app.route('/addPatient', methods=['POST'])
def add_patient():
    digital_id = request.form['id']  # Make using public and private keys
    age = request.form['age']
    blood_group = request.form['blood_group']
    allergies = request.form['allergies']
    genetic_problems = request.form['genetic_problems']

    block = Block()
    block.add_message(Message(digital_id))
    block.add_message(Message(age))
    block.add_message(Message(blood_group))
    block.add_message(Message(allergies))
    block.add_message(Message(genetic_problems))
    block.seal()

    chain.add_block(block)

    return jsonify({'status': 'success'})


@app.route('/addRecord', methods=['POST'])
def add_record():
    digital_id = request.form['id']
    rec_type = request.form['record_type']
    hash = request.form['hash']
    accessible_by = request.form['accessible_by']
    datacenter = request.form['datacenter']

    block = Block()
    block.add_message(Message(digital_id))
    block.add_message(Message(rec_type))
    block.add_message(Message(hash))
    block.add_message(Message(accessible_by))
    block.add_message(Message(datacenter))
    block.seal()
    chain.add_block(block)

    return jsonify({'status': 'success'})


@app.route('/fetchRecord', methods=['POST'])
def fetch_record():
    digital_id = request.form['id']

    records = []

    blocks = chain.get_blocks()
    for block in blocks:
        for message in block.get_messages():
            if message.get() == digital_id:
                records.append(block)

    return jsonify(records)
