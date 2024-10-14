from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Store income and expenses
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

    # Generate the pie chart
    if incomes or expenses:
        labels = ['Total Income', 'Total Expense']
        sizes = [sum(incomes), sum(expenses)]
        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Save the figure
        if not os.path.exists('static'):
            os.makedirs('static')
        plt.savefig('static/pie_chart.png')
        plt.close()

    return render_template('index.html', incomes=incomes, expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)
