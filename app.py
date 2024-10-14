from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

DATA_FILE = 'data.csv'

# Initialize CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Income', 'Expense'])
    df.to_csv(DATA_FILE, index=False)

@app.route('/')
def home():
    df = pd.read_csv(DATA_FILE)
    incomes = df['Income'].dropna().tolist()
    expenses = df['Expense'].dropna().tolist()
    return render_template('index.html', incomes=incomes, expenses=expenses)

@app.route('/submit', methods=['POST'])
def submit():
    income = request.form.get('income', type=float)
    expense = request.form.get('expense', type=float)

    # Load existing data
    df = pd.read_csv(DATA_FILE)

    if income is not None:
        df = df.append({'Income': income}, ignore_index=True)
    if expense is not None:
        df = df.append({'Expense': expense}, ignore_index=True)

    # Save updated data
    df.to_csv(DATA_FILE, index=False)

    # Generate the pie chart
    total_income = df['Income'].sum()
    total_expense = df['Expense'].sum()

    if total_income or total_expense:
        labels = ['Total Income', 'Total Expense']
        sizes = [total_income, total_expense]
        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')

        if not os.path.exists('static'):
            os.makedirs('static')
        plt.savefig('static/pie_chart.png')
        plt.close()

    balance = total_income - total_expense

    return render_template('index.html', incomes=df['Income'].dropna().tolist(),
                           expenses=df['Expense'].dropna().tolist(),
                           total_income=total_income, total_expense=total_expense, balance=balance)

if __name__ == '__main__':
    app.run(debug=True)
