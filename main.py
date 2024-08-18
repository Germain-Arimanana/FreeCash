import streamlit as st
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt

from create_pie_chart import create_pie_chart
from generate_bar_chart import generate_bar_chart
from streamlit_option_menu import option_menu
from Rapport import rapport
from pdfGenerator import generate_pdf
from aboutApp import  about

st.set_page_config(layout="wide", page_title="Free Cash",
                   menu_items={
                       'About': "# Free Cash 🤑🤑🤑"}
                   )


conn = sqlite3.connect('financial_data.db', check_same_thread=False)
cursor = conn.cursor()


def menu():
    def updateDate():
        cursor.execute(f"DELETE FROM {selected_table}")
        conn.commit()

        for index, row in edited_df.iloc[:-1].iterrows():
            insert_record(selected_table, row['date'], row['description'], row['revenu'], row['depenses'])
        st.toast(f"Modifications enregistrées dans {selected_table} !", icon=":material/thumb_up:")
        st.rerun()

    @st.dialog("Nouveau Registre")
    def news():
        description = st.text_input("Motif")
        revenu = st.number_input("Débit", min_value=0)
        depenses = st.number_input("Crédit", min_value=0)
        date = st.date_input("Date", format="DD-MM-YYYY")
        if st.button("Enregistrer"):
            insert_record(selected_table, date, description, revenu, depenses)
            df = load_table_data(selected_table)
            total_revenu = df['revenu'].sum()
            total_depenses = df['depenses'].sum()
            summary_row = pd.DataFrame({
                'date': ['Total'],
                'description': [''],
                'revenu': [total_revenu],
                'depenses': [total_depenses]
            })
            df_with_totals = pd.concat([df, summary_row], ignore_index=True)
            st.rerun()
            st.toast("Registre Ajouté avec Succès", icon=":material/thumb_up:")

    def create_table(table_name):
        if table_name:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    description TEXT,
                    revenu REAL,
                    depenses REAL
                )
            """)
            conn.commit()
            st.toast(f"Table '{table_name}' créée !", icon="📊")

    def insert_record(table_name, date, description, revenu, depenses):
        cursor.execute(f"""
            INSERT INTO {table_name} (date, description, revenu, depenses)
            VALUES (?, ?, ?, ?)
        """, (date, description, revenu, depenses))
        conn.commit()

    def delete_tables(table_names):
        for table_name in table_names:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.commit()
            st.sidebar.toast(f"Table '{table_name}' supprimée !")

    def load_table_data(table_name):
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        return df

    def sanitize_table_name(new_table_name):
        characters_to_replace = ["'", "/", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "=", "[", "]", "{",
                                 "}", "|", ";", ":", ",", ".", "<", ">", "?", "!", "~", "`"]
        for char in characters_to_replace:
            new_table_name = new_table_name.replace(char, '_')
        formatted_name = new_table_name.replace(" ", "_").upper()
        return formatted_name

   
    with st.sidebar.form(key="create_table_form", clear_on_submit=True):
        new_table_name = st.text_input("Nouveau tableau").strip()
        if st.form_submit_button("Créer un Tableau 📊"):
            formatted_table = sanitize_table_name(new_table_name)
            create_table(formatted_table)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = [t[0] for t in cursor.fetchall()]
    with st.sidebar:
        with st.container(border=True):
            selected_table = st.selectbox("Afficher un Tableau ", options=tables[::-1])

    if selected_table:
        st.markdown(f" # Compte : {selected_table}")
        df = load_table_data(selected_table)
        total_revenu = df['revenu'].sum()
        total_depenses = df['depenses'].sum()
        total_rest = total_revenu - total_depenses

        summary_row = pd.DataFrame({
            'date': ['Total'],
            'description': [''],
            'revenu': [total_revenu],
            'depenses': [total_depenses]
        })
        df_with_totals = pd.concat([df, summary_row], ignore_index=True)

        edited_df = st.data_editor(df_with_totals, num_rows="dynamic", hide_index=True, width=1800,
                                   column_config={
                                       "revenu": st.column_config.NumberColumn("Débit ⬇️", format="Ar  %.2f",
                                                                               help="Le débit correspond au **montant qui entre** ⬇️"),
                                       "depenses": st.column_config.NumberColumn("Crédit ⬆️", format="Ar  %.2f",
                                                                                 help="Le crédit correspond au **montant qui sort** ⬆️"),
                                       "description": st.column_config.TextColumn("Description 🔖"),
                                       "date": st.column_config.TextColumn("Date 📅"),
                                   },
                                   )

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Nouveau Registre"):
                news()

        with col2:
            pdf_buffer = generate_pdf(df_with_totals, filename=f"{selected_table}.pdf")
            st.download_button(
                label="Exporter en PDF",
                data=pdf_buffer,
                file_name=f"{selected_table}.pdf",
                mime="application/pdf"
            )

        with col3:
            if st.button(f"Enregistrer les modifications"):
                updateDate()

        def format_number(number):
            return f"{number:,.2f}".replace(',', ' ').replace('.', '.')

        formatted_total_rest = format_number(total_rest)
        st.markdown(f"## Rèste : {formatted_total_rest} ar")

        with st.expander("Représentation Graphique", expanded=False):
            cl1, cl2 = st.columns(2)
            with cl1:
                generate_bar_chart(df_with_totals, title=f"Revenu et Dépenses de {selected_table}", width=400,)
                                
              
            with cl2:
                create_pie_chart(df, title=f"Revenu et Dépenses de {selected_table}", width=5, height=5)
               


    with st.sidebar:
        with st.container(border=True):
            tables_to_delete = st.multiselect("Sélectionner les Tableaux à supprimer", options=tables[::-1],
                                              placeholder="Multi-options")
            if st.button("Supprimer les Tableaux ❌"):
                if tables_to_delete:
                    delete_tables(tables_to_delete)
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
                    tables = [t[0] for t in cursor.fetchall()]
                    st.rerun()
                    st.toast("Tableau supprimé avec succès", icon=":material/thumb_up:")
                else:
                    st.warning("Veuillez sélectionner des tables à supprimer.")

            with st.expander(label="Fusionner les Tableaux",expanded=False):
               
                tables_to_merge = st.multiselect("Sélectionner les Tableaux à fusionner", options=tables[::-1],
                                                 placeholder="Multi-options")
                merged_table_name = st.text_input("Nom de la nouvelle table fusionnée").strip()
                if st.button("Fusionner les Tableaux"):

                    if tables_to_merge and new_table_name_table:
                        merged_df = pd.DataFrame()
                        for table in tables_to_merge:
                            df = load_table_data(table)
                            merged_df = pd.concat([merged_df, df], ignore_index=True)

                        formatted_merged_name = sanitize_table_name(merged_table_name)
                        create_table(formatted_merged_name)

                        for index, row in merged_df.iterrows():
                            insert_record(formatted_merged_name, row['date'], row['description'], row['revenu'],
                                          row['depenses'])

                        st.toast(f"Tables fusionnées dans '{formatted_merged_name}' !", icon=":material/thumb_up:")
                        st.rerun()
                    else:
                        st.warning("Veuillez sélectionner des tables et nommer la nouvelle table fusionnée.")





with st.sidebar:
    select = option_menu(
        "Free Cash",
        options=["Gestion des Comptes", "Rapport","A propos"],
        icons=["cash-coin", "file-bar-graph","info-square-fill"],
        menu_icon="currency-bitcoin"
    )

if select == "Gestion des Comptes":
    menu()
if select == "Rapport":
    rapport()
if select == "A propos":
    about()

