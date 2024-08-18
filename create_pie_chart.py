import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def create_pie_chart(df, title="Revenu et Dépenses", width=5, height=5):
    """
    Generates a pie chart for Revenu and Dépenses from a DataFrame.

    Parameters:
    - df (pandas.DataFrame): The data containing 'revenu' and 'depenses' columns.
    - title (str): The title of the chart.
    - width (int or float): The width of the chart in inches. Default is 8.
    - height (int or float): The height of the chart in inches. Default is 8.
    """
    # Check if the DataFrame is empty
    if df.empty:
        st.warning("Cette Table est vide. Veuillez ajouter des données pour regenerer le graphique.",icon="⚠️")
        return

    # Ensure the DataFrame has the required columns
    if not {'revenu', 'depenses'}.issubset(df.columns):
        st.error("DataFrame must contain 'revenu' and 'depenses' columns")
        return

    # Aggregate data for pie chart
    total_revenu = df['revenu'].sum()
    total_depenses = df['depenses'].sum()
    sizes = [total_revenu, total_depenses]
    labels = ['Revenu', 'Dépenses']
    colors = ['blue', 'red']

    # Check if both values are zero
    if total_revenu == 0 and total_depenses == 0:
        st.warning("Les données sont vide.",icon="⚠️")
        return

    # Create a new figure
    fig, ax = plt.subplots(figsize=(width, height))

    # Generate the pie chart
    wedges, texts, autotexts = ax.pie(

        sizes,
        normalize=True,
        shadow=True,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=1)  # Adjust the width of the disc
    )

    # Set chart title
    ax.set_title(title)

    # Display the chart in Streamlit
    st.pyplot(fig,use_container_width=True)

# Example usage
if __name__ == "__main__":
    # Example DataFrame
    data = {
        'revenu': [1000, 1500, 1200],
        'depenses': [800, 1200, 1100]
    }
    df = pd.DataFrame(data)

    # Generate the pie chart
    create_pie_chart(df, title="Revenu et Dépenses")