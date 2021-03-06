from flask import Flask, jsonify, request
from flask_cors import CORS
import json
app = Flask(__name__)

CORS(
    app,
    origins=["*"],
    # origins=['http://localhost:3000','http://35.200.34.122:3000/'],
    methods=["GET", "PUT", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Origin", "X-Requested-With", "Content-Type"],
    supports_credentials=True,
)


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/reply', methods=['POST'])
def reply():
    data = json.loads(request.data)
    answer = "Yes, it is %s!\n" % data["keyword"]
    result = {
      "Content-Type": "application/json",
      "Answer":{"Text": answer}
    }
    # return answer
    return jsonify(result)

@app.route('/mask', methods=['POST'])
def masking():
    data = json.loads(request.data)
    mp = Morph()
    mp.set_sentence(data['text'])
    mp.get_parsed_text()
    proper_noun = mp.extract_proper_noun()
    text = mp.masking()
    result = {
        'text': text,
        'proper': proper_noun
    }
    return jsonify(result)

class Morph(object):
    def __init__(self):
        self.dic_path = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd'
        try:
            import MeCab
            self.normal = MeCab.Tagger('-d {}'.format(self.dic_path))
            self.wakati = MeCab.Tagger('-Owakati -d {}'.format(self.dic_path))
        except:
            self.normal = MeCab.Tagger('')
            self.wakati = MeCab.Tagger('-Owakati')

    def mask(self):
        import MeCab
        mecab = MeCab.Tagger ('-d {}'.format(self.dic_path))
    
    def set_sentence(self, text):
        self.text = text

    def extract_proper_noun(self):
        """固有名詞の抽出"""
        self.results = []
        for node in self.parsed:
            l = node.split(',')
            if len(l[0]) != 0:
                (word, part) = l[0].split('\t')
                noun_type = l[1]
                if part in '名詞' and noun_type in "固有名詞":
                    kind_of_proper_noun = (l[2], l[3])
                    if l[2] not in '一般':
                        self.results.append((word, kind_of_proper_noun))
        result_uniq = list(set(self.results))
        self.result_dict = dict(result_uniq)
        return self.result_dict


    def get_parsed_text(self):
        """形態素解析"""
        self.normal.parse('')
        self.parsed = self.normal.parse(self.text).splitlines()[:-1]

    def masking(self):
        wakati_txt = self.wakati.parse(self.text).split(' ')
        words = self.text
        for word in wakati_txt:
            kind_touple = self.result_dict.get(word)
            if kind_touple is not None:
                words = words.replace(word, '{}'.format('*' * len(word)))
        return words

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)