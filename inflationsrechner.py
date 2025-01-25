import streamlit as st
import matplotlib.pyplot as plt

# Titel des Rechners
st.title("💸 Luh Calm Sparkassen Inflationsrechner (ACHTUNG REALZINSFALLE)")
st.markdown("""
Mit diesem Tool können Sie den zukünftigen Wert Ihres Geldes berechnen, indem die Inflation berücksichtigt wird. 
Erfahren Sie, wie viel Kaufkraft Ihr Geld über die Zeit verliert und wie ein positiver Zinssatz dagegen wirken könnte.
""")

# Eingaben
st.sidebar.header("📥 Eingaben")
startbetrag = st.sidebar.number_input("💵 Startbetrag (€):", min_value=0.0, step=100.0, value=1000.0)
inflationsrate = st.sidebar.number_input("📈 Inflationsrate (% pro Jahr):", min_value=0.0, step=0.1, value=2.0)
zinsrate = st.sidebar.number_input("💵 Positiver Zinssatz (% pro Jahr):", min_value=0.0, step=0.1, value=0.5)
zeitraum = st.sidebar.number_input("⏳ Zeitraum (in Jahren):", min_value=1, step=1, value=10)

# Berechnung
if st.button("📊 Berechnung starten"):
    # Berechnung der Kaufkraftentwicklung ohne Zinsen
    endbetrag = startbetrag * ((1 - inflationsrate / 100) ** zeitraum)
    inflationsverlust = startbetrag - endbetrag

    # Berechnung der Kaufkraftentwicklung mit Zinsen (Realzinsfalle)
    endbetrag_mit_zins = startbetrag * ((1 + zinsrate / 100) ** zeitraum) * ((1 - inflationsrate / 100) ** zeitraum)
    kaufkraftverlust_mit_zins = startbetrag - endbetrag_mit_zins

    # Ergebnisse anzeigen
    st.markdown("### 📋 Ergebnisse")
    st.success(f"💼 Ursprünglicher Betrag: **{startbetrag:,.2f} €**")
    st.info(f"📉 Betrag nach {zeitraum} Jahren ohne Zinsen: **{endbetrag:,.2f} €**")
    st.info(f"📈 Betrag nach {zeitraum} Jahren mit {zinsrate}% Zinsen pro Jahr: **{endbetrag_mit_zins:,.2f} €**")
    st.error(f"🛒 Kaufkraftverlust ohne Zinsen: **{inflationsverlust:,.2f} €**")
    st.error(f"🛒 Kaufkraftverlust trotz Zinsen: **{kaufkraftverlust_mit_zins:,.2f} €**")

    # Grafische Darstellung
    jahre = list(range(zeitraum + 1))
    werte_ohne_zins = [startbetrag * ((1 - inflationsrate / 100) ** jahr) for jahr in jahre]
    werte_mit_zins = [startbetrag * ((1 + zinsrate / 100) ** jahr) * ((1 - inflationsrate / 100) ** jahr) for jahr in jahre]

    plt.figure(figsize=(10, 6))
    plt.plot(jahre, werte_ohne_zins, marker="o", label="Kaufkraft ohne Zinsen")
    plt.plot(jahre, werte_mit_zins, marker="o", label="Kaufkraft mit Zinsen", linestyle="--")
    plt.axhline(endbetrag, color="red", linestyle="--", label="Endbetrag ohne Zinsen")
    plt.axhline(endbetrag_mit_zins, color="green", linestyle="--", label="Endbetrag mit Zinsen")
    plt.title("Entwicklung der Kaufkraft")
    plt.xlabel("Jahre")
    plt.ylabel("Betrag (€)")
    plt.grid(True)
    plt.legend()

    st.pyplot(plt)

    st.markdown("""
    🔎 **Hinweis:** Diese Berechnung berücksichtigt sowohl Inflation als auch Zinsen. 
    Tatsächliche Werte können aufgrund wirtschaftlicher Schwankungen abweichen.
    """)

