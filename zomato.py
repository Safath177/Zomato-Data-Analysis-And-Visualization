import pandas as pd
import streamlit as st
import matplotlib.pyplot
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('S:\Projects\Zomato Viz Assignment\zomato_final.csv')
cur = pd.read_csv('S:\Projects\Zomato Viz Assignment\zomato_country_data.csv')

st.set_page_config(layout='wide')

st.title('Zomato Data Analysis and Visualization')

def analyze_country_data(df):

    country = st.selectbox('Select The Country',df['Country'].unique())


    fil_df_c = df[df['Country'] == country ]

    col1,col2 = st.columns(2)

    with col1:

        # cuisine analysis
        chart_ca = px.bar(fil_df_c,x='Cuisines',title='Cuisine Analysis')
        chart_ca.update_traces(marker_color = '#FFA500')
        st.plotly_chart(chart_ca)

        # Ratings analysis

        chart_ra = px.bar(fil_df_c,x='Restaurant Name',y='Aggregate rating',title='Rating Analysis')
        chart_ra.update_traces(marker_color = '#FFA500')
        st.plotly_chart(chart_ra)

        # Delivery services

        chart_ds = px.pie(fil_df_c.drop_duplicates(subset = ['Restaurant Name']),names='Has Online delivery',title='Delivery Services',
                          color_discrete_sequence=['#00FFFF','#FFA500'])
        st.plotly_chart(chart_ds)

    with col2:

        # cost analysis on cuisine

        chart_cac = px.bar(fil_df_c.groupby('Cuisines').agg({'Converted_Cost':'mean'}).reset_index(),
        x = 'Cuisines', y = 'Converted_Cost', title = 'Cost Analysis on Cuisine')
        chart_cac.update_traces(marker_color = '#FFA500')
        st.plotly_chart(chart_cac)

        # cost analysis on restaurant

        chart_car = px.bar(fil_df_c.groupby('Restaurant Name').agg({'Converted_Cost':'mean'}).reset_index(),
                            x = 'Restaurant Name',y='Converted_Cost',title='Cost Analysis on Restaurants')
        chart_car.update_traces(marker_color = '#FFA500')
        st.plotly_chart(chart_car)
        

    # Expensive cuisine

    most_expensive_cuisine = fil_df_c.groupby('Cuisines')['Converted_Cost'].mean().idxmax()

    st.write(f'The Most Expensive Cuisine in {country} is "{most_expensive_cuisine}"')

    # Expensive Restaurant

    most_expensive_restaurant = fil_df_c.groupby('Restaurant Name')['Converted_Cost'].mean().idxmax()

    st.write(f'The Most Expensive Restaurant in {country} is "{most_expensive_restaurant}"')


def analyze_city_data(df):

    country = st.selectbox('Select The Country for City Analysis',df['Country'].unique())

    fil_df_c = df[df['Country'] == country ]

    city = st.selectbox('Select The City',fil_df_c['City'].unique())

    fil_df_c_c = fil_df_c[fil_df_c['City'] == city]

    col1,col2 = st.columns(2)

    with col1:

        # Cuisine Analysis

        chart_cca = px.bar(fil_df_c_c['Cuisines'].value_counts().nlargest(10).reset_index(),
                            x='Cuisines',y='count',title='Top Cuisines in the City',labels={'index':'Cuisine','Cuisines':'Count'})
        st.plotly_chart(chart_cca)

    
        # Price Analysis of Cuisine

        chart_pac = px.bar(fil_df_c_c.groupby('Cuisines').agg({'Converted_Cost':'mean'}).reset_index(),
                            x='Cuisines',y='Converted_Cost',title='Cost Analysis on Cuisines of the City')
        st.plotly_chart(chart_pac)

        
        # Ratings of Cuisines

        chart_rc = px.bar(fil_df_c_c,x='Cuisines',y='Votes',title='Ratings of the Cuisines in the City',color='Aggregate rating')
        st.plotly_chart(chart_rc)
    with col2:
        # online delivery

        chart_od = px.pie(fil_df_c_c,names='Has Online delivery',title='Online Delivery Availability')
        st.plotly_chart(chart_od)

        # Price Analysis of Restaurant

        chart_par = px.bar(fil_df_c_c.groupby('Restaurant Name').agg({'Converted_Cost':'mean'}).reset_index(),
                            x='Restaurant Name',y='Converted_Cost',title='Cost Analysis on Restaurants of the City')
        st.plotly_chart(chart_par)

        # Ratings of Restaurants

        chart_rr = px.bar(fil_df_c_c,x='Restaurant Name',y='Votes',title='Ratings of the Restaurants in the City',color='Aggregate rating')
        st.plotly_chart(chart_rr)
    st.write("")
    st.write("")
    # Expensive cuisine

    most_expensive_cuisine = fil_df_c_c.groupby('Cuisines')['Converted_Cost'].mean().idxmax()

    st.write(f'The Most Expensive Cuisine in {city} is "{most_expensive_cuisine}"')

    # Expensive Restaurant

    most_expensive_restaurant = fil_df_c_c.groupby('Restaurant Name')['Converted_Cost'].mean().idxmax()

    st.write(f'The Most Expensive Restaurant in {city} is "{most_expensive_restaurant}"')



