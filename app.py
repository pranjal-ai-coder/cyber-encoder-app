from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import base64
import binascii
import random
import time

app = Flask(__name__, template_folder='.')
CORS(app)

CODE_DICT = {
    'a':'@','b':'#','c':'$','d':'%','e':'&','f':'1','g':'2',
    'h':'3','i':'4','j':'5','k':'6','l':'7','m':'8','n':'9',
    'o':'0','p':'*','q':'!','r':'?','s':'+','t':'=','u':'-',
    'v':'/','w':'~','x':'<','y':'>','z':'^',' ':'_'
}
DECODE_DICT = {v:k for k,v in CODE_DICT.items()}

history_list = []

def caesar_cipher(text, shift=3, mode='encode'):
    if mode == 'decode': shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    global history_list
    try:
        data = request.get_json()
        text = data.get('text', '')
        mode = data.get('mode', 'encode')
        algo = data.get('algo', 'custom')
        
        if not text:
            return jsonify({'result': '', 'history': history_list, 'ai_tip': 'Type something to encode! 😎'})
        
        result = ""
        
        if algo == 'custom':
            if mode == 'encode':
                result = "".join(CODE_DICT.get(c.lower(), c) for c in text)
            else:
                result = "".join(DECODE_DICT.get(c, c) for c in text)
        elif algo == 'base64':
            if mode == 'encode':
                result = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            else:
                result = base64.b64decode(text.encode('utf-8')).decode('utf-8')
        elif algo == 'caesar':
            result = caesar_cipher(text, 3, mode)
        elif algo == 'hex':
            if mode == 'encode':
                result = binascii.hexlify(text.encode('utf-8')).decode('utf-8')
            else:
                result = binascii.unhexlify(text.encode('utf-8')).decode('utf-8')
        
        timestamp = time.strftime("%H:%M:%S")
        history_item = f"[{timestamp}] {algo.upper()}/{mode.upper()}: {result[:35]}..."
        history_list.insert(0, history_item)
        if len(history_list) > 6:
            history_list.pop()
        
        ai_tips = [
            f"Pro Tip: '{text[:10]}...' encoded perfectly! 🔒",
            "Try Base64 for web-safe encoding 📦",
            "Caesar cipher = ROT13 classic! 🔄",
            "Hex is great for binary data 🔢",
            "Custom cipher = Most secure! 🛡️"
        ]
        
        return jsonify({
            'result': result, 
            'history': history_list,
            'ai_tip': random.choice(ai_tips)
        })
    except:
        return jsonify({'result': 'ERROR: Invalid input', 'history': history_list})

if __name__ == '__main__':
    # Replit ke liye perfect config
    app.run(host='0.0.0.0', port=5000)
