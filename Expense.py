import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# MySQL connection configuration
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
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
    st.image("C:/Users/LONE PIRATE.LAPTOP-PAANLTJP/OneDrive/Pictures/114600779.jpg")

def total():
    st.title("TOTAL EXPENSES")
    
    # query1
    query = "SELECT * FROM EXPENSETRACKER2024"
    
    df = fetch_data(query)
    if not df.empty:
        st.subheader("Overall expense of 2024")
        st.dataframe(df)  
    else:
        st.warning("No data found or an error occurred.")
    
    #query2
    query=(""" select category, sum(amount) from expensetracker2024
                group by category
                ORDER BY CATEGORY DESC; """)

    df = fetch_data(query)
    st.subheader("Total expense Categorically")
    st.dataframe(df)

    #query3
    query=("""select payment_mode, sum(amount) from expensetracker2024
            group by Payment_mode;
    """)

    df = fetch_data(query)
    st.subheader("Total spent on Payment modes")
    st.dataframe(df)


    # query4
    query=("select sum(cashback) from expensetracker2024;")

    df = fetch_data(query)
    st.subheader("Total Cashback")
    st.dataframe(df)

    #QUERy5
    query=("""select category, sum(amount) from expensetracker2024
                group by category
                ORDER BY CATEGORY DESC
                limit 4;
    """)

    df = fetch_data(query)
    st.subheader("Top 4 total expense categorically")
    st.dataframe(df)

   
    #QUERY6
    query=("""select category, amount from expensetracker2024
            where cashback>0;
    """)

    df = fetch_data(query)
    st.subheader("Cash back gained all Transactions")
    st.dataframe(df)

    #QUERY7
    query=("""select date_format(date, '%y-%m') as Months, sum(amount) as Total_spending
        from expensetracker2024 
        group by date_format(date, '%y-%m' )
        order by date_format(date, '%y-%m' );
    """)

    df = fetch_data(query)
    st.subheader("Total Monthly Expense")
    st.dataframe(df)

    #QUERY8
    query=("""select date_format(date, '%y-%m') as Months, sum(cashback) as Total_cashback
        from expensetracker2024 
        group by date_format(date, '%y-%m' )
        order by date_format(date, '%y-%m' );
    """)

    df = fetch_data(query)
    st.subheader("Total Monthly Cashback")
    st.dataframe(df)

def category():
    st.title("Expense on Categories")
    #query9
    query=("""select Payment_mode, sum(Amount) from expensetracker2024
            where CATEGORY="TRANSPORT"
            group by Payment_mode;
    """)

    df = fetch_data(query)
    st.subheader("Total spent on Transport")
    st.dataframe(df)


    #query10
    query=("""SELECT date, CATEGORY, DESCRIPTION, PAYMENT_MODE ,AMOUNT
        FROM EXPENSETRACKER2024 
        WHERE AMOUNT = (SELECT MAX(AMOUNT) FROM EXPENSETRACKER2024);
           """)
    df=fetch_data(query)
    st.subheader("Max spent category")
    st.dataframe(df)

    #query11
    query=("""SELECT category, 
       DATE_FORMAT(date, '%y-%m') AS month, 
       COUNT(*) AS occurrence_count, 
        SUM(amount) AS total_spent
        FROM EXPENSETRACKER2024
        GROUP BY category, DATE_FORMAT(date, '%y-%m')
        HAVING COUNT(*) > 1  -- Ensures that only recurring expenses are shown
        ORDER BY month, occurrence_count DESC;
           """)
    df=fetch_data(query)
    st.subheader("Recurring categorical Expense")
    st.dataframe(df)

    #query12
    query=("""SELECT date, CATEGORY, DESCRIPTION, PAYMENT_MODE ,AMOUNT
        FROM EXPENSETRACKER2024 
        WHERE AMOUNT = (SELECT MIN(AMOUNT) FROM EXPENSETRACKER2024)
           """)
    df=fetch_data(query)
    st.subheader("Min categorical Expense")
    st.dataframe(df)

    #query13
    query=("""select Payment_mode, sum(Amount) as Total from expensetracker2024
            where CATEGORY="ENTERTAINMENT"
            group by Payment_mode
           """)
    df=fetch_data(query)
    st.subheader("Expense on Entertainment")
    st.dataframe(df)

    #query14
    query=("""select description, sum(amount) from expensetracker2024 
        where category = "transport"
        group by description;
           """)
    df=fetch_data(query)
    st.subheader("Expense on different Types of transport")
    st.dataframe(df)


def viz():
    st.title("Visualization")

    #VIZ 1 
    query = """
    SELECT category, SUM(amount) AS total_spent
    FROM EXPENSETRACKER2024
    GROUP BY category
    ORDER BY total_spent DESC;
    """
    df=fetch_data(query)

    if not df.empty:
        # Calculate percentage contribution
        df['percentage'] = (df['total_spent'] / df['total_spent'].sum()) * 100

        # Display Dataframe
        st.subheader("Spending by Category")
        #st.dataframe(df)

        # Plot Pie Chart using Matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(df['total_spent'], labels=df['category'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title("Category-wise Spending Distribution")

        # Show the plot in Streamlit
        st.pyplot(fig)

    else:
        st.warning("No data found for the selected query.")
    
    #viz 2
    query = """
        SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) AS total_spent
        FROM expensetracker2024
        WHERE category = 'Health'
        GROUP BY DATE_FORMAT(date, '%Y-%m')
        ORDER BY DATE_FORMAT(date, '%Y-%m');
    """

    df = fetch_data(query)
    
    if not df.empty:
        st.subheader("Monthly health Expense viz")
        #st.dataframe(df)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df["month"], df["total_spent"], marker ='o', linestyle='-', color='b', label='Health expense' )
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Spent (₹)")
        ax.set_title("Grocery Spending Over Time")
        ax.legend()
        ax.grid(True)

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation=45)

        # Show chart in Streamlit
        st.pyplot(fig)
    else:
        st.warning("No grocery spending data found.")
    
    #viz 3 
    query = """
        select date_format(date, '%Y-%m') as Months, category, payment_mode, sum(amount) as total_spent 
        from expensetracker2024 
        group by DATE_FORMAT(date, '%Y-%m'), category, payment_mode
        order by DATE_FORMAT(date, '%Y-%m'), category;
    """

    df = fetch_data(query)

    #subheader 
    st.subheader("Most Used Payment Mode Month-wise with Category")

    #plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x="category", y="total_spent", hue="payment_mode", data=df)
    
    # Labels and title
    plt.xlabel("category")
    plt.ylabel("Total Spent (₹)")
    plt.title("Monthly Spending by Payment Mode and Category")
    plt.xticks(rotation=45)
    plt.legend(title="Payment Mode")

    # Display chart in Streamlit
    st.pyplot(plt)


def thank():
    st.title("Thank you")
    st.image("C:/Users/LONE PIRATE.LAPTOP-PAANLTJP/OneDrive/Pictures/hand-lettering-thank-you-flowery-vector.jpg")
    st.subheader("By Abinash")


pages = {"HOME" : homepage, 
         "Total spent": total, 
         "Category expense" : category,
         "Visuvalization" : viz,
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


