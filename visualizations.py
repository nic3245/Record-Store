# Bonus Visualizations

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


username = input("Enter MySQL username: ")
password = input("Enter MySQL password: ")

cnx = pymysql.connect(
      host='localhost',
        user=username,
        password=password,
        db='record_store',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


# Employee visualization
employee = "SELECT * FROM employee"
employee_df = pd.read_sql_query(employee, cnx)
employee_df = employee_df.sort_values(by='salary')

plt.figure(figsize=(10, 6))
plt.bar(employee_df['full_name'], employee_df['salary'])
plt.xlabel('Employees')
plt.ylabel('Salary')
plt.title('Salary Difference between Employees')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Shifts visualization
shifts = "SELECT * FROM shifts"
shifts_df = pd.read_sql_query(shifts, cnx)
# Count the number of shifts per weekday
shift_counts = shifts_df['week_day'].value_counts().sort_index()

# Create the visualization
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

# Bar chart for shift counts
ax[0].bar(shift_counts.index, shift_counts.values)
ax[0].set_xlabel('Weekday')
ax[0].set_ylabel('Number of Shifts')
ax[0].set_title('Shift Distribution per Weekday')

# Line plot for start and end hours
ax[1].plot(shifts_df['shift_id'], shifts_df['start_hr'], marker='o', label='Start Hour')
ax[1].plot(shifts_df['shift_id'], shifts_df['end_hr'], marker='o', label='End Hour')
ax[1].set_xlabel('Shift ID')
ax[1].set_ylabel('Hour')
ax[1].set_title('Shift Start and End Hours')
ax[1].legend()

plt.tight_layout()

plt.show()

# Records visualization
records = "SELECT * FROM records"
records_df = pd.read_sql_query(records, cnx)

plt.figure(figsize=(10, 8))
sns.scatterplot(data=records_df, x='release_year', y='genre_id', hue='artist_id', size='artist_id', sizes=(50, 200), palette='viridis')
plt.xlabel('Release Year')
plt.ylabel('Genre ID')
plt.title('Records: Release Year vs. Genre')


plt.show()

# Orders visualization
orders = "SELECT * FROM orders"
orders_df = pd.read_sql_query(orders, cnx)

fig = px.scatter(orders_df, x='num_items', y='total', size='total', color='location', hover_data=['order_id', 'c_id'])
fig.update_layout(title='Orders: Number of Items vs. Total Amount',
                  xaxis_title='Number of Items',
                  yaxis_title='Total Amount')

fig.show()
