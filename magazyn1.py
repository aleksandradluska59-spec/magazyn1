import streamlit as st
import pandas as pd

def main():
    """
    Zmodyfikowana funkcja dla prostego magazynu z cenami, VAT-em i wizualizacją.
    """
    st.set_page_config(layout="wide", page_title="Magazyn z Wizualizacją Cen")
    st.title("Magazyn z Wizualizacją i Wartością 📊")
    st.markdown("---")

    # Inicjalizacja stanu (lista resetuje się przy przeładowaniu)
    if 'magazyn' not in st.session_state:
        # Nowa struktura: id, nazwa, ilosc, cena_zakupu, vat
        st.session_state.magazyn = []

    # --- Sekcja Dodawania Towaru ---
    st.header("➕ Dodaj Nowy Towar i Dane Finansowe")
    
    with st.form("dodawanie_towaru", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nazwa = st.text_input("Nazwa Towaru:", key="nazwa_input")
            ilosc = st.number_input("Ilość:", min_value=1, step=1, value=1, key="ilosc_input")

        with col2:
            cena_zakupu = st.number_input("Cena Zakupu Netto (PLN):", min_value=0.01, step=0.01, value=10.00, format="%.2f", key="cena_zakupu_input")
            # Proste pole dla VAT (np. 23, 8, 5)
            vat_proc = st.number_input("Stawka VAT (%):", min_value=0, max_value=100, step=1, value=23, key="vat_input")
        
        # Przycisk dodawania
        dodaj_button = st.form_submit_button("Dodaj do Magazynu")

        if dodaj_button and nazwa and ilosc and cena_zakupu >= 0 and vat_proc >= 0:
            nowy_id = len(st.session_state.magazyn) + 1
            
            nowy_towar = {
                "id": nowy_id,
                "nazwa": nazwa.strip(),
                "ilosc": ilosc,
                "cena_zakupu": cena_zakupu,
                "vat_proc": vat_proc
            }
            st.session_state.magazyn.append(nowy_towar)
            st.success(f"Dodano: **{nazwa}** (Ilość: {ilosc}, Netto: {cena_zakupu:.2f} PLN)")
        elif dodaj_button and not nazwa:
             st.error("Wprowadź nazwę towaru.")

    st.markdown("---")
    
    # --- Sekcja Wizualizacji Danych i Podsumowania ---
    st.header("📈 Analiza Magazynu")

    if st.session_state.magazyn:
        df_magazyn = pd.DataFrame(st.session_state.magazyn)
        
        # Obliczenia wartości
        df_magazyn['wartosc_netto_jedn'] = df_magazyn['cena_zakupu']
        df_magazyn['wartosc_vat_jedn'] = df_magazyn['cena_zakupu'] * (df_magazyn['vat_proc'] / 100)
        df_magazyn['wartosc_brutto_jedn'] = df_magazyn['wartosc_netto_jedn'] + df_magazyn['wartosc_vat_jedn']
        
        df_magazyn['wartosc_netto_calosc'] = df_magazyn['
