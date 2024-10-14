from flask import Flask, render_template, request

app = Flask(__name__)

# Store income and expenses in lists (or you can use a database later)
incomes = []
expenses = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    income = request.form.get('income', type=float)
    expense = request.form.get('expense', type=float)

    if income is not None:
        incomes.append(income)
    if expense is not None:
        expenses.append(expense)

    return render_template('index.html', incomes=incomes, expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)
