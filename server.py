from flask import Flask, render_template,request
from service import generateResponse
app = Flask(__name__)
boilerplateHead = "<html><title>Report</title><style>tr:nth-child(even) {color:Red;background: white} tr:nth-child(odd) {color:blue;background: black}</style><body style = \"text-align:center; background-color:black; font-size: 30px;\"> <p style=\"color:yellow\">Report</p><table style = \"text-align:center; margin:1em auto;\"><tr><td style=\"font-size:30px\">"
boilerplateTail = "</td></tr></table><a href =\"/\" style=\"color:yellow\"><img src=\"templates/home.jpg\" alt=\"home\" width=\"100\" height=\"50\"></a></body></html>"
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
    c = response.count("\n")
    print(c)
    s = ""
    #for i in range(0, c-1):
    s = response.replace("\n","</td></tr><tr><td style=\"font-size:30px\">")
    response1 = boilerplateHead + s +boilerplateTail
    print(response1)
    index = open("templates/index.html").read().format(x=response1)
    return response1
    
if __name__ == '__main__':
    app.run(debug=True)