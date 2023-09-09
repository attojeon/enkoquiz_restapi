# flask 서비스 기본 코드

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, random, os

app = Flask("__english_dictionary__")

# enko 딕셔너리 
enko_dict = {}
# 같은 디렉토리에서 json 파일을 읽어서 enko_dict에 저장
current_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_path, 'english_korean_dictionary.json')
with open(data_file_path, 'r', encoding='utf-8') as f:
    enko_dict = json.load(f)

# enko 리스트
enko_list = []
for k, v in enko_dict.items():
    enko_list.append((k, v))

# enko quiz card 리스트 
'''
card = {
    'en': 'apple',
    'ko': '사과',
    'options': ['사과', '바나나', '포도', '수박'] 
    'result': 's' # s: success, f: fail , n: not yet
}
'''
def build_quiz_card(word):
    card = {}
    card['en'] = word[0]
    card['ko'] = word[1]
    options = []
    while len(options) < 3:
        options.append(random.choice(enko_list)[1])
        if card['ko'] in options:
            options.remove(card['ko'])
        options = list(set(options))
    options.append(card['ko'])
    random.shuffle(options)
    card['options'] = options
    card['result'] = 'n'
    return card


@app.route('/')
def index():
    return 'English Dictionary'

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/quiz/<count>')
def quiz(count):
    quiz_list = []
    quiz_ko_list = random.sample(enko_dict.items(), int(count))
    for i in range(int(count)):
        onecard = build_quiz_card(quiz_ko_list[i])
        quiz_list.append(onecard)
        print(onecard)
    return jsonify(quiz_list)

app.run(host="0.0.0.0", port="8080")