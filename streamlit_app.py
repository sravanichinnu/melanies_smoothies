# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

# display the Fruit options list
#session = get_active_session()
#my_dataframe = session.table("smoothies.public.fruit_options")
#st.dataframe(data = my_dataframe, use_container_width=True)

# removed the SELECT BOX

# focus on the FRUIT_NAME column
# To use a Snowpark column function named 'col', we need to import it into our app.

# a text inout box, so that a customer can enter their name while ordering smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

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
