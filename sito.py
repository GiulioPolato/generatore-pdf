import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos

st.title("🚀 Generatore PDF Push More")
st.subheader("Inserisci i dati per la tabella")

# Creiamo dei campi di input semplici
prodotto = st.text_input("Nome Prodotto", "VITAMINA D3+K2")
quantita = st.number_input("Quantità", min_value=1, value=186)
prezzo = st.text_input("Prezzo Unitario (es. EUR 3,72)", "EUR 3,72")

if st.button("Genera e Scarica PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "RIEPILOGO INVENTARIO PUSH MORE", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("helvetica", size=12)
    pdf.ln(10)
    
    # Creazione tabella con i dati inseriti nel sito
    with pdf.table() as table:
        header = table.row()
        header.cell("PRODOTTO")
        header.cell("QUANTITA'")
        header.cell("PREZZO")
        
        row = table.row()
        row.cell(prodotto)
        row.cell(str(quantita))
        row.cell(prezzo)
    
    # Genera il file in memoria per il download
    pdf_output = pdf.output()
    st.download_button(label="📥 Clicca qui per il tuo PDF", 
                       data=bytes(pdf_output), 
                       file_name="riepilogo.pdf", 
                       mime="application/pdf")