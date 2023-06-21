from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd;

app = Flask(__name__)
df=pd.read_pickle("book.pkl")
pt=pd.read_pickle("pt.pkl")
sim=pd.read_pickle("sim.pkl")
book=pd.read_pickle("books.pkl")
@app.route('/')
def index():
    return  render_template("index.html",
                            book_name=list(df['Book-Title'].values),
                            author=list(df['Book-Author'].values),
                            image=list(df['Image-URL-M'].values),
                            votes=list(df['num_ratings'].values),
                            rating=np.round(list(df['avg_ratings'].values),2)
                            )
@app.route('/rec')
def recommend_ui():
    return render_template('recomedation.html')
@app.route("/recom",methods=['GET','POST'])
def recom():

    y = []
    user_input = request.form.get('user_input')
    ind = np.where(pt.index == user_input)[0][0]
    lis = sorted(list(enumerate(sim[ind])), key=lambda x: x[1], reverse=True)[0:6]
    for i in lis:
        y.append(pt.index[i[0]])
    df2=book[book["Book-Title"].isin(y)].drop_duplicates("Book-Title")
    print(df2)
    return render_template("recomedation.html",
                           data=df2,
                           book_nam=list(df2['Book-Title'].values),
                           autho=list(df2['Book-Author'].values),
                           imag=list(df2['Image-URL-M'].values),
                           )
if __name__ == '__main__':
    app.run(debug=True)
