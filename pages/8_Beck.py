# Some useful libraries you've probably used have already been imported for you
import streamlit as st
import os
import pandas as pd
import ssl
import matplotlib.pyplot as plt
import textwrap

# Page setup
tab_name = os.path.basename(__file__) # Gets file name
front_trim_index = tab_name.find('_') # Calculates where to trim the file name
tab_name = tab_name[front_trim_index+1:].removesuffix('.py') # Formats the file name to just the name
st.set_page_config(page_title=f"{tab_name}'s project", # Sets page title based on file name
                   page_icon="🍕", # Pick an emoji to show in the tab
                   layout='wide', # Uses the whole page for content
                   initial_sidebar_state='collapsed') # Auto hides the sidebar

# Info about content shown on page
st.title("NYC Health Code Violations") # Display a title for the project
project_description = """My project gets data from GitHub which is sourced from the health board of NYC.
It calculates an average amount of violations received for each type of cuisine. Then, it graphs them in
different colors where red is the most violations and green is the fewest.
What I am proud of is how I calculated the average violations per cuisine type. It took a lot of time
because I had to try different methods to do this. I did this by using dictionaries to keep track of the
number of received violations, and every time a cuisine is seen again, updating its average. 
What I overcame was formatting the graph. I struggled to get the labels and bars right because there was so
much data, but trial and error was able to get me there. Also, there was one category of restaurants (cafés)
which encountered an error where the accent would cause the text to display all weird, so I had to create a function
to remove those pesky accent marks."""
st.markdown(f"**About my project:** *{project_description}*") # Displays the student's description in a pre-formatted way using markdown

# This section of the file runs your code that makes the graph
go_button = st.button("▶️ Run code", use_container_width=True) # Button to run the person's code
if go_button: # When the button is clicked, this will run
    project_running = st.status(f"Running {tab_name}'s code", expanded=True) # Creates a display showing the progress of the app running
    with project_running:
        # Step 1: Get data
        st.write("Getting data from the internet...") # Adds an update to the execution status

        # Set up certificate
        ssl._create_default_https_context = ssl._create_stdlib_context
        # Load the dataset
        url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-12-11/nyc_restaurants.csv'
        df = pd.read_csv(url)

        # Step 2: Data analysis
        st.write("Processing the data using PANDAS...")

        # Set up dataframe
        df['cuisine_description'] = df['cuisine_description']
        # Make sure 'score' and 'cuisine_description' are not null
        df.dropna(subset=['score', 'cuisine_description'], inplace=True)

        # Calculate average scores using for loops
        score_sums = {}
        count = {}

        # Iterate through the DataFrame
        for index, row in df.iterrows():
            cuisine = row['cuisine_description']
            score = row['score']

            if cuisine in score_sums:
                score_sums[cuisine] += score
                count[cuisine] += 1
            else:
                score_sums[cuisine] = score
                count[cuisine] = 1

        # Calculate averages and store them in a dictionary
        average_scores = {cuisine: score_sums[cuisine] / count[cuisine] for cuisine in score_sums}

        # Make a formatted (accent free dictionary and rounded numbers)
        final_data = {}
        for key in average_scores.keys():
            key_new = key.replace("CafÃ©", "Cafe") # .replace("\u00c3\u00a9", "e").replace("é", "e")
            final_data[key_new] = round(average_scores[key])

        # Because a lower score is better, sort by low to high scores based on values
        def get_value(item):
            return item[1]

        # Sorting the dictionary items by value
        sorted_items = sorted(final_data.items(), key=get_value)

        # Creating a new dictionary with sorted items
        sorted_data = {}
        for key, value in sorted_items:
            sorted_data[key] = value

        # Step 3: Create and show graph
        st.write("Creating graph...")

        x = list(sorted_data.keys())
        y = list(sorted_data.values())

        # Define the colors based on values
        colors = []
        for value in y:
            if value < 15:
                colors.append('green')  # Bars representing values less than 10 will be green
            elif 15 <= value <= 20:
                colors.append('orange')  # Bars representing values between 10 and 20 will be yellow
            else:
                colors.append('red')  # Bars representing values greater than 20 will be red


        def format_labels(labels, width):
            """Trim long labels based on content and wrap them to the specified width."""
            trimmed_labels = []
            for label in labels:
                # Trim labels based on their content
                if "Latin" in label:
                    label = "Latin"
                elif "Bottled" in label:
                    label = "Drinks"
                elif "Vietnamese" in label:
                    label = "Vietnamese"
                
                # Append the trimmed and wrapped label to the list
                trimmed_labels.append(textwrap.fill(label, width))
        
            return trimmed_labels


        fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the size as needed
        ax.barh(x, y, color=colors, height=0.8)
        ax.set_title('Average Health Code Violations Of Each Cuisine in NYC', fontsize=14)
        ax.set_xlabel('Amount of violations', fontsize=12)
        ax.set_ylabel('Type of restaurant', fontsize=12)
        ax.set_yticks(range(len(x)))
        ax.set_yticklabels(format_labels(x, width=50), fontsize=5)
        plt.tight_layout()

    # All the coder's code is now ran, time to display the graph
    st.balloons() # Shows a little celebration

    # Streamlit will take care of displaying the graph from here
    st.pyplot(fig) # Make sure to have your graph saved to a variable called 'fig'