from flask import Flask, render_template,redirect, url_for, request,g
import time

from readJson import searchQuery
app = Flask(__name__)

@app.route('/')
def home():
    # search = request.args.get('inputButton')
    
    # return redirect(url_for('index.html', name = search))
    return render_template('index.html')

@app.route('/search',methods=["GET","POST"])
def search(it=None):
    search_time = time.time()
    name = request.args.get('inputButton')
    a = searchQuery(name)
    search_time = time.time() - search_time
    print(search_time)
    return render_template('search.html',it= a)

if __name__ == "__main__":
    app.run(debug=True)