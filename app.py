from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

pin = '4545'


class Todo(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


# home page
@app.route('/')
def hello_world():
    return render_template('index.html')


# quote page
@app.route('/quote/')
def quotePage():
    quotes = Todo.query.all()
    if len(quotes) < 1:
        return 'No quotes'
        # render_template('quote.html', quote="There aren't any quotes.")
    else:
        quote = random.choice(quotes)
        return render_template('quote.html', quote=quote)


# takes you to pinCheck
@app.route('/addQuotePage/')
def addQuotePage():
    return render_template('pinCheck.html')


# adds the quote
@app.route('/addQuote/', methods=['GET', 'POST'])
def addQuote():
    if request.method == 'POST':
        quote = request.form['content']
        newQuote = Todo(content=quote)

        try:
            db.session.add(newQuote)
            db.session.commit()
            return render_template('pinSuccess.html')
        except:
            return 'failure'
    else:
        return redirect('/')

@app.route('/addAnotherQuote/')
def anotherQuote():
    return render_template('addQuote.html')

# checks your pin
@app.route('/pinCheckPage/', methods=['GET', 'POST'])
def pinCheckPage():
    if request.method == 'POST':
        if request.form['content'] == pin:
            return render_template('addQuote.html')
        else:
            return "Ian you stinky ape man you don't have the power to add a quote :)"
    else:
        return redirect('/')


# @app.route('/editQuotePinCheckPage/')
@app.route('/quotePinCheckPage/')
def quotePinCheckPage():
    return render_template('quotePinCheck.html')


# Checks your pin before editing quotes
@app.route('/quotePinCheck/', methods=['GET', 'POST'])
def quotePinCheck():
    if request.method == 'POST':
        if request.form['content'] == pin:
            # quotes = Todo.query.all()
            # return render_template('quoteEditor.html', quotes=quotes)
            return redirect('/quoteEditor/')
            # return render_template('quoteEditor.html')
        else:
            return "Failure"
    else:
        return redirect('/')


# takes you to the quote editor
@app.route('/quoteEditor/')
def quoteEditor():
    quotes = Todo.query.all()
    return render_template('quoteEditor.html', quotes=quotes)
    # return render_template('quoteEditor.html')


# deletes the quote
@app.route('/delete/<int:id>')
def delete(id):
    quoteDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(quoteDelete)
        db.session.commit()
        return redirect('/quoteEditor/')
    except:
        return 'There was a problem deleting that task'


if __name__ == '__main__':
    #False for production
    app.run(debug=False)
