# Import Python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

# a text inout box, so that a customer can enter their name while ordering smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

# to bring back only the FRUIT_NAME column instead of the whole table,
# we use '.select(col('FRUIT_NAME'))

# adding a Multiselect - the Streamlit Multi-Select Widget
# commenting out 'st.dataframe(data=my_dataframe, use_container_width=True)'
# we can uncomment it later
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

# we are telling users to choose up to 5 ingredients, but we are not enforcing that limit in code

# The data returned is both a list and a LIST
# The 'ingredients' variable is an object (data type) called a LIST.
# It's a list in the everyday sense of the word, but it's also a specific datatype called a LIST.
# A LIST is different from a DATAFRAME, which is also different from a STRING.
# We can use the following Streamlit methods to inspect what's inside out ingredients LIST:
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://MY.smoothiefroot.com/api/fruit/{search_on}")
        # st.text(smoothiefroot_response) => this just gives the 'Response [200]' which generally means the API was successful
        #st.text(smoothiefroot_response.json()) # this convert the response so we can read the response object's contents.
        # lets put the JSON into a Dataframe  
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    # st.write(ingredients_string)

    # storing the Orders in Snowflake
    # build a SQL Insert Statement & Test it
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    # Streamlit Stop command is great for troubleshooting.
    # we want to get the SQL right before the app tries to write to the database
    time_to_insert = st.button('Submit Order')

    # insert the Order into Snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


# new section to display smoothiefroot nutrition information



