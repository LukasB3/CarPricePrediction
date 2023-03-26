import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from get_data import load_data

df = load_data()

def wagen_nach_hersteller(dataframe):
    car_makers = dataframe['make'].value_counts()
    
    fig_height = max(6, len(car_makers) * 0.1)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    
    ax.bar(car_makers.index, car_makers.values)
    plt.xticks(rotation=90)
    ax.set_ylabel('Anzahl')
    ax.set_title('Verkaufte Gebrauchtwagen nach Hersteller')

    padding = 0.2
    ax.set_xlim(-0.5 - padding, len(car_makers) - 0.5 + padding)

    return fig

def top_20_modelle(dataframe):
    top20_car_models = dataframe['model'].value_counts().head(20)

    fig_height = max(6, len(top20_car_models) * 0.2)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    ax.bar(top20_car_models.index, top20_car_models.values)
    plt.xticks(rotation=90)
    ax.set_ylabel('Anzahl')
    ax.set_title('Top 20 meistverkaufte Gebrauchtwagenmodelle')

    padding = 0.2
    ax.set_xlim(-0.5 - padding, len(top20_car_models) - 0.5 + padding)

    return fig

def gesamtumsatz_hersteller(dataframe):
    car_makers_total_price = dataframe.groupby('make')['price'].sum().sort_values(ascending=False)
    
    fig_height = max(6, len(car_makers_total_price) * 0.1)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    
    ax.bar(car_makers_total_price.index, car_makers_total_price.values)
    plt.xticks(rotation=90)
    ax.set_ylabel('Umsatz (€)')
    ax.set_title('Gesamtumsatz nach Hersteller')
    
    padding = 0.2
    ax.set_xlim(-0.5 - padding, len(car_makers_total_price) - 0.5 + padding)
    
    return fig

def modell_verteilung(dataframe, car_maker):
    models = dataframe[dataframe['make'] == car_maker]['model'].value_counts()

    fig_height = max(6, len(models) * 0.2)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    
    ax.barh(models.index, models.values)
    ax.set_xlabel('Anzahl Autos')
    ax.set_title(f'{car_maker} Modell Verteilung')

    padding = 0.2
    ax.set_ylim(-0.5 - padding, len(models) - 0.5 + padding)

    return fig

def top_modelle_preis(dataframe, car_maker):
    models_average_price = dataframe[dataframe['make'] == car_maker].groupby('model')['price'].mean().sort_values(ascending=False).head(5)
    
    fig, ax = plt.subplots(figsize=(8, 2))
    
    bars = ax.bar(models_average_price.index, models_average_price.values)
    ax.set_ylabel('∅-Preis (€)')
    
    num_models_displayed = len(models_average_price)
    ax.set_title(f'Top {num_models_displayed} {car_maker} Modelle nach höchstem ∅-Preis')

    def add_value_labels(ax, bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}€',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, -12),  # Offset the value slightly below the top of the bar
                        textcoords='offset points',
                        ha='center', va='bottom',
                        color='white')

    add_value_labels(ax, bars)

    
    return fig

def top_modelle_umsatz(dataframe, car_maker):
    top5_models = dataframe[dataframe['make'] == car_maker].groupby('model')['price'].sum().sort_values(ascending=False).head(5)
    
    fig, ax = plt.subplots(figsize=(8, 2))
    
    bars = ax.bar(top5_models.index, top5_models.values)
    ax.set_ylabel('Umsatz (€)')
    
    num_models_displayed = len(top5_models)
    ax.set_title(f'Top {num_models_displayed} {car_maker} Modelle nach höchstem Umsatz')

    def add_value_labels(ax, bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}€',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, -12),  # Offset the value slightly below the top of the bar
                        textcoords='offset points',
                        ha='center', va='bottom',
                        color='white')

    add_value_labels(ax, bars)

    return fig

def kraftstoff_pie_chart(dataframe, car_maker):
    fuel_counts = dataframe[dataframe['make'] == car_maker]['fuel'].value_counts()

    fuel_counts.index = fuel_counts.index.map(lambda x: 'Benzin' if x == 'Gasoline' else x)
    fig, ax = plt.subplots()
    ax.pie(fuel_counts.values, labels=fuel_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(f'{car_maker} Kraftstoff Verteilung')

    return fig

def calculate_data(dataframe, car_maker):
    avg_price = dataframe[dataframe['make'] == car_maker]['price'].mean()
    avg_mileage = dataframe[dataframe['make'] == car_maker]['mileage'].mean()
    max_price = dataframe[dataframe['make'] == car_maker]['price'].max()
    min_price = dataframe[dataframe['make'] == car_maker]['price'].min()
    max_mileage = dataframe[dataframe['make'] == car_maker]['mileage'].max()
    min_mileage = dataframe[dataframe['make'] == car_maker]['mileage'].min()
    return avg_price, avg_mileage, max_price, min_price, max_mileage, min_mileage

def explore_page():
    
    car_makers = sorted(df['make'].unique())
    car_makers.insert(0, "All Car Makers")
    selected_car_maker = st.sidebar.selectbox("Hersteller wählen", car_makers)

    if selected_car_maker == "All Car Makers":
        st.subheader("Gesamtübersicht aller Hersteller")
        wagen_nach_hersteller_chart = wagen_nach_hersteller(df)
        st.pyplot(wagen_nach_hersteller_chart)

        top_20_modelle_chart = top_20_modelle(df)
        st.pyplot(top_20_modelle_chart)

        gesamtumsatz_hersteller_chart = gesamtumsatz_hersteller(df)
        st.pyplot(gesamtumsatz_hersteller_chart)

        

    else:
        st.subheader(f"Übersicht für {selected_car_maker}")
        
        modell_verteilung_chart = modell_verteilung(df, selected_car_maker)
        st.pyplot(modell_verteilung_chart)
        
        fuel_pie_chart = kraftstoff_pie_chart(df, selected_car_maker)
        
        avg_price, avg_mileage , max_price, min_price, max_mileage, min_mileage = calculate_data(df, selected_car_maker)

        
        
        top_modelle_preis_chart = top_modelle_preis(df, selected_car_maker)
        st.pyplot(top_modelle_preis_chart)
        
        top_modelle_umsatz_chart = top_modelle_umsatz(df, selected_car_maker)
        st.pyplot(top_modelle_umsatz_chart)

        col3, col4 = st.columns([2, 1])  
        with col3:
            st.pyplot(fuel_pie_chart)
        with col4:
            st.subheader("Durchschnittswerte")
            st.markdown(f"**∅ - Preis:**\n{avg_price:.2f} €")
            st.markdown(f"**∅ - Kilometerstand:**\n{avg_mileage:.0f} km")
            st.subheader("Min / Max - Werte")
            st.markdown(f"**Max. Preis:**\n{max_price} €")
            st.markdown(f"**Min. Preis:**\n{min_price} €")
            st.markdown(f"**Max. Kilometerstand:**\n{max_mileage} km")
            st.markdown(f"**Min. Kilometerstand:**\n{min_mileage} km")


st.set_option('deprecation.showPyplotGlobalUse', False)