import re
from pathlib import Path

import streamlit as st
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def save_data(df: pd.DataFrame, data_path: str) -> None:
    path = Path(data_path).expanduser()
    if path.parent:
        path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, sep=';', index=False, encoding='utf-8')


def load_data(data_path: str = '') -> pd.DataFrame:
    try:
        if not data_path:
            return pd.DataFrame(columns=['Datum', 'R-S', 'L-S', 'R-corrIOP', 'L-corrIOP'])

        path = Path(data_path).expanduser()
        if path.is_dir():
            raise ValueError(f'Der angegebene Pfad ist ein Verzeichnis: {path}')

        if not path.exists():
            if path.parent:
                path.parent.mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame(columns=['Datum', 'R-S', 'L-S', 'R-corrIOP', 'L-corrIOP'])
            df.to_csv(path, sep=';', index=False, encoding='utf-8')
            return df

        df = pd.read_csv(path, sep=';', encoding='utf-8')

        cols = df.columns[1:]
        df[cols] = (
            df[cols]
            .astype(str)
            .apply(lambda col: col.str.strip().str.replace(',', '.', regex=False))
            .apply(pd.to_numeric, errors='coerce')
        )

        df['Datum'] = pd.to_datetime(df['Datum'], format='%Y-%m-%d', errors='coerce')
        df = df.sort_values('Datum')
        df.reset_index(drop=True, inplace=True)

        return df
    except Exception as e:
        st.error(f'Fehler beim Laden der Daten: {e}')
        return pd.DataFrame(columns=['Datum', 'R-S', 'L-S', 'R-corrIOP', 'L-corrIOP'])


def debug():
    st.subheader('Debug - Start')
    y = 'L-S'
    df_plot = pd.DataFrame({
        'Datum': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01']),
        y: [1.0, 2.0, 3.0]
    })
    st.line_chart(
        data=df_plot,
        x='Datum',
        y=y,
    )

    st.subheader('Debug - Ende')


def add_data(df: pd.DataFrame, data_path: str) -> pd.DataFrame:
    def make_num(s: str) -> float:
        if re.search(r'[a-zA-Z]', str(s)):
            raise ValueError(f'Ungültige Eingabe: "{s}" enthält Buchstaben.')
        if s is None or str(s).strip() == '':
            return ''
        s = str(s).strip().replace(',', '.')
        return pd.to_numeric(s, errors='coerce')

    st.subheader('Daten hinzufügen')
    with st.form('data_form'):
        datum = st.date_input('Datum', value=pd.to_datetime('today'), format='YYYY-MM-DD')
        datum = pd.to_datetime(datum, format='%Y-%m-%d', errors='coerce')

        r_s = st.text_input('R-S')
        l_s = st.text_input('L-S')
        r_corr_iop = st.text_input('R-corrIOP')
        l_corr_iop = st.text_input('L-corrIOP')
        submitted = st.form_submit_button('Daten hinzufügen')

        try:
            r_s = make_num(r_s)
            l_s = make_num(l_s)
            r_corr_iop = make_num(r_corr_iop)
            l_corr_iop = make_num(l_corr_iop)
        except ValueError as e:
            st.warning(str(e))
            return df

        if submitted:
            new_row = {
                'Datum': datum,
                'R-S': r_s,
                'L-S': l_s,
                'R-corrIOP': r_corr_iop,
                'L-corrIOP': l_corr_iop,
            }
            df.loc[len(df)] = new_row
            save_data(df, data_path)
            st.rerun()

        st.write('Datum bitte im Format YYYY-MM-DD eingeben, z.B. 2024-06-01')
        st.write('Wenn auf dem entsprechenden Feld des Ausdruck des Autorefraktometers "NO DATA" steht, '
                 'lassen Sie das entsprechende Feld leer.')
        st.write('In allen Feldern dürfen keine Buchstaben eingegeben werden.')
        st.write('Dezimalzahlen können mit Punkt oder Komma eingegeben werden, z.B. 1.5 oder 1,5')
    return df


def del_data(df: pd.DataFrame, data_path: str) -> pd.DataFrame:
    if st.button('Letzte Zeile löschen'):
        if not df.empty:
            df = df[:-1]
            save_data(df, data_path)
        else:
            st.warning('Keine Daten zum Löschen vorhanden.')
        st.rerun()
    return df


def data_prev(df: pd.DataFrame):
    df_prev = df.copy()
    if not df.empty:
        df_prev['Datum'] = df_prev['Datum'].dt.strftime('%Y-%m-%d')
    st.dataframe(df_prev)


def create_plots(df: pd.DataFrame, colors=['#2ae93c', '#f89021']):
    def add_line(fig, df, x_col, y_col, name, row, col, color, showlegend):
        df_trace = df[[x_col, y_col]].dropna(subset=[x_col, y_col])

        fig.add_trace(
            go.Scatter(
                x=df_trace[x_col],
                y=df_trace[y_col],
                mode='lines+markers',
                name=name,
                legendgroup=name,
                showlegend=showlegend,
                line=dict(color=color),
                marker=dict(color=color),
            ),
            row=row,
            col=col,
        )

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        subplot_titles=('Sphäre über Zeit', 'Augeninnendruck über Zeit'),
    )

    color_right = colors[0]
    color_left = colors[1]

    add_line(
        fig=fig,
        df=df,
        x_col='Datum',
        y_col='R-S',
        name='Rechtes Auge',
        row=1,
        col=1,
        color=color_right,
        showlegend=True,
    )
    add_line(
        fig=fig,
        df=df,
        x_col='Datum',
        y_col='L-S',
        name='Linkes Auge',
        row=1,
        col=1,
        color=color_left,
        showlegend=True,
    )
    add_line(
        fig=fig,
        df=df,
        x_col='Datum',
        y_col='R-corrIOP',
        name='Rechtes Auge',
        row=2,
        col=1,
        color=color_right,
        showlegend=False,
    )
    add_line(
        fig=fig,
        df=df,
        x_col='Datum',
        y_col='L-corrIOP',
        name='Linkes Auge',
        row=2,
        col=1,
        color=color_left,
        showlegend=False,
    )

    fig.update_layout(
        title='',
        height=700,
        hovermode='x unified',
        legend_title_text='Auge',
    )
    fig.update_yaxes(title_text='Sphäre [dpt]', row=1, col=1)
    fig.update_yaxes(title_text='corrIOP [mmHg]', row=2, col=1)
    fig.update_xaxes(title_text='Datum', row=2, col=1)

    st.plotly_chart(fig, width='stretch')


if __name__ == '__main__':
    st.title('Autorefraktometer Datenvisualisierung', text_alignment='center')

    default_data_path = './data/Claudius.csv'
    default_data_path = './tmp.csv'
    data_path = st.text_input('**Pfad zur CSV-Datei**', value=default_data_path)

    if not data_path:
        st.write(f'Default Pfad: {default_data_path}')
        data_path = default_data_path

    data_path = str(Path(data_path).expanduser())
    df = load_data(data_path)
    create_plots(df)

    if df is not None:
        data_prev(df)
        df = del_data(df, data_path)
        df = add_data(df, data_path)