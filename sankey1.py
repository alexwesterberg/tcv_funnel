# app.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

csv_file_path = r'C:\Users\a.westerberg\Documents\2024 jobseaerch\2024 01 data volunteering TCV\first try with sample data provided by John\sample data\Hull-vols-to-analyse.csv'
csv_file_path2 = r'..\first try with sample data provided by John\sample data\Hull-vols-to-analyse.csv'


df = pd.read_csv(csv_file_path)



# Set the title of the app
st.title('Exploration of Hull volunteers dataset')



# Display the head of the DataFrame
st.write("Here's the head of the DataFrame:")
st.dataframe(df.head())  # You can also use st.write(df.head())


# create a timeline???
df['Start'] = pd.to_datetime(df['First Task'])
df['Finish'] = pd.to_datetime(df['Last Task'])
df['New_ID'] = pd.factorize(df['ID'])[0] + 1

# Get the unique IDs sorted
sorted_unique_ids = sorted(df['ID'].unique())

# Create a mapping from old IDs to new IDs (1 to n)
id_mapping = {ID: new2_id for new2_id, ID in enumerate(sorted_unique_ids, start=1)}

# Map the old IDs to new IDs using the mapping
df['new2_id'] = df['ID'].map(id_mapping)

# Create a Gantt chart (timeline) using Plotly
fig = px.timeline(df, x_start="Start", x_end="Finish", y="new2_id") #, labels={"ID": "Task Name"})
fig.update_yaxes(categoryorder="total ascending")  # Optional: This line makes the y-axis (Task names) ordered
fig.update_layout(xaxis_title='Time', yaxis_title='ID', title='Volunteers Timeline')


# Date for the horizontal line
line_date = datetime.now().date() 

# Add a horizontal line across the timeline
fig.add_shape(
    # Line Horizontal
    type="line",
    x0=line_date,
    y0=0,
    x1=line_date,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(
        color="Red",
        width=3,
    ),
)

# Display the timeline in Streamlit
st.plotly_chart(fig)
# Run this app with the command: streamlit run app.py



st.header('Sankey Diagram Example')


# Exemplar data for the Sankey diagram
nodes = ['A', 'B', 'C', 'D', 'E']  # Example nodes
source_indices = [0, 1, 0, 2, 3]  # Indices of the source nodes in the nodes list
target_indices = [2, 3, 3, 4, 4]  # Indices of the target nodes in the nodes list
values = [8, 4, 2, 8, 4]  # The values associated with each flow

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,  # Padding between nodes
        thickness=20,  # Thickness of the nodes
        line=dict(color="black", width=0.5),
        label=nodes  # Labels for the nodes
    ),
    link=dict(
        source=source_indices,  # Indices of source nodes
        target=target_indices,  # Indices of target nodes
        value=values  # Values for each flow
    ))])

# Show the figure in the Plotly renderer (outside Streamlit)
# fig.show()  # Uncomment this line if you want to see the plot outside Streamlit

# Streamlit app code to display the diagram
st.plotly_chart(fig)

st.write("N.B. according to ChatGPT-4, there is no way for a vertical orientation using the prebuilt Graphobjects version of Sankey Diagrams. This is apparently due to the limitations of the API that it uses? But this may of course be the AI hallucinating...")

st.header('Sankey Diagram First Try')
st.subheader('prelim steps')
# Try using dummy data in real format for the Sankey diagram

csv_file_path2 = r'C:\Users\a.westerberg\Documents\2024 jobseaerch\2024 01 data volunteering TCV\first try with sample data provided by John\sample data\Dummy custom report.csv'
df2 = pd.read_csv(csv_file_path2)

st.write("Here's the head of the next DataFrame:")
st.dataframe(df2.head())  # You can also use st.write(df.head())

# now fix the concatenation of dates for column "list of dates"

st.write("Check the column \'task dates\' has been fixed:")

df2['task dates'] = df2.apply(lambda row: ' '.join([str(x) for x in [row['first task'], row['second task'], row['third task']] if pd.notnull(x)]), axis=1)

st.dataframe(df2.head())  # You can also use st.write(df.head())

# Display the code
st.write("Type of object in column \'task dates\' after artificial concatenation")

st.code(print(df2['task dates'].dtype))

unique_types = {type(v) for v in df2['task dates']}
st.code(print(unique_types))

## now suppose you have successfully extracted all the dates into separate columns (the opposite of what we were doing above)

## next, we would want to actually.. make a sankey diagram?

# # need:
# a total count
# a count of all the rows where they didn't turn up
# a count of all the rows they did turn up once but no more
# a count of all the rows they turned up three times

## then - integrate these numbers into the sankey diagram?

##where to start?
# counts first

st.write("Check result of calculation of length of df:")
type_1_all = len(df2)
st.write(type_1_all)  # This will display the length correctly in the app
st.write("Verified by cross checking with dummy dataset in excel - that has 151 rows incl header so 151-1 = 150 which is the correct result we have here")

# Check for empty (NaN) values across specific columns and count rows where all are empty
st.write("Check result of calculation of number of empty dates in df:")
count_empty_rows = df2[['first task', 'second task', 'third task']].isna().all(axis=1).sum()
st.write(count_empty_rows)


st.write("Check result of calculation of number of only one attendance in df:")
# # Count rows where "first task" is not empty and both "second task" and "third task" are empty
# count_only_one_attendance = df2[((df2['first task'].notna() & df2['second task'].isna() & df2['third task'].isna()) |
#                                  (df2['first task'].isna() & df2['second task'].notna() & df2['third task'].isna()) |
#                                  (df2['first task'].isna() & df2['second task'].isna() & df2['third task'].notna())
#                                 )].shape[0]
# st.write(count_only_one_attendance)

count_only_one_attendance = type_1_all - count_empty_rows

st.write("Check result of calculation of number of multiple attendances in df:")
# Create a boolean DataFrame where True indicates the presence of a non-blank (not NaN) value
not_blank = df2[['first task', 'second task', 'third task']].notna()

# Sum the boolean values row-wise to count non-blank entries per row
non_blank_counts = not_blank.sum(axis=1)

# Count rows where there are at least two non-blank entries
count_rows_at_least_two_non_blank = (non_blank_counts >= 2).sum()

st.write(count_rows_at_least_two_non_blank)

number_who_left_after_one_session = count_only_one_attendance - count_rows_at_least_two_non_blank

##### now assign these calculated numbers to the sankey diagram
st.subheader('First proper diagram')

nodes_2 = ['Signed up', 'Did not attend any sessions', 'Attended one session', 'Left after one session', 'Returned for multiple sessions']  # Example nodes
source_indices_2 = [0, 0, 2, 2]  # Indices of the source nodes in the nodes list
target_indices_2 = [1, 2, 3, 4]  # Indices of the target nodes in the nodes list
values_2 = [count_empty_rows, count_only_one_attendance, number_who_left_after_one_session, count_rows_at_least_two_non_blank]  # The values associated with each flow

# Manually specify the position of each node
node_x = [0.1, 0.5, 0.5, 0.9, 0.9]
node_y = [0.3, 0.8, 0.2, 0.8, 0.1]

# Create the Sankey diagram
fig_2 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,  # Padding between nodes
        thickness=20,  # Thickness of the nodes
        line=dict(color="black", width=0.5),
        label=nodes_2,  # Labels for the nodes
        x=node_x,  # Set X positions
        y=node_y  # Set Y positions
    ),
    link=dict(
        source=source_indices_2,  # Indices of source nodes
        target=target_indices_2,  # Indices of target nodes
        value=values_2  # Values for each flow
    ))])

fig.update_layout(title_text="Sankey Diagram for vol engagement with Manually Positioned Nodes", font_size=10)

st.plotly_chart(fig_2)
#############################################
#################### END ####################
#############################################

# Run this app with the command: streamlit run app.py