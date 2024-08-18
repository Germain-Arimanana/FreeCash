import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def generate_bar_chart(df, title="Revenu et Dépenses",width=400, height=200):
    """
    Generates a bar chart for Revenu (blue) and Dépenses (red) from a DataFrame.

    Parameters:
    - df (pandas.DataFrame): The data containing 'date', 'revenu', and 'depenses' columns.
    - title (str): The title of the chart.
    """
   
    if not {'date', 'revenu', 'depenses'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'date', 'revenu', and 'depenses' columns")

   
    if df.index.name != 'date':
        df.set_index('date', inplace=True)

   
    ax = df[['revenu', 'depenses']].plot(kind='bar', color=['blue', 'red'], figsize=(10, 6))

    
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Montant")

   
    plt.xticks(rotation=45, ha='right')

   
    plt.grid(True, linestyle='--', alpha=0.7)

   
    plt.tight_layout()

    
    st.pyplot(plt)


if __name__ == "__main__":
  
    data = {
        'date': ['2024-08-01', '2024-08-02', '2024-08-03'],
        'revenu': [1000, 1500, 1200],
        'depenses': [800, 1200, 1100]
    }
    df = pd.DataFrame(data)

  
    st.title("Revenu vs Dépenses Bar Chart Example")
    generate_bar_chart(df, title="Example: Revenu et Dépenses")
