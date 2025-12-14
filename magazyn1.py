import streamlit as st

def main():
    """
    Główna funkcja aplikacji Streamlit dla prostego magazynu.
    Dane są przechowywane w pamięci (lista 'magazyn') i resetują się
    po przeładowaniu aplikacji, ponieważ nie używamy mechanizmu sesji.
    """
    st.set_page_config(layout="wide", page_title="Prosty Magazyn")
    st.title("Prosty Magazyn 📦")
    st.markdown("---")

    # Inicjalizacja listy towarów (magazynu).
    # UWAGA: Ta lista jest resetowana przy każdym przeładowaniu aplikacji
    # (zgodnie z Twoją prośbą o nieużywanie sesji i zapisywania danych).
    if 'magazyn' not in st.session_state:
        st.session_state.magazyn = []

    # --- Sekcja Dodawania Towaru ---
    st.header("➕ Dodaj Nowy Towar")
    
    with st.form("dodawanie_towaru", clear_on_submit=True):
        nazwa = st.text_input("Nazwa Towaru:", key="nazwa_input")
        ilosc = st.number_input("Ilość:", min_value=1, step=1, value=1, key="ilosc_input")
        
        # Przycisk dodawania
        dodaj_button = st.form_submit_button("Dodaj do Magazynu")

        if dodaj_button and nazwa and ilosc:
            # Tworzenie unikalnego identyfikatora dla prostoty
            # W bardziej zaawansowanym systemie użyłbyś UUID
            nowy_id = len(st.session_state.magazyn) + 1
            
            nowy_towar = {
                "id": nowy_id,
                "nazwa": nazwa.strip(),
                "ilosc": ilosc
            }
            st.session_state.magazyn.append(nowy_towar)
            st.success(f"Dodano: **{nazwa}** (Ilość: {ilosc})")
        elif dodaj_button and not nazwa:
             st.error("Wprowadź nazwę towaru, aby dodać go do magazynu.")

    st.markdown("---")

    # --- Sekcja Aktualnego Magazynu ---
    st.header("📋 Aktualny Stan Magazynu")
    
    if not st.session_state.magazyn:
        st.info("Magazyn jest pusty. Dodaj pierwszy towar powyżej.")
    else:
        # Konwersja listy słowników na DataFrame dla ładniejszej tabeli w Streamlit
        import pandas as pd
        df_magazyn = pd.DataFrame(st.session_state.magazyn)
        
        # Wyświetlanie danych w tabeli
        st.dataframe(
            df_magazyn.set_index('id').rename(columns={'nazwa': 'Nazwa Towaru', 'ilosc': 'Ilość'}), 
            use_container_width=True
        )

    st.markdown("---")

    # --- Sekcja Usuwania Towaru ---
    st.header("➖ Usuń Towar")

    if st.session_state.magazyn:
        # Tworzenie listy opcji do wyboru w selectbox: "ID - Nazwa Towaru"
        opcje_do_usuniecia = {
            f"{t['id']} - {t['nazwa']}": t['id'] 
            for t in st.session_state.magazyn
        }

        wybrana_opcja = st.selectbox(
            "Wybierz towar do usunięcia:",
            options=list(opcje_do_usuniecia.keys()),
            key="selectbox_usuwanie"
        )
        
        # Znajdowanie ID wybranego towaru
        id_do_usuniecia = opcje_do_usuniecia.get(wybrana_opcja)

        if st.button("Usuń Wybrany Towar"):
            if id_do_usuniecia is not None:
                # Filtracja listy: zostaw te elementy, których ID nie pasuje
                dlugosc_przed = len(st.session_state.magazyn)
                st.session_state.magazyn = [
                    t for t in st.session_state.magazyn 
                    if t['id'] != id_do_usuniecia
                ]
                
                if len(st.session_state.magazyn) < dlugosc_przed:
                    st.success(f"Usunięto: **{wybrana_opcja}**")
                    # Ponowne uruchomienie aplikacji, aby odświeżyć tabelę i selectbox
                    st.experimental_rerun()
                else:
                    st.warning("Nie udało się usunąć towaru.")
            else:
                st.error("Wybierz poprawny towar do usunięcia.")
    else:
        st.info("Brak towarów do usunięcia.")

if __name__ == "__main__":
    main()
