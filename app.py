import re
import streamlit as st
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data(path : str) -> tuple[pd.DataFrame, str]:
    try:
        df= pd.read_csv(path, sep=";", encoding="utf-8")

        # Patientenname muss im Namen der CSV-Datei vor ".csv" stehen. zB "Claudius.csv" -> Patient: "Claudius"
        patient = data_path.split("/")[-1].split(".")[0]

        cols = df.columns[1:]  # Alle Spalten außer "Datum"
        df[cols] = (
            df[cols]
            .astype(str)
            .apply(lambda col: col.str.strip().str.replace(",", ".", regex=False))
            .apply(pd.to_numeric, errors="coerce")
        )

        df["Datum"] = pd.to_datetime(df["Datum"], format="%Y-%m-%d", errors="coerce")
        df = df.sort_values("Datum")
        df.reset_index(drop=True, inplace=True)

        return df, patient
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return None

def debug():
    st.subheader("Debug - Start")
    y = "L-S"
    df_plot = pd.DataFrame({
        "Datum": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
        y: [1.0, 2.0, 3.0]
    })
    st.line_chart(
        data=df_plot,
        x="Datum",
        y=y,
    )

    st.subheader("Debug - Ende")

def add_data(df : pd.DataFrame = None):
    def make_num(s : str) -> float:
        if re.search('[a-zA-Z]', s) :
            raise ValueError(f"Ungültige Eingabe: '{s}' enthält Buchstaben.")
        if s is None or s.strip() == "":
            return ""
        s = s.strip().replace(",", ".")
        return pd.to_numeric(s, errors="coerce")


    st.subheader("Daten hinzufügen")
    with st.form("data_form"):
        datum = (st.date_input("Datum", value=pd.to_datetime("today"), format="YYYY-MM-DD"))
        datum = pd.to_datetime(datum, format="%Y-%m-%d", errors="coerce")

        r_s = st.text_input("R-S")
        l_s = st.text_input("L-S")
        r_corr_iop = st.text_input("R-corrIOP")
        l_corr_iop = st.text_input("L-corrIOP")
        submitted = st.form_submit_button("Daten hinzufügen")

        try:
            r_s = make_num(r_s)
            l_s = make_num(l_s)
            r_corr_iop = make_num(r_corr_iop)
            l_corr_iop = make_num(l_corr_iop)
        except ValueError as e:
            # Catch the ValueError raised by make_num and display a warning
            st.warning(f"Ungültige Eingabe: '{e}' enthält Buchstaben. Bitte geben Sie nur Zahlen ein.")
            return df


        if submitted:
            new_row = {
                "Datum": datum,
                "R-S": r_s,
                "L-S": l_s,
                "R-corrIOP": r_corr_iop,
                "L-corrIOP": l_corr_iop
            }
            df.loc[len(df)] = new_row
            df.to_csv(data_path, sep=";", index=False, encoding="utf-8")
            st.rerun()

        st.write("Datum bitte im Format YYYY-MM-DD eingeben, z.B. 2024-06-01")
        st.write("Wenn auf dem entsprechenden Feld des Ausdruck des Autorefraktometers \"NO DATA\" steht, " \
                "lassen Sie das entsprechende Feld leer.")
        st.write("In allen Feldern dürfen keine Buchstaben eingegeben werden.")
        st.write("Dezimalzahlen können mit Punkt oder Komma eingegeben werden, z.B. 1.5 oder 1,5")
    return df

def del_data(df : pd.DataFrame):
    if st.button("Letzte Zeile löschen"):
        if not df.empty:
            df = df[:-1]
        else:
            st.warning("Keine Daten zum Löschen vorhanden.")
        df.to_csv(data_path, sep=";", index=False, encoding="utf-8")
        st.rerun()
    return df

def data_prev(df : pd.DataFrame, patient : str):
    df_prev = df.copy()
    df_prev["Datum"] = df_prev["Datum"].dt.strftime("%Y-%m-%d")
    st.dataframe(df_prev)


def create_plots(colors=["#2ae93c", "#f89021"],):
    def add_line(fig, df, x_col, y_col, name, row, col, color, showlegend):
        df_trace = df[[x_col, y_col]].dropna(subset=[x_col, y_col])

        fig.add_trace(
            go.Scatter(
                x=df_trace[x_col],
                y=df_trace[y_col],
                mode="lines+markers",
                name=name,
                legendgroup=name,
                showlegend=showlegend,
                line=dict(color=color),
                marker=dict(color=color),
            ),
            row=row,
            col=col
        )


    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        subplot_titles=(
            "Sphäre über Zeit",
            "Augeninnendruck über Zeit"
        )
    )

    color_right = colors[0]
    color_left = colors[1]

    # Plot 1: Sphäre
    add_line( fig=fig, df=df,
        x_col="Datum",
        y_col="R-S",
        name="Rechtes Auge",
        row=1, col=1, color=color_right, showlegend=True
    )

    add_line( fig=fig, df=df,
        x_col="Datum",
        y_col="L-S",
        name="Linkes Auge",
        row=1, col=1, color=color_left, showlegend=True
    )

    # Plot 2: corrIOP
    add_line( fig=fig, df=df,
        x_col="Datum",
        y_col="R-corrIOP",
        name="Rechtes Auge",
        row=2, col=1, color=color_right, showlegend=False
    )

    add_line( fig=fig, df=df,
        x_col="Datum",
        y_col="L-corrIOP",
        name="Linkes Auge",
        row=2, col=1, color=color_left, showlegend=False
    )

    fig.update_layout(
        title=f"Patient: {patient}",
        height=700,
        hovermode="x unified",
        legend_title_text="Auge"
    )

    fig.update_yaxes(title_text="Sphäre [dpt]", row=1, col=1)
    fig.update_yaxes(title_text="corrIOP [mmHg]", row=2, col=1)
    fig.update_xaxes(title_text="Datum", row=2, col=1)

    st.plotly_chart(fig, width='stretch')


if __name__ == "__main__":

    st.title("Autorefraktometer Datenvisualisierung", text_alignment="center")

    # Beschreibung und Anweisungen
    st.write("Willkommen zur Datenvisualisierung für Autorefraktometer-Messungen! " \
            "Bitte geben Sie den vollständigen Dateipfad zu Ihrer CSV-Datei ein, um die Daten zu laden und zu visualisieren. " \
            "Danach können Sie hier die Messdaten Ihres Autorefraktometers einsehen, neue Messdaten hinzufügen oder die jeweilige letzte Zeile löschen. " \
            )
    st.write("Die CSV-Datei sollte nach dem Namen des Patienten benannt sein und " \
            "die folgenden Spalten enthalten: ") 
    st.write("Datum; R-S; L-S; R-corrIOP; L-corrIOP")
    st.write("Die Spaltennamen müssen exakt mit den gerade genannten Bezeichnungen übereinstimmen." \
            "Die Felder werden der darauf folgenden Zeilen werden durch ein Semikolon getrennt. " \
            "**Hier ein Beispiel:**"
            )
    st.code("""
            Datum; R-S; L-S; R-corrIOP; L-corrIOP
            2024-06-01; 1.5; 2.0; 15; 16
            2024-06-15; 1.0; 1.5; 14; 15
            2024-07-01; 0.5; 1.0; 13; 14
    """)

    # Eingabefeld für den Pfad zur CSV-Datei
    data_path = st.text_input("**Pfad zur CSV-Datei**", value="./data/Patient01.csv")

    df, patient = load_data(data_path)

    if df is not None:
        data_prev(df, patient)
        df = del_data(df)
        df = add_data(df)

        st.subheader("Datenvisualisierung")
        create_plots()