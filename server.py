from flask import Flask, render_template,request
from service import generateResponse
app = Flask(__name__)


from bs4 import BeautifulSoup as Soup

html = """
<html>
<head>
<title>Test Page</title>
</head>
<body>
<div>Your Report</div>
</html>
"""
soup = Soup(html)

title = soup.find('title')
meta = soup.new_tag('meta')
meta['content'] = "text/html; charset=UTF-8"
meta['http-equiv'] = "Content-Type"
title.insert_after(meta)

print soup

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submitForm', methods=['GET', 'POST'])
def my_link():
    print('I got clicked!')
    firstName = request.args.get('firstname',None)
    print(firstName)
    lastName = request.args.get('lastname',None)
    print(lastName)
    response = generateResponse(firstName,lastName)
    print(response)
    return response
    
if __name__ == '__main__':
    app.run(debug=True)