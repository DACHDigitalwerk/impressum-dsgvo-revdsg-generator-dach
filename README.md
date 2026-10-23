# DACH Impressum & DSGVO / revDSG Compliance Engine 2026 🇩🇪 🇨🇭 🇦🇹

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DACH Legal Tech](https://img.shields.io/badge/Rechtsstand-2026_|_DDG_|_TDDDG_|_MStV_|_revDSG_|_ECG_|_MedienG-emerald.svg)](https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/)
[![Live Web App](https://img.shields.io/badge/Web_App-100%25_Kostenlos_&_DSGVO--konform-indigo.svg)](https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-0_Zero_Dependency-success.svg)](https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/)

> ⚖️ **Open-Source Compliance-Scanner & rechtssicherer Generator für Impressum und Datenschutzerklärung nach aktuellem Recht 2026 in Deutschland, der Schweiz und Österreich.**  
> Erkennt und verhindert typische Abmahnfallen: Veraltetes **§ 5 TMG** (ersetzt durch **§ 5 DDG**), veraltetes **TTDSG** (ersetzt durch **§ 25 TDDDG**), veralteter **§ 55 Abs. 2 RStV** (ersetzt durch **§ 18 Abs. 2 MStV**), fehlende Schweizer **revDSG- / UWG-Angaben** sowie fehlende österreichische **ECG- / MedienG-Blattlinien**.

---

### 🌐 Interaktiver Online-Generator & Scanner (Sofort im Browser nutzen)

**Erstellen Sie Ihr abmahnsicheres Impressum und Ihre Datenschutzerklärung mit 1 Klick oder scannen Sie Ihre bestehende Website:**  
👉 **[https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/](https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/)**

*(Entdecken Sie auch unsere weiteren 100 % clientseitigen DACH B2B- & Bürger-Tools: [Nebenkosten-Check](https://dach-digitalwerk.netlify.app/nebenkosten-check/) | [Abfindungs- & Kündigungsrechner](https://dach-digitalwerk.netlify.app/abfindung-kuendigung/) | [Arbeitszeugnis-Decoder](https://dach-digitalwerk.netlify.app/arbeitszeugnis/) | [Schweizer QR-Rechnung & XRechnung Suite](https://dach-digitalwerk.netlify.app/qr-suite/) | [Gesamte Rechner-Suite](https://dach-digitalwerk.netlify.app/rechner/))*

---

## Inhaltsverzeichnis
1. [Die Rechtslage 2026 im DACH-Raum im Überblick](#1-die-rechtslage-2026-im-dach-raum-im-überblick)
2. [Deutschland: Vom TMG zum DDG & vom TTDSG zum TDDDG](#2-deutschland-vom-tmg-zum-ddg--vom-ttdsg-zum-tdddg)
3. [Deutschland: Redaktionelle Verantwortung (§ 18 Abs. 2 MStV statt RStV)](#3-deutschland-redaktionelle-verantwortung--18-abs-2-mstv-statt-rstv)
4. [Schweiz: Das neue revDSG & Art. 3 Abs. 1 lit. s UWG Checkliste](#4-schweiz-das-neue-revdsg--art-3-abs-1-lit-s-uwg-checkliste)
5. [Österreich: § 5 ECG & § 25 MedienG Offenlegungspflicht ("Blattlinie")](#5-österreich--5-ecg--25-medieng-offenlegungspflicht-blattlinie)
6. [Abmahn-Checkliste 2026: Die 7 teuersten Fallen](#6-abmahn-checkliste-2026-die-7-teuersten-fallen)
7. [CLI- & Bibliotheks-Nutzung (Python & Node.js / Browser)](#7-cli---bibliotheks-nutzung-python--nodejs--browser)
8. [DACH Digitalwerk Suite & Lizenz](#8-dach-digitalwerk-suite--lizenz)

---

## 1. Die Rechtslage 2026 im DACH-Raum im Überblick

In den letzten 24 Monaten wurden im gesamten DACH-Raum fundamentale Gesetzesreformen verabschiedet, die bestehende Impressums- und Datenschutztexte veralten ließen:

| Land | Veraltete Rechtsnorm | Verbindliche Rechtsnorm 2026 | Anwendungsbereich & Pflicht |
| :--- | :--- | :--- | :--- |
| 🇩🇪 **DE** | **§ 5 TMG** (Telemediengesetz) | **§ 5 DDG** (Digitale-Dienste-Gesetz) | Impressumspflicht für alle geschäftsmäßigen digitalen Dienste |
| 🇩🇪 **DE** | **TTDSG** | **§ 25 TDDDG** | Einwilligungspflicht für Cookies & Gerätezugriffe (Local Storage) |
| 🇩🇪 **DE** | **§ 55 Abs. 2 RStV** | **§ 18 Abs. 2 MStV** | Nennung des redaktionell Verantwortlichen bei Blogs, News & Podcasts |
| 🇩🇪 / 🇪🇺 | ODR-Plattform (`ec.europa.eu/consumers/odr`) | **§ 36 VSBG** (Dispute Resolution) | Einstellung der EU-OS-Plattform; Klarstellung der Teilnahmebereitschaft |
| 🇨🇭 **CH** | Altes DSG (1992) | **revDSG (Art. 19, 16/17)** & **Art. 3 UWG** | Bekanntgabe von Personendaten ins Ausland, EDÖB, vollständige UID |
| 🇦🇹 **AT** | Fehlende Blattlinie | **§ 5 ECG** & **§ 25 MedienG** | Impressum, WKO-Kammer, Firmenbuch & Mediengesetz-Offenlegung (Blattlinie) |

---

## 2. Deutschland: Vom TMG zum DDG & vom TTDSG zum TDDDG

### 🇩🇪 Digitale-Dienste-Gesetz (DDG) – Das Ende des TMG
Mit dem **Gesetz zur Durchführung des Digital Services Act (Digitale-Dienste-Gesetz – DDG)** vom 14. Mai 2024 wurde das bewährte Telemediengesetz (TMG) vollständig aufgehoben.
* **Neuer Standard:** Aus der bekannten Formel *„Angaben gemäß § 5 TMG“* wird zwingend:
  $$\text{Rechtskonform 2026: } \textbf{Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)}$$
* **Risiko:** Die Fortführung veralteter TMG-Zitate wird von Mitbewerbern und Abmahnvereinen als Verletzung von Marktverhaltensregeln nach § 3a UWG abgemahnt.

### 🇩🇪 Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG)
Gleichzeitig wurde das erst 2021 eingeführte TTDSG umbenannt in **TDDDG**:
* **§ 25 Abs. 1 TDDDG:** Speicherung von Informationen in der Endeinrichtung des Nutzers (Cookies, Fingerprinting, LocalStorage) oder Zugriff auf solche Informationen ist nur mit vorheriger informierter Einwilligung zulässig.
* **§ 25 Abs. 2 TDDDG:** Ausnahme nur für technisch zwingend erforderliche Vorgänge.
* In allen Cookie-Bannern, Consent-Management-Plattformen (CMP) und Datenschutzerklärungen müssen die Verweise von **TTDSG** auf **TDDDG** aktualisiert werden.

---

## 3. Deutschland: Redaktionelle Verantwortung (§ 18 Abs. 2 MStV statt RStV)

Wer auf seiner Website journalistisch-redaktionelle Beiträge veröffentlicht (z. B. Fachartikel, Corporate Blogs, Podcasts, Branchen-News), muss nach **[§ 18 Abs. 2 Medienstaatsvertrag (MStV)](https://www.die-medienanstalten.de/service/medienstaatsvertrag)** einen inhaltlich Verantwortlichen namentlich benennen:

```text
Verantwortlich für den redaktionellen Inhalt nach § 18 Abs. 2 MStV:
Max Mustermann
Musterstraße 123
10115 Berlin
```

> ⚠️ **Achtung:** Die Benennung eines reinen Firmennamens oder eines Postfachs genügt nicht! Es muss zwingend eine **natürliche Person mit vollständiger Wohnanschrift** (Straße, Hausnummer, PLZ, Ort) genannt werden.

---

## 4. Schweiz: Das neue revDSG & Art. 3 Abs. 1 lit. s UWG Checkliste

Seit Inkrafttreten des totalrevidierten Bundesgesetzes über den Datenschutz (**revDSG**) und der revidierten Datenschutzverordnung (**DSV**) gelten in der Schweiz strikte Pflichten für Unternehmen, Vereine und Website-Betreiber:

### 🇨🇭 Schweizer Impressumspflicht (Art. 3 Abs. 1 lit. s UWG)
Wer im elektronischen Geschäftsverkehr Waren, Werke oder Leistungen anbietet, muss klare Angaben machen:
1. Vollständiger Name bzw. Firmenname (wie im Handelsregister eingetragen)
2. Physische Postadresse (kein reines Postfach)
3. Direkte Kontaktmöglichkeit inklusive E-Mail-Adresse und Telefonnummer
4. Schweizer Unternehmens-Identifikationsnummer (**UID**, z. B. `CHE-123.456.789 MWST / HR`)

### 🇨🇭 Datenschutzerklärung nach Art. 19 revDSG
Die Datenschutzerklärung muss zwingend enthalten:
* **Identität des Verantwortlichen:** Name, Sitz, Kontakt.
* **Bearbeitungszwecke:** Transparente Auflistung, wozu Daten erhoben werden.
* **Empfängerstaaten bei Auslandsübermittlung (Art. 16 / Art. 19 Abs. 2 lit. b revDSG):**  
  Werden Dienste US-amerikanischer Konzerne (Google, AWS, Microsoft, Netlify, Cloudflare) genutzt, müssen die Staaten (z. B. USA, EU/EWR) und die Übermittlungsgrundlage (z. B. **Swiss-U.S. Data Privacy Framework** oder Standardvertragsklauseln der Schweizer Aufsichtsbehörde) genannt werden.
* **Aufsichtsbehörde:** Nennung des **EDÖB** (Eidgenössischer Datenschutz- und Öffentlichkeitsbeauftragter, Feldeggweg 1, 3003 Bern).

---

## 5. Österreich: § 5 ECG & § 25 MedienG Offenlegungspflicht ("Blattlinie")

Kommerzielle Websites in Österreich unterliegen einer doppelten Regelung durch das E-Commerce-Gesetz und das Mediengesetz:

### 🇦🇹 Allgemeine Angaben nach § 5 E-Commerce-Gesetz (ECG)
* Firmenname und Rechtsform
* Geografische Anschrift
* E-Mail und Telefonnummer
* Firmenbuchnummer und Firmenbuchgericht
* Zuständige Kammer (in der Regel Wirtschaftskammer Österreich – **WKO**)
* Zuständige Gewerbe- bzw. Aufsichtsbehörde (Magistratisches Bezirksamt bzw. Bezirkshauptmannschaft)
* UID-Nummer (Umsatzsteuer-Identifikationsnummer mit Präfix `ATU`)

### 🇦🇹 Die Offenlegungspflicht nach § 25 Mediengesetz (MedienG)
Jedes Web-Medium mit redaktionellem Inhalt oder über die Basis-Visitenkarte hinausgehender Firmenpräsentation benötigt eine **Offenlegung**:
1. Vertretungsbefugte Organe (Geschäftsführer, Vorstand)
2. Gesellschafter und Eigentümerverhältnisse (Beteiligungen)
3. **Blattlinie („Grundlegende Richtung des Mediums“):**  
   *Muster:*  
   > *„Grundlegende Richtung des Mediums (Blattlinie nach § 25 MedienG): Information über Produkte, Softwarelösungen, rechtliche Trends und Dienstleistungen von [Firma].“*  
   Das Fehlen dieser Formulierung ist eine der häufigsten Ursachen für Beanstandungen in Österreich!

---

## 6. Abmahn-Checkliste 2026: Die 7 teuersten Fallen

1. ❌ **Dynamische Google Fonts via US-CDN:**  
   Einbindung über `fonts.googleapis.com` ohne vorherige Einwilligung überträgt IP-Adressen in die USA (Urteil des LG München I, Az. 3 O 17493/20).  
   *Lösung:* Fonts lokal via WOFF2 hosten oder über die [DACH Digitalwerk Suite](https://dach-digitalwerk.netlify.app/) einbinden.
2. ❌ **Veraltete Paragraphen (§ 5 TMG statt § 5 DDG, TTDSG statt TDDDG):**  
   Einfach durch automatisierten Regex-Scan findbar und von Mitbewerbern attackierbar.
3. ❌ **Toter ODR-Link der EU-Kommission:**  
   Die interaktive Plattform `ec.europa.eu/consumers/odr` wurde von der EU stillgelegt. Stattdessen reicht die klare Erklärung nach **§ 36 VSBG**, ob an einer Verbraucherschlichtung teilgenommen wird.
4. ❌ **Fehlende redaktionelle Kennzeichnung (§ 18 Abs. 2 MStV):**  
   Sobald ein Blog, Newsfeed oder Podcast existiert, muss eine namentlich benannte Person mit Anschrift genannt werden.
5. ❌ **Fehlende Blattlinie in Österreich (§ 25 MedienG):**  
   Österreichische Aufsichtsbehörden prüfen die „grundlegende Richtung“ bei jedem geschäftlichen Webauftritt.
6. ❌ **Schweizer revDSG ohne Nennung von Empfängerländern:**  
   Art. 19 revDSG verlangt die Nennung aller Staaten, in die Personendaten fließen.
7. ❌ **Dark Patterns im Cookie-Banner:**  
   „Alle ablehnen“ muss genauso einfach und prominent zugänglich sein wie „Alle akzeptieren“ (Art. 7 Abs. 3 DSGVO).

---

## 7. CLI- & Bibliotheks-Nutzung (Python & Node.js / Browser)

Dieses Repository liefert zwei vollständig abhängigkeitsfreie Werkzeuge (`impressum_dsgvo_checker.py` und `impressum_dsgvo_checker.js`), die sowohl im Terminal als auch als Import-Bibliothek betrieben werden können.

### Python 3 Ausführung

```bash
# 1. Selbsttest-Suite ausführen (9 automatisierte Tests)
python impressum_dsgvo_checker.py --test

# 2. Textdatei oder HTML-Quelltext scannen
python impressum_dsgvo_checker.py --file /pfad/zu/impressum.html --country DE

# 3. Live-URL per HTTP scannen
python impressum_dsgvo_checker.py --url https://meine-website.de/impressum

# 4. Rechtssicheres Impressum 2026 nach § 5 DDG & MStV generieren
python impressum_dsgvo_checker.py --generate-impressum --country DE --company "Digital Innovations GmbH" --person "Erika Muster"

# 5. Schweizer revDSG & UWG Impressum generieren
python impressum_dsgvo_checker.py --generate-impressum --country CH --company "Alpine Cloud AG" --vat-id "CHE-123.456.789 MWST"
```

### Python als Bibliothek einbinden

```python
from impressum_dsgvo_checker import scan_compliance, generate_impressum, generate_privacy_policy

# Compliance-Scan
result = scan_compliance("Angaben nach § 5 TMG. Cookies nach TTDSG.", country="DE")
print(f"Compliance Score: {result['score']}/100")
for finding in result["findings"]:
    print(f"- [{finding['severity']}] {finding['title']}: {finding['recommendation']}")

# Impressum generieren
impressum_markdown = generate_impressum({
    "country": "DE",
    "companyName": "TechVentures GmbH",
    "personName": "Alexander Schmidt",
    "street": "Friedrichstraße 100",
    "zipCity": "10117 Berlin",
    "email": "hallo@techventures.de",
    "phone": "+49 30 9876543",
    "vatId": "DE987654321"
})
print(impressum_markdown)
```

### Node.js / JavaScript Ausführung

```bash
# Selbsttest in Node.js ausführen
node impressum_dsgvo_checker.js --test

# Text analysieren
node impressum_dsgvo_checker.js --text "Angaben gemäß § 5 TMG. Muster GmbH." --country DE
```

### Als JavaScript-Modul (Node oder Browser)

```javascript
const { scanCompliance, generateImpressum, generatePrivacyPolicy } = require('./impressum_dsgvo_checker.js');

const analysis = scanCompliance('Angaben gemäß § 5 TMG...', 'DE');
console.log(`Score: ${analysis.score}/100, Rechtskonform: ${analysis.isCompliant}`);

const privacyText = generatePrivacyPolicy({
  country: 'CH',
  companyName: 'Helvetia Tech AG',
  personName: 'Marc Keller',
  email: 'datenschutz@helvetia-tech.ch'
});
console.log(privacyText);
```

---

## 8. DACH Digitalwerk Suite & Lizenz

DACH Digitalwerk entwickelt führende, 100 % browserbasierte und datenschutzkonforme Produktivitäts- und Legal-Tech-Werkzeuge für den deutschsprachigen Raum:

* 🌐 **[DACH Impressum & Datenschutz Generator 2026](https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/)** – Interaktiver Web-Generator für DE, AT, CH mit sofortiger PDF- & Markdown-Ausgabe.
* 🏢 **[Nebenkosten- & Heizkosten-Prüfer](https://dach-digitalwerk.netlify.app/nebenkosten-check/)** – Fehlerhafte Betriebskosten nach BGB & HeizkostenV aufdecken.
* 💼 **[Abfindungs- & Kündigungsfrist-Rechner](https://dach-digitalwerk.netlify.app/abfindung-kuendigung/)** – Regelabfindung nach § 1a KSchG & Fristen nach § 622 BGB / Art. 335c OR berechnen.
* 🔍 **[Arbeitszeugnis Geheimcode-Decoder](https://dach-digitalwerk.netlify.app/arbeitszeugnis/)** – Über 140 versteckte HR-Formulierungen lokal im Browser analysieren.
* 🧾 **[Schweizer QR-Rechnung & XRechnung 3.0 Suite](https://dach-digitalwerk.netlify.app/qr-suite/)** – SIX-konforme QR-Rechnungen und B2G-konforme E-Rechnungen erstellen.
* ⚡ **[DACH Digitalwerk Pro-Checkout](https://dachdigital.gumroad.com/l/gthgwc)** – Professionelle Gewerbelizenzen, API-Templates und erweiterte B2B-Musterverträge.

---

### Lizenz
Veröffentlicht unter der **[MIT License](LICENSE)** – Copyright © 2026 [DACH Digitalwerk](https://dach-digitalwerk.netlify.app). Frei nutzbar für private und kommerzielle Projekte.
