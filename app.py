import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import os

app = Flask(__name__)


DATA_FILE = 'data.csv'

app.secret_key = 'your_secret_key'  # Replace with a secure random key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['user_id'] = request.form['username']  # Save user ID in session for simplicity
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        user = User(user_id)
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Initialize CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Income', 'Expense'])
    df.to_csv(DATA_FILE, index=False)

@app.route('/')
@login_required
def home():
    df = pd.read_csv(DATA_FILE)
    incomes = df['Income'].dropna().tolist()
    expenses = df['Expense'].dropna().tolist()
    return render_template('index.html', incomes=incomes, expenses=expenses,
                           income_indexes=range(len(incomes)), expense_indexes=range(len(expenses)))

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
