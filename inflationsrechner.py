import streamlit as st
import matplotlib.pyplot as plt
import time

# Titel des Rechners
st.title("💸 Sparkassen Inflationsrechner (ACHTUNG REALZINSFALLE)")
st.markdown("""
Mit diesem Tool können Sie den zukünftigen Wert Ihres Geldes berechnen, indem die Inflation berücksichtigt wird. 
Erfahren Sie, wie viel Kaufkraft Ihr Geld über die Zeit verliert und wie ein positiver Zinssatz dagegen wirken könnte.

🔍 **Was ist die Realzinsfalle?**
Die Realzinsfalle beschreibt die Situation, in der selbst bei positiven Zinsen die Inflation dazu führt, dass Ihre tatsächliche Kaufkraft sinkt. 
Dieses Tool hilft Ihnen zu verstehen, wie sich Inflation und Zinsen gegenseitig beeinflussen.
""")

# Eingaben
st.sidebar.header("📥 Eingaben")
startbetrag = st.sidebar.number_input("💵 Startbetrag (€):", min_value=0.0, step=100.0, value=1000.0)
inflationsrate = st.sidebar.number_input("📈 Inflationsrate (% pro Jahr):", min_value=0.0, step=0.1, value=2.0)
zinsrate = st.sidebar.number_input("💵 Positiver Zinssatz (% pro Jahr):", min_value=0.0, step=0.1, value=0.5)
zeitraum = st.sidebar.number_input("⏳ Zeitraum (in Jahren):", min_value=1, step=1, value=10)

# Ladeanimation
if st.button("📊 Berechnung starten"):
    with st.spinner("Berechnungen werden durchgeführt..."):
        time.sleep(2)  # Simuliert eine kurze Wartezeit

        # Berechnung der Kaufkraftentwicklung ohne Zinsen
        endbetrag = startbetrag * ((1 - inflationsrate / 100) ** zeitraum)
        inflationsverlust = startbetrag - endbetrag

        # Berechnung der Kaufkraftentwicklung mit Zinsen (Realzinsfalle)
        endbetrag_mit_zins = startbetrag * ((1 + zinsrate / 100) ** zeitraum) * ((1 - inflationsrate / 100) ** zeitraum)
        kaufkraftverlust_mit_zins = startbetrag - endbetrag_mit_zins

        # Ergebnisse anzeigen
        st.markdown("### 📋 Ergebnisse")

        # Zusammenfassung als Karten
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="💼 Startbetrag", value=f"{startbetrag:,.2f} €")
        with col2:
            st.metric(label=f"📉 Betrag nach {zeitraum} Jahren (ohne Zinsen)", value=f"{endbetrag:,.2f} €", delta=f"-{inflationsverlust:,.2f} €", )
        with col3:
            st.metric(label=f"📈 Betrag mit {zinsrate:.2f}% Zinsen", value=f"{endbetrag_mit_zins:,.2f} €", delta=f"{endbetrag_mit_zins - startbetrag:,.2f} €", delta_color="normal" if endbetrag_mit_zins >= startbetrag else "inverse")

        st.markdown("""
        **Erklärung der Ergebnisse:**
        - Der Kaufkraftverlust ohne Zinsen zeigt, wie stark die Inflation allein Ihren Betrag reduziert.
        - Der Kaufkraftverlust trotz Zinsen verdeutlicht, dass Zinsen allein möglicherweise nicht ausreichen, um die Inflation auszugleichen.
        - Ein positiver Zinssatz kann die Verluste mindern, jedoch die Kaufkraft nicht vollständig erhalten, wenn die Inflationsrate höher ist.
        """)

        # Grafische Darstellung
        jahre = list(range(zeitraum + 1))
        werte_ohne_zins = [startbetrag * ((1 - inflationsrate / 100) ** jahr) for jahr in jahre]
        werte_mit_zins = [startbetrag * ((1 + zinsrate / 100) ** jahr) * ((1 - inflationsrate / 100) ** jahr) for jahr in jahre]

        plt.figure(figsize=(10, 6))
        plt.plot(jahre, werte_ohne_zins, marker="o", label="Kaufkraft ohne Zinsen", color="blue")
        plt.plot(jahre, werte_mit_zins, marker="o", label="Kaufkraft mit Zinsen", linestyle="--", color="green")
        plt.axhline(endbetrag, color="red", linestyle="--", label="Endbetrag ohne Zinsen")
        plt.axhline(endbetrag_mit_zins, color="green", linestyle="--", label="Endbetrag mit Zinsen")
        plt.title("Entwicklung der Kaufkraft")
        plt.xlabel("Jahre")
        plt.ylabel("Betrag (€)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()

        st.pyplot(plt)

        st.markdown("""
        🔎 **Hinweis:**
        - Diese Berechnung basiert auf einer konstanten Inflations- und Zinsrate.
        - Tatsächliche Werte können aufgrund wirtschaftlicher Schwankungen abweichen.
        - Die grafische Darstellung hilft Ihnen, den Einfluss der Inflation auf Ihre Ersparnisse besser zu verstehen.
        """)