def city_comparison(df):
    df2 = df[df['Country'] == 'India']

    # Number of restaurants of the cities of India

    col1,col2 = st.columns(2)

    with col1:

        chart_no_rest = px.bar(df2.groupby('City').size().reset_index(),
                            x='City',y=0,title='Number of Restaurants in each City')
        st.plotly_chart(chart_no_rest)

        # Online Delivery in each City

        df_spend = df2[df2['Has Online delivery'] == 'Yes'].groupby('City')['Converted_Cost'].sum().reset_index()

        fig_online = px.bar(df_spend,x='City',y='Converted_Cost',title='Indian Cities And Thier Online Order Expenses')

        st.plotly_chart(fig_online)

    with col2:
    
        # Dine in in each city

        df_dine = df2[df2['Has Table booking'] == 'Yes'].groupby('City')['Converted_Cost'].sum().reset_index()

        fig_dine = px.bar(df_dine,x='City',y='Converted_Cost',title='Indian Cities And Thier Dine-In Expenses')

        st.plotly_chart(fig_dine)
        
        # Cost of Living in each City

        col = px.bar(df2.groupby('City')['Average Cost for two'].mean().reset_index(),
                    x='City',y='Average Cost for two',title='Cost of Living in Different Cities')
        st.plotly_chart(col)

tab1,tab2,tab3,tab4,tab5 = st.tabs(['About','Currency Analysis','Country Analysis','City Analysis','Indian Cities'])

with tab1:
    st.header("Zomato:")
    st.write('Zomato is a **leading Indian food delivery and restaurant discovery platform** that has transformed the way people experience dining.')
    st.write('Founded in **2008** by **Deepinder Goyal and Pankaj Chaddah**, Zomato started as a restaurant listing service and later expanded into food delivery, table reservations, and even grocery delivery.')
    st.write('Over the years, Zomato has grown into a **global food-tech company**, operating in multiple countries and serving millions of users. It connects customers with restaurants, offering menus, reviews, ratings, and seamless ordering options.')
    st.header('Business Model:')
    st.write('Zomato operates on a **multi-faceted business model** that combines food delivery, restaurant discovery, and various revenue streams. Here’s a breakdown of how Zomato functions:')
    st.write('### **Key Components of Zomato’s Business Model**')
    st.write('1. **Food Delivery** – Zomato partners with restaurants to facilitate food delivery. It charges a **commission** on each order placed through its platform.')
    st.write('2. **Restaurant Listings & Advertising** – Restaurants pay to be listed and promoted on Zomato, increasing their visibility to potential customers.')
    st.write('3. **Subscription Services** – Zomato offers **Zomato Gold**, a premium membership that provides discounts and exclusive deals.')
    st.write('4. **Hyperpure (B2B Supplies)** – Zomato supplies fresh ingredients and kitchen essentials to restaurants, ensuring quality and consistency.')
    st.write('5. **Quick Commerce (Blinkit)** – Zomato has expanded into **instant grocery delivery** through Blinkit.')
    st.write('6. **Table Reservations & Events** – Users can book tables at restaurants and access exclusive dining experiences.')
    st.write("Zomato’s revenue comes from **advertising, commissions, subscriptions, and B2B services**, making it a **diverse and sustainable** business model.")




with tab2:
    st.header('Currency Conversion Analysis:')
    st.subheader('INR Vs Others:')
    st.plotly_chart(px.bar(cur,x='Country',y='Exchange Rate',title='INR Vs Others'))


with tab3:
    st.header('Analysis Based on the Country:')
    
    analyze_country_data(df)

with tab4:
    st.header('Analysis Based on the City:')
    analyze_city_data(df)

with tab5:
    st.header('Comparison Between Cities In India')
    st.write("")
    city_comparison(df)