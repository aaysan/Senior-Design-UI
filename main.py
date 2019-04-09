#Mehmet Alp Aysan
import sys
sys.path.insert(0, './../Senior_Design/')
# print(sys.path)


from flask import request
from flask import render_template
from flask import Flask
import re
import blttest as b
import get_weather as gw

app = Flask(__name__,static_url_path='/static')

class Information:
    name = ""

    def __init__(self):
        return


@app.route("/",methods=['GET', 'POST'])
def hello():
    return render_template('main_page.html')

@app.route("/fr_res")
def face_recog():
    a = b.get_name()
    pattern = r'Name:(.*)\n'
    res = re.findall(pattern,a)

    if len(res) > 0:
        name = res[0].strip()
        Information.name = name
        if name != 'outsider':
            return render_template('main_page_recognized.html', name=name)
    return render_template('main_page_not_recognized.html')

@app.route("/logged_in")
def show_options():

    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('post_login_main.html',name=Information.name,temperature=temperature)

@app.route("/add_clothes")
def add_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('add_clothes.html', name=Information.name,temperature=temperature)



if __name__ == '__main__':
    app.run()
