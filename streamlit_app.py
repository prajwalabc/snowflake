# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f" :cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

name_on_order = st.text_input('Name of Smoothie')
st.write('The name on the smoothie will be ', name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_list = st.multiselect(
    "Choose up to five ingredients",
    my_dataframe, max_selections=5
)

if ingredients_list:
    ingredients_string=''
    for x in ingredients_list:
        ingredients_string += x + ' ';
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', x,' is ', search_on, '.')
      
        st.subheader(x+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + x)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert= st.button('submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




