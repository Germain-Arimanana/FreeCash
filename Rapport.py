import streamlit as st
import pandas as pd
import sqlite3
import datetime
from pdfGeneratorT import generateT_pdf

try:
    conn = sqlite3.connect('financial_data.db',check_same_thread=False)
    cursor = conn.cursor()
except sqlite3.Error as e:
    st.error(f"Error connecting to the database: {e}")

def rapport():
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        tables = [t[0] for t in cursor.fetchall()]
    except sqlite3.Error as e:
        st.error(f"Failed to execute query: {e}")
        return

    selected_reporting_tables = st.sidebar.multiselect("Sélectionner des tables pour le rapport", options=tables)

    if selected_reporting_tables:
        st.markdown("# Rapport Final")

        report_data = []
        total_revenu_all_tables = 0
        total_depenses_all_tables = 0

        for table in selected_reporting_tables:
            df_report = load_table_data(table)
            total_revenu_report = df_report['revenu'].sum()
            total_depenses_report = df_report['depenses'].sum()

            report_data.append({
                'Table': table,
                'Total Débit': total_revenu_report,
                'Total Crédit': total_depenses_report
            })

            total_revenu_all_tables += total_revenu_report
            total_depenses_all_tables += total_depenses_report

        report_df = pd.DataFrame(report_data)

        summary_row = pd.DataFrame({
            'Table': ['Total'],
            'Total Débit': [total_revenu_all_tables],
            'Total Crédit': [total_depenses_all_tables]
        })

        report_df_with_totals = pd.concat([report_df, summary_row], ignore_index=True)

        cal1, cal2 = st.columns(2)

        with cal1:
            st.metric(label="Total Débit", value=f"{total_revenu_all_tables} ar")
        with cal2:
            st.metric(label="Total Crédit", value=f"{total_depenses_all_tables} ar")

        st.dataframe(report_df_with_totals, width=700,
                     column_config={
                         "Total Débit": st.column_config.NumberColumn(format="Ar %.2f"),
                         "Total Crédit": st.column_config.NumberColumn(format="Ar %.2f")}
                     )

        pdf_buffer = generateT_pdf(report_df_with_totals, filename=f"Rapport_du_{datetime.date.today()}.pdf")
        st.download_button(
            label="Exporter en PDF",
            data=pdf_buffer,
            file_name=f"Rapport_du_{datetime.date.today()}.pdf",
            mime="application/pdf"
        )

    else:
        st.image('nodata.png')

def load_table_data(table_name):
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    return df


