from flask import Flask
from flask import render_template
from flask import json

from Bio import pairwise2

app = Flask(__name__)

@app.route('/alignment')
def alignment():
    return render_template('d3_alignment.html')

@app.route('/alignment_json')
def alignment_json():
    alignments = pairwise2.align.globalxx("ACCACTGATCGAAATTGTGGCCCGT",
            "TTAGTAAGGCCAAACG")
    data = [{'s':p[0],'d':p[1]} for p in zip(alignments[0][0], alignments[0][1])]
    return json.dumps(data)

if __name__ == '__main__':
    app.run()
