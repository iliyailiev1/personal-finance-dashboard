import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import pandas as pd
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

    # Create a new DataFrame for the new entry
    new_entry = pd.DataFrame({'Income': [income] if income is not None else [None],
                              'Expense': [expense] if expense is not None else [None]})

    # Concatenate the new entry with the existing DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)

    # Save updated data
    df.to_csv(DATA_FILE, index=False)

    # Calculate totals for the chart
    total_income = df['Income'].sum()
    total_expense = df['Expense'].sum()

    # Generate the pie chart
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

@app.route('/edit_income/<int:index>', methods=['POST'])
def edit_income(index):
    new_income = request.form.get('new_income', type=float)
    df = pd.read_csv(DATA_FILE)
    df.at[index, 'Income'] = new_income
    df.to_csv(DATA_FILE, index=False)
    return home()

@app.route('/delete_income/<int:index>', methods=['POST'])
def delete_income(index):
    df = pd.read_csv(DATA_FILE)
    df = df.drop(index)  # Remove the row at the specified index
    df.to_csv(DATA_FILE, index=False)
    return home()

@app.route('/edit_expense/<int:index>', methods=['POST'])
def edit_expense(index):
    new_expense = request.form.get('new_expense', type=float)
    df = pd.read_csv(DATA_FILE)
    df.at[index, 'Expense'] = new_expense
    df.to_csv(DATA_FILE, index=False)
    return home()

@app.route('/delete_expense/<int:index>', methods=['POST'])
def delete_expense(index):
    df = pd.read_csv(DATA_FILE)
    df = df.drop(index)  # Remove the row at the specified index
    df.to_csv(DATA_FILE, index=False)
    return home()



if __name__ == '__main__':
    app.run(debug=True)
