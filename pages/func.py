import streamlit as st
import pandas as pd
import plotly.express as px
import random
import datetime
from datetime import timedelta

class TaskManager:
    """
    A class to manage tasks, generate fake data, calculate allocated hours,
    and visualize task allocations using Streamlit and Plotly.

    Attributes:
        users (list): List of user IDs.
        tasks (list): List of tasks with their corresponding hours.
        data (list): List of generated task data.
    """

    def __init__(self, users, tasks):
        """
        Initializes the TaskManager with users and tasks.

        Args:
            users (list): List of user IDs.
            tasks (list): List of tasks with their corresponding hours.
        """
        self.users = users
        self.tasks = tasks
        self.data = self.generate_fake_data()

    def generate_fake_data(self):
        """
        Generates fake task data for users.

        Returns:
            list: A list of dictionaries containing task information.
        """
        data = []
        for user in self.users:
            num_issues = random.randint(1, 10)  # Random number of issues per user
            for _ in range(num_issues):
                issue_key = f"TASK-{random.randint(100000, 999999)}"  # Generate a fake issue key
                task = random.choice(self.tasks)  # Choose a random task
                
                # Generate delivery date (today, tomorrow, or in the future)
                days_until_delivery = random.choice([0, 1, random.randint(2, 7)])  # Today (0), Tomorrow (1), Future (>2 days)
                delivery = datetime.datetime.today() + timedelta(days=days_until_delivery)
                
                data.append({
                    'user_id': user,
                    'issue_key': issue_key,
                    'task': task['task'],
                    'hours': task['hours'],
                    'delivery': delivery.strftime('%Y-%m-%d')  # Format delivery date
                })
        return data

    def create_dataframe(self):
        """
        Converts the generated data into a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the task data.
        """
        return pd.DataFrame(self.data)

    def calculate_allocated_hours(self, df):
        """
        Calculates the total allocated hours and free time for each user.

        Args:
            df (pd.DataFrame): A DataFrame containing task data.

        Returns:
            pd.DataFrame: A DataFrame with total allocated hours and free time per user.
        """
        allocated_hours = df.groupby('user_id')['hours'].sum().reset_index(name='Allocated Hours')
        allocated_hours['Limit'] = 8  # Set daily hour limit
        allocated_hours['Free Time'] = allocated_hours['Limit'] - allocated_hours['Allocated Hours']
        allocated_hours['Free Time'] = allocated_hours['Free Time'].apply(lambda x: max(0, x))
        return allocated_hours

    def filter_data(self, df, filter_option, custom_date=None):
        """
        Filters the DataFrame based on the selected delivery date option.

        Args:
            df (pd.DataFrame): A DataFrame containing task data.
            filter_option (str): The option selected for filtering ('Today', 'Tomorrow', 'Custom', 'All').
            custom_date (datetime.date, optional): A custom date for filtering.

        Returns:
            pd.DataFrame: A filtered DataFrame based on the delivery date.
        """
        if filter_option == "Today":
            return df[df['delivery'] == datetime.datetime.today().strftime('%Y-%m-%d')]
        elif filter_option == "Tomorrow":
            return df[df['delivery'] == (datetime.datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')]
        elif filter_option == "Future":
            return df[df['delivery'] > (datetime.datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')]
        elif filter_option == "Custom" and len(custom_date) > 1:
            start_date, end_date = custom_date
            return df[(df['delivery'] >= start_date.strftime('%Y-%m-%d')) & (df['delivery'] <= end_date.strftime('%Y-%m-%d'))]
        else:
            return df  # If "All" is selected, show all

    def plot_data(self, filtered_df, allocated_hours):
        """
        Plots the allocated hours and free time for the filtered data.

        Args:
            filtered_df (pd.DataFrame): A filtered DataFrame containing task data.
            allocated_hours (pd.DataFrame): A DataFrame with total allocated hours per user.

        Returns:
            plotly.graph_objs.Figure: A Plotly figure object representing the bar chart.
        """
        allocated_filtered = filtered_df.groupby('user_id')['hours'].sum().reset_index(name='Allocated Hours')
        allocated_filtered = allocated_filtered.merge(allocated_hours[['user_id']], on='user_id', how='left')

        # Calculate Free Time
        allocated_filtered['Limit'] = 8
        allocated_filtered['Free Time'] = allocated_filtered['Limit'] - allocated_filtered['Allocated Hours']
        allocated_filtered['Free Time'] = allocated_filtered['Free Time'].apply(lambda x: max(0, x))

        # Create bar chart
        fig = px.bar(allocated_filtered, 
                     x='user_id', 
                     y=['Allocated Hours', 'Free Time', 'Limit'], 
                     barmode='group', 
                     title='Allocated Tasks and Free Time by User')

        # Update layout
        fig.update_layout(yaxis_title="Hours", xaxis_title="User")
        fig.for_each_trace(lambda t: t.update(marker_color='green') if t.name == 'Free Time' else ())
        return fig

# List of fake users
users = ['ana.costa', 'joao.pereira', 'maria.santos', 'lucas.oliveira']

# Types of tasks with hours weights
tasks = [
    {'task': 'code review', 'hours': 3},
    {'task': 'testing', 'hours': 1},
    {'task': 'documentation', 'hours': 2},
    {'task': 'development', 'hours': 4}
]

# Create TaskManager instance
task_manager = TaskManager(users, tasks)

# Generate DataFrame
df = task_manager.create_dataframe()

# Calculate allocated hours
allocated_hours = task_manager.calculate_allocated_hours(df)

# Streamlit UI for date filter
st.subheader("Delivery Date Filter")
filter_option = st.selectbox("Select delivery date", ["Today", "Tomorrow", "All", "Custom"])
custom_date = None


if filter_option == "Custom":
    default_start, default_end = datetime.datetime.now() - timedelta(minutes=30), datetime.datetime.now()
    today = datetime.datetime.now()
    current_year = today.year
    jan_1 = datetime.date(current_year, 1, 1)
    dec_31 = datetime.date(current_year, 12, 31)

    custom_date = st.date_input(
        "Select your vacation for next year",
        value=(default_start, default_end),
        min_value=jan_1,
        max_value=dec_31,
    )

    # Convertendo a data selecionada para o formato desejado
    if len(custom_date) > 1: 
        formatted_dates = [date.strftime('%Y-%m-%d') for date in custom_date]
        start_date_str = formatted_dates[0]  # Data de início
        end_date_str = formatted_dates[1] if len(formatted_dates) > 1 else formatted_dates[0]

        st.write(f"Selected start date: {start_date_str}")
        st.write(f"Selected end date: {end_date_str}")


    
#custom_date = st.date_input("Choose a date:", value=datetime.today())

# Filter data based on selection
filtered_df = task_manager.filter_data(df, filter_option, custom_date)

# Plot data
fig = task_manager.plot_data(filtered_df, allocated_hours)

# Show plot in Streamlit
st.plotly_chart(fig)

# Display filtered data table
st.write("Filtered Tasks sem range")
st.write(df[['user_id', 'issue_key', 'task', 'hours', 'delivery']])


st.write("Filtered Tasks com range")
st.write(filtered_df[['user_id', 'issue_key', 'task', 'hours', 'delivery']])