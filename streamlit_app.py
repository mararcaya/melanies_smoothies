# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Streamlit page setup
st.title(f"Customize Your Smoothie! 🥤 {st.__version__}")
st.write(
    """Choose the fruits you want in your custom smoothie"""
)

# Get Snowflake connection from secrets.toml
cnx = st.connection("snowflake")
session = cnx.session()

# Text input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Load fruit options from Snowflake table
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
st.dataframe(my_dataframe, use_container_width=True)

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    [row['FRUIT_NAME'] for row in my_dataframe.collect()],
    max_selections=5
)

# Insert order into table
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ✅')
