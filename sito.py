import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos

st.set_page_config(page_title="Generatore PDF Push More", layout="wide")

st.title("🚀 Generatore PDF Multiriga Push More")

# --- GESTIONE DATI (SESSION STATE) ---
# Inizializziamo la lista dei prodotti se non esiste
if 'lista_prodotti' not in st.session_state:
    st.session_state.lista_prodotti = []

# --- INTERFACCIA DI INSERIMENTO ---
with st.form("form_aggiunta"):
    st.subheader("Aggiungi un nuovo prodotto alla lista")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prodotto = st.text_input("Nome Prodotto", "VITAMINA D3+K2")
        formato = st.text_input("Formato", "60 cpr")
    with col2:
        quantita = st.number_input("Quantità", min_value=1, value=1)
        prezzo_testo = st.text_input("Prezzo Unitario (es. 3.72)", "3.72")
    with col3:
        lista_lotti = [f"L250{str(i).zfill(3)}" for i in range(1, 101)]
        lotto_scelto = st.selectbox("Lotto", lista_lotti)
        scadenza = st.text_input("Scadenza", "13/03/2028")

    submit = st.form_submit_button("➕ Aggiungi riga")

if submit:
    try:
        prezzo_f = float(prezzo_testo)
        totale_riga = quantita * prezzo_f
        # Salviamo la riga nella memoria del sito
        nuova_riga = {
            "prodotto": prodotto,
            "formato": formato,
            "quantita": quantita,
            "prezzo_u": prezzo_f,
            "prezzo_t": totale_riga,
            "lotto": lotto_scelto,
            "scadenza": scadenza
        }
        st.session_state.lista_prodotti.append(nuova_riga)
        st.success(f"Aggiunto: {prodotto}")
    except ValueError:
        st.error("Errore nel prezzo! Usa il punto per i decimali.")

# --- VISUALIZZAZIONE TABELLA NEL SITO ---
if st.session_state.lista_prodotti:
    st.subheader("Riepilogo prodotti inseriti")
    st.table(st.session_state.lista_prodotti)
    
    if st.button("🗑️ Svuota lista"):
        st.session_state.lista_prodotti = []
        st.rerun()

    # --- GENERAZIONE PDF ---
    if st.button("📄 Genera PDF con tutte le righe"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "RIEPILOGO INVENTARIO PUSH MORE", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)
        
        pdf.set_font("helvetica", size=9)
        
        with pdf.table() as table:
            # Intestazione
            h_row = table.row()
            for col in ["PRODOTTO", "FORMATO", "Q.TA", "PREZZO U.", "TOTALE", "LOTTO", "SCADENZA"]:
                h_row.cell(col)
            
            # Righe dinamiche
            totale_generale = 0
            for p in st.session_state.lista_prodotti:
                row = table.row()
                row.cell(p["prodotto"])
                row.cell(p["formato"])
                row.cell(str(p["quantita"]))
                row.cell(f"EUR {p['prezzo_u']:.2f}")
                row.cell(f"EUR {p['prezzo_t']:.2f}")
                row.cell(p["lotto"])
                row.cell(p["scadenza"])
                totale_generale += p["prezzo_t"]

        pdf.ln(5)
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 10, f"TOTALE COMPLESSIVO: EUR {totale_generale:.2f}", align="R")

        pdf_output = pdf.output()
        st.download_button(label="📥 Scarica PDF Finale", 
                           data=bytes(pdf_output), 
                           file_name="inventario_completo.pdf", 
                           mime="application/pdf")
