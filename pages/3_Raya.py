# Some useful libraries you've probably used have already been imported for you
import streamlit as st
import os
import pandas as pd
import ssl
import matplotlib.pyplot as plt

# Page setup
tab_name = os.path.basename(__file__) # Gets file name
front_trim_index = tab_name.find('_') # Calculates where to trim the file name
tab_name = tab_name[front_trim_index+1:].removesuffix('.py') # Formats the file name to just the name
st.set_page_config(page_title=f"{tab_name}'s project", # Sets page title based on file name
                   page_icon="😀", # Pick an emoji to show in the tab
                   layout='wide', # Uses the whole page for content
                   initial_sidebar_state='collapsed') # Auto hides the sidebar

# Info about content shown on page
st.title("Project_title") # Display a title for the project
project_description = """My project does___. What I am proud of is ___. What I overcame was ___."""
st.markdown(f"**About my project:** *{project_description}*") # Displays the student's description in a pre-formatted way using markdown

# This section of the file runs your code that makes the graph
go_button = st.button("▶️ Run code", use_container_width=True) # Button to run the person's code
if go_button: # When the button is clicked, this will run
    project_running = st.status(f"Running {tab_name}'s code", expanded=True) # Creates a display showing the progress of the app running
    with project_running:
        # Step 1: Get data
        st.write("Getting data from the internet...") # Adds an update to the execution status
        # Paste your code here to get the data from the webpage

        # Step 2: Data analysis
        st.write("Processing the data using PANDAS...")
        # Paste your code here to process the data with pandas

        # Step 3: Create and show graph
        st.write("Creating graph...")
        # Paste your code here to create the graph

    # All the coder's code is now ran, time to display the graph
    st.balloons() # Shows a little celebration

    # Streamlit will take care of displaying the graph from here
    fig = None # DELETE THIS LINE AFTER PUTTING IN YOUR CODE, IT JUST STOPS THE IDE FROM SHOWING AN ERROR
    st.pyplot(fig) # Make sure to have your graph saved to a variable called 'fig'