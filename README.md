# Autorefraktometer Datenvisualisierung

## Willkommen

Willkommen bei der Autorefraktometer Datenvisualisierungs-App. Diese Anwendung wurde für Anwender entwickelt, die Messdaten aus einem Autorefraktometer anschauen, speichern und ergänzen möchten – ohne Programmierkenntnisse.

Die App zeigt Ihre Daten als Tabelle und als Diagramm an. Sie können neue Messwerte hinzufügen oder die letzte Zeile löschen. Wenn die Standarddatei noch nicht existiert, legt die App sie automatisch an.

## Zweck

Diese Anwendung unterstützt Sie dabei:

- CSV-Daten aus einem Messgerät zu laden
- Messwerte übersichtlich anzuzeigen
- Verläufe in einer Grafik zu sehen
- neue Messdaten direkt in der App zu speichern
- die letzte erfasste Zeile zu löschen

## Installation

1. Öffnen Sie den Ordner `visRefra` in Ihrem Dateimanager.
2. Stellen Sie sicher, dass Python auf Ihrem Computer installiert ist.
   - Für Windows und macOS: https://www.python.org
3. Öffnen Sie ein Terminal oder eine Eingabeaufforderung im Ordner `visRefra`.
4. Installieren Sie die benötigten Programme mit:

```bash
pip install -r requirements.txt
```

5. Starten Sie die Anwendung mit:

```bash
streamlit run app.py
```

6. Im Terminal erscheint ein Link zur App. Öffnen Sie diesen Link im Browser.

## Erste Schritte

- Lassen Sie das Eingabefeld für den Dateipfad leer, wenn Sie die Standarddatei verwenden möchten.
- Die Standarddatei lautet `./data/tmp.csv`.
- Wenn diese Datei nicht existiert, wird sie automatisch erstellt.

## CSV-Datei bearbeiten

Die Anwendung verwendet CSV-Dateien mit genau diesen Spalten:

- `Datum`
- `R-S`
- `L-S`
- `R-corrIOP`
- `L-corrIOP`

Jede Zeile steht für einen Messwert. Werte müssen mit einem Semikolon (`;`) getrennt sein.

### Beispiel für eine gültige CSV-Datei

```csv
Datum;R-S;L-S;R-corrIOP;L-corrIOP
2024-06-01;1.5;2.0;15;16
2024-06-15;1.0;1.5;14;15
2024-07-01;0.5;1.0;13;14
```

### Wichtige Bearbeitungshinweise

- Die erste Zeile muss die Spaltenüberschriften enthalten.
- Das Datum muss im Format `YYYY-MM-DD` sein, zum Beispiel `2024-06-01`.
- Dezimalzahlen können mit Punkt (`1.5`) oder Komma (`1,5`) eingegeben werden.
- Leer gelassene Felder sind erlaubt, wenn für einen Messwert kein Wert vorliegt.
- Speichern Sie die Datei nach Änderungen im Texteditor.

## Nutzung der App

1. Starten Sie die App mit `streamlit run app.py`.
2. Geben Sie bei Bedarf den Pfad zur CSV-Datei ein.
3. Wenn kein Pfad eingegeben ist, wird `./data/Claudius.csv` verwendet.
4. Wenn die Datei fehlt, wird sie automatisch neu angelegt.
5. Neue Messwerte können Sie direkt im Formular erfassen und mit `Daten hinzufügen` speichern.
6. Mit `Letzte Zeile löschen` entfernen Sie die zuletzt gespeicherte Zeile.

## Tipps für Windows-Nutzer

- Sie können Dateipfade mit Backslashes schreiben, zum Beispiel `C:\Users\Name\data\Claudius.csv`.
- Alternativ funktionieren auch normale Schrägstriche: `C:/Users/Name/data/Claudius.csv`.
- Die App erzeugt fehlende Ordner automatisch, wenn der gewählte Pfad noch nicht existiert.

Viel Erfolg bei der Arbeit mit Ihren Autorefraktometer-Daten!
