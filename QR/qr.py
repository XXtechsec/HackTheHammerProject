from flask import Flask, render_template
from flask_qrcode import QRcode
from binascii import hexlify
import os
import uuid

app = Flask(__name__)
qrcode = QRcode(app)

class chall_context:
    def __init__(self, id, challenge):
        self.id = id
        self.challenge = challenge
    def to_string(self):
        chall = str(self.challenge)
        chall = chall[2:len(chall)-1]
        return '{ "id":' + str(self.id) + ', "challenge":' + chall + ' }'

@app.route('/')
def generate_qrcode():
    id = uuid.uuid4()
    challenge = hexlify(os.urandom(64))
    content = chall_context(id, challenge)
    return render_template('qrcode.html', content=content.to_string())

if __name__ == '__main__':
    app.run()