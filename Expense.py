import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL connection configuration
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="expense_tracker"
    )

# Function to fetch data from MySQL
def fetch_data(query):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # Get column names
        cursor.close()
        connection.close()
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# Streamlit app
def homepage():
    st.title("WELCOME TO THE ANNUAL EXPENSE TRACKER")
    st.subheader("PRESENTED BY ABINASH")
    st.image("C:/Users/LONE PIRATE.LAPTOP-PAANLTJP/Pictures/114600779.jpg")

def total():
    st.title("TOTAL EXPENSE")
    
    # query1
    query = "SELECT * FROM EXPENSETRACKER2024"
    
    df = fetch_data(query)
    if not df.empty:
        st.subheader("Overall expense of 2024")
        st.dataframe(df)  # Display data as an interactive table
    else:
        st.warning("No data found or an error occurred.")
    
    #query2
    query=("select sum(amount) as Total_expense from expensetracker2024")

    df = fetch_data(query)
    st.subheader("Total expense in 2024")
    st.dataframe(df)

    #query3
    query=("""select date_format(date, '%y-%m') as Months, sum(amount) as Total_spending
        from expensetracker2024 
        group by date_format(date, '%y-%m' )
        order by date_format(date, '%y-%m' )
        
    """)

    df = fetch_data(query)
    st.subheader("Monthly total expense")
    st.dataframe(df)


    # query4
    query=("""select category, sum(amount) as Total from expensetracker2024
            group by category
            ORDER BY CATEGORY DESC
        
    """)

    df = fetch_data(query)
    st.subheader("Total expense on all categories")
    st.dataframe(df)

    #QUERy5
    query=("""select date_format(date, '%y-%m') as Months, category, sum(amount) as Total_spending
            from expensetracker2024 
            group by date_format(date, '%y-%m' ), category
            order by date_format(date, '%y-%m' ), category
    """)

    df = fetch_data(query)
    st.subheader("Total monthly expense on each category")
    st.dataframe(df)

def category():
    st.title("TOTAL EXPENSE ON EACH CATEGORY")
    #query 6 
    query=("""select Payment_mode, sum(Amount) as Total from expensetracker2024
            where CATEGORY="FOOD"
            group by Payment_mode
           """)
    df=fetch_data(query)
    st.subheader("Expense on Food")
    st.dataframe(df)

    #query7
    query=("""select Payment_mode, sum(Amount) as Total from expensetracker2024
            where CATEGORY="TRANSPORT"
            group by Payment_mode
           """)
    df=fetch_data(query)
    st.subheader("Expense on Transport")
    st.dataframe(df)

    #query8
    query=("""select Payment_mode, sum(Amount) as Total from expensetracker2024
            where CATEGORY="HEALTH"
            group by Payment_mode
           """)
    df=fetch_data(query)
    st.subheader("Expense on Health")
    st.dataframe(df)

    #query9
    query=("""select Payment_mode, sum(Amount) as Total from expensetracker2024
            where CATEGORY="EDUCATION"
            group by Payment_mode
           """)
    df=fetch_data(query)
    st.subheader("Expense on Education")
    st.dataframe(df)

    #query10
    query=("""select Payment_mode, sum(Amount) as Total from expensetracker2024
            where CATEGORY="ENTERTAINMENT"
            group by Payment_mode
           """)
    df=fetch_data(query)
    st.subheader("Expense on Entertainment")
    st.dataframe(df)

def max_spent():
    st.title("Maximum expense")

    #query11
    query=("""SELECT date, CATEGORY, DESCRIPTION, PAYMENT_MODE ,AMOUNT
            FROM EXPENSETRACKER2024 
            WHERE AMOUNT = (SELECT MAX(AMOUNT) FROM EXPENSETRACKER2024)
           """)
    df=fetch_data(query)
    st.subheader("Max expens above all")
    st.dataframe(df)

    #query12
    query=("""SELECT date_format(date, '%y-%m' ) as Months, MAX(AMOUNT) as Max_expense
            FROM EXPENSETRACKER2024 
            GROUP BY date_format(date, '%y-%m' )
           """)
    df=fetch_data(query)
    st.subheader("Monthly maximum expense")
    st.dataframe(df)
    
    #query13
    query=("""select category, max(amount) as Max_expense , date_format(date, '%y-%m' ) as Months from expensetracker2024
            group by category, date_format(date, '%y-%m' )
            order by category desc;
           """)
    df=fetch_data(query)
    st.subheader("Max spend on each category per month")
    st.dataframe(df)

    #query14
    query=("""select t1.category, t1.description, t1.payment_mode, date_format(date, '%y-%m') as Months, t1.amount as Max_spent
            from expensetracker2024 t1
            join (SELECT date_format(date, '%y-%m' ) as months, MAX(AMOUNT) as max_amount
            FROM EXPENSETRACKER2024 
            GROUP BY date_format(date, '%y-%m' ))t2 
            on 
            date_format(t1.date, '%y-%m') = t2.months
            AND t1.amount=t2.max_amount
            order by max_spent desc;
           """)
    df=fetch_data(query)
    st.subheader("Max epense on category per month")
    st.dataframe(df)

def min_spent():
    st.title("Minium expense")

    #query15
    query=("""SELECT date, CATEGORY, DESCRIPTION, PAYMENT_MODE ,AMOUNT
            FROM EXPENSETRACKER2024 
            WHERE AMOUNT = (SELECT MIN(AMOUNT) FROM EXPENSETRACKER2024)
           """)
    df=fetch_data(query)
    st.subheader("Min expens above all")
    st.dataframe(df)

    #query16
    query=("""SELECT date_format(date, '%y-%m' ) as Months, MIN(AMOUNT) as Min_expense
            FROM EXPENSETRACKER2024 
            GROUP BY date_format(date, '%y-%m' )
           """)
    df=fetch_data(query)
    st.subheader("Monthly minimum expense")
    st.dataframe(df)
    
    #query17
    query=("""select category, min(amount) as Min_expense , date_format(date, '%y-%m' ) as Months from expensetracker2024
            group by category, date_format(date, '%y-%m' )
            order by category desc;
           """)
    df=fetch_data(query)
    st.subheader("Min spend on each category per month")
    st.dataframe(df)

    #query18
    query=("""select t1.category, t1.description, t1.payment_mode, date_format(date, '%y-%m') as Months, t1.amount as Min_spent
            from expensetracker2024 t1
            join (SELECT date_format(date, '%y-%m' ) as months, min(AMOUNT) as min_amount
            FROM EXPENSETRACKER2024 
            GROUP BY date_format(date, '%y-%m' ))t2 
            on 
            date_format(t1.date, '%y-%m') = t2.months
            AND t1.amount=t2.min_amount
            order by min_spent desc;
           """)
    df=fetch_data(query)
    st.subheader("Min epense on category per month")
    st.dataframe(df)

def thank():
    st.title("Thank you")
    st.image("C:/Users/LONE PIRATE.LAPTOP-PAANLTJP/Pictures/hand-lettering-thank-you-flowery-vector.jpg")
    st.subheader("By Abinash")


pages = {"HOME" : homepage, 
         "Total spent": total, 
         "Category expense" : category, 
         "Max expense" : max_spent, 
         "Min expense" : min_spent, 
         "END" : thank
}
selection = st.sidebar.radio("Choose a Page", list(pages.keys()))

# Execute the selected page
if selection:
    pages[selection]()



#ensures it only runs when the script is executed directly but not during imports 
if __name__ == "__total__":
    total()
if __name__ == "__category__":
    category()
if __name__ == "__max_spent__":
    max_spent()
if __name__ == "__min_spent__":
    min_spent()


