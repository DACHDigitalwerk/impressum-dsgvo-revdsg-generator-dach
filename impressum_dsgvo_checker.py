#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DACH Impressum & DSGVO/revDSG Compliance Checker 2026
Erkennt Abmahnfallen nach aktuellem Recht in Deutschland, Österreich und der Schweiz:
- DDG (ehemals § 5 TMG)
- § 25 TDDDG (ehemals TTDSG)
- § 18 Abs. 2 MStV (ehemals § 55 Abs. 2 RStV)
- Schweizer revDSG (Art. 19, Art. 16/17) & Art. 3 Abs. 1 lit. s UWG
- Österreichisches ECG (§ 5) & MedienG (§ 25 Blattlinie/Offenlegung)

Live Web-App: https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/
Copyright (c) 2026 DACH Digitalwerk (MIT License)
"""

import sys
import os
import re
import json
import argparse
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional


SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"


def scan_compliance(text: str, country: str = "ALL") -> Dict[str, Any]:
    """
    Scannt einen Impressums- oder Datenschutztext auf rechtliche Risiken und veraltete Gesetzesverweise
    nach der Rechtslage 2026 für Deutschland (DE), Österreich (AT) und die Schweiz (CH).
    """
    country = country.upper()
    findings: List[Dict[str, Any]] = []

    # 1. Veraltetes Telemediengesetz (TMG -> DDG)
    tmg_matches = re.findall(r"(?:§\s*5\s+)?TMG|Telemediengesetz", text, re.IGNORECASE)
    if tmg_matches:
        findings.append({
            "id": "OUTDATED_TMG",
            "title": "Veralteter Verweis auf § 5 TMG statt § 5 DDG",
            "severity": SEVERITY_CRITICAL,
            "category": "DE",
            "legalBasis": "Digitale-Dienste-Gesetz (DDG) vom 14. Mai 2024 / Rechtsstand 2026",
            "description": (
                "Das Telemediengesetz (TMG) wurde durch das Digitale-Dienste-Gesetz (DDG) abgelöst. "
                "Die Impressumspflicht für Anbieter digitaler Dienste folgt nun aus § 5 DDG. "
                "Ein veralteter Verweis auf '§ 5 TMG' stellt eine formelle Falschangabe und Abmahnfalle dar."
            ),
            "recommendation": "Ersetzen Sie sämtliche Verweise auf '§ 5 TMG' durch '§ 5 DDG' oder 'Angaben gemäß § 5 DDG'.",
            "snippet": tmg_matches[0]
        })

    # 2. Veraltetes TTDSG (TTDSG -> TDDDG)
    ttdsg_matches = re.findall(r"TTDSG|Telekommunikation-Telemedien-Datenschutz-Gesetz", text, re.IGNORECASE)
    if ttdsg_matches:
        findings.append({
            "id": "OUTDATED_TTDSG",
            "title": "Veralteter Verweis auf TTDSG statt § 25 TDDDG",
            "severity": SEVERITY_CRITICAL,
            "category": "DE",
            "legalBasis": "Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG)",
            "description": (
                "Das TTDSG wurde synchron zum Inkrafttreten des DDG in TDDDG umbenannt. "
                "Die Rechtsgrundlage für Cookies und Geräteabfragen (Einwilligungspflicht) lautet zwingend § 25 TDDDG."
            ),
            "recommendation": "Ersetzen Sie 'TTDSG' bzw. '§ 25 TTDSG' durch '§ 25 TDDDG' (Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz).",
            "snippet": ttdsg_matches[0]
        })

    # 3. Veralteter Rundfunkstaatsvertrag (RStV -> MStV)
    rstv_matches = re.findall(r"(?:§\s*55\s+Abs\.?\s*2\s+)?RStV|Rundfunkstaatsvertrag", text, re.IGNORECASE)
    if rstv_matches:
        findings.append({
            "id": "OUTDATED_RSTV",
            "title": "Veralteter Verweis auf § 55 Abs. 2 RStV statt § 18 Abs. 2 MStV",
            "severity": SEVERITY_HIGH,
            "category": "DE",
            "legalBasis": "Medienstaatsvertrag (MStV) § 18 Abs. 2",
            "description": (
                "Der Rundfunkstaatsvertrag (RStV) ist seit November 2020 außer Kraft. "
                "Die Pflicht zur Benennung eines inhaltlich Verantwortlichen für redaktionelle Inhalte "
                "ergibt sich seither aus § 18 Abs. 2 Medienstaatsvertrag (MStV)."
            ),
            "recommendation": "Aktualisieren Sie die redaktionelle Kennzeichnung auf: 'Verantwortlich für den redaktionellen Inhalt gemäß § 18 Abs. 2 MStV: Vorname Nachname, Adresse'.",
            "snippet": rstv_matches[0]
        })

    # 4. Fehlende MStV-Angabe bei redaktionellen Inhalten (DE)
    editorial_signals = ["blog", "magazin", "news", "artikel", "beitrag", "podcast", "kommentar", "redaktion"]
    has_editorial_hint = any(re.search(r"\b" + sig + r"\b", text, re.IGNORECASE) for sig in editorial_signals)
    has_mstv = bool(re.search(r"(?:§\s*18\s+Abs\.?\s*2\s+MStV|Medienstaatsvertrag)", text, re.IGNORECASE))
    if country in ("DE", "ALL") and has_editorial_hint and not has_mstv and not rstv_matches:
        findings.append({
            "id": "MISSING_MSTV",
            "title": "Möglicherweise fehlende Angabe nach § 18 Abs. 2 MStV für redaktionelle Inhalte",
            "severity": SEVERITY_MEDIUM,
            "category": "DE",
            "legalBasis": "§ 18 Abs. 2 MStV (Deutschland)",
            "description": (
                "Auf der Website finden sich Hinweise auf redaktionelle oder journalistische Inhalte (Blog, News, Fachartikel). "
                "Telemedien mit journalistisch-redaktionell gestalteten Angeboten müssen zwingend eine verantwortliche Person "
                "mit vollständiger Wohnanschrift benennen (§ 18 Abs. 2 MStV)."
            ),
            "recommendation": "Fügen Sie im Impressum hinzu: 'Verantwortlich für den redaktionellen Inhalt nach § 18 Abs. 2 MStV: [Vorname Nachname], [vollständige Wohnanschrift]'.",
            "snippet": "Redaktionelle Signalwörter im Text erkannt, kein § 18 Abs. 2 MStV gefunden"
        })

    # 5. Veraltete / eingestellte EU-Streitbeilegung (ODR-Plattform / OS-Plattform)
    odr_matches = re.findall(r"ec\.europa\.eu/consumers/odr", text, re.IGNORECASE)
    has_vsbg = bool(re.search(r"(?:§\s*36\s+VSBG|Verbraucherstreitbeilegung|Universalschlichtungsstelle|Verbraucherschlichtung)", text, re.IGNORECASE))
    if odr_matches:
        # Prüfe ob Text bereits auf Einstellung/Neuregelung der OS-Plattform hinweist
        has_sunset_notice = bool(re.search(r"(?:eingestellt|stillgelegt|außer betrieb|abgeschaltet|historisch|einstellung)", text, re.IGNORECASE))
        if not has_sunset_notice:
            findings.append({
                "id": "OBSOLETE_ODR_LINK",
                "title": "Abmahngefahr: Veralteter Link auf die stillgelegte EU-OS-Plattform",
                "severity": SEVERITY_MEDIUM,
                "category": "DE/AT",
                "legalBasis": "EU-Verordnung über die Einstellung der europäischen OS-Plattform & § 36 VSBG",
                "description": (
                    "Die Europäische Kommission hat die bisherige interaktive Online-Streitbeilegungs-Plattform (OS-Plattform unter ec.europa.eu/consumers/odr) "
                    "stillgelegt. Die bisherige Verpflichtung zur Verlinkung ist entfallen; tote oder irreführende Links "
                    "stellen ein wettbewerbsrechtliches Abmahnrisiko dar. Relevant bleibt allein die Erklärung nach § 36 VSBG."
                ),
                "recommendation": "Entfernen Sie den toten OS-Link 'ec.europa.eu/consumers/odr' und belassen Sie die standardmäßige Erklärung nach § 36 VSBG.",
                "snippet": odr_matches[0]
            })
    elif country in ("DE", "ALL") and not has_vsbg and ("impressum" in text.lower() or "anbieterkennzeichnung" in text.lower()):
        findings.append({
            "id": "MISSING_VSBG",
            "title": "Fehlender Hinweis zur Verbraucherstreitbeilegung nach § 36 VSBG",
            "severity": SEVERITY_LOW,
            "category": "DE",
            "legalBasis": "§ 36 Verbraucherstreitbeilegungsgesetz (VSBG)",
            "description": (
                "Unternehmen müssen im Impressum klar darüber informieren, "
                "ob sie an einem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilnehmen oder nicht."
            ),
            "recommendation": "Fügen Sie eine klare Erklärung nach § 36 VSBG hinzu.",
            "snippet": "Keine VSBG-Erklärung im Impressum gefunden"
        })

    # 6. Schweiz (CH) – revDSG & UWG Checks
    if country in ("CH", "ALL"):
        has_ch_signals = bool(re.search(r"\b(?:schweiz|switzerland|ch|gmbh|ag|chf|eidgenössisch|edöb|uid|che-)\b", text, re.IGNORECASE))
        has_revdsg = bool(re.search(r"\b(?:revDSG|Datenschutzgesetz|DSG|EDÖB)\b", text, re.IGNORECASE))
        has_ch_abroad_transfer = bool(re.search(r"(?:ausland|drittstaat|bekanntgabe ins ausland|art\.?\s*16|art\.?\s*17|standardvertragsklauseln|swiss-us)", text, re.IGNORECASE))
        has_ch_uid = bool(re.search(r"CHE-\d{3}\.\d{3}\.\d{3}", text, re.IGNORECASE))
        has_uwg_identity = bool(re.search(r"(?:Art\.?\s*3\s+Abs\.?\s*1\s+lit\.?\s*s\s+UWG|Bundesgesetz gegen den unlauteren Wettbewerb)", text, re.IGNORECASE))

        # Falls Text Datenschutz betrifft
        is_privacy_text = bool(re.search(r"(?:datenschutz|privacy|personendaten|bearbeitung)", text, re.IGNORECASE))
        if is_privacy_text and not has_revdsg and (country == "CH" or (has_ch_signals and "schweiz" in text.lower())):
            findings.append({
                "id": "MISSING_CH_REVDSG",
                "title": "Fehlende Übereinstimmung mit dem neuen Schweizer Datenschutzgesetz (revDSG)",
                "severity": SEVERITY_HIGH,
                "category": "CH",
                "legalBasis": "Bundesgesetz über den Datenschutz (revDSG, Art. 19)",
                "description": (
                    "Für Websites mit Schweizer Nutzern oder Schweizer Anbietern gilt das revDSG. "
                    "Art. 19 revDSG verlangt die Information über die Beschaffung von Personendaten, Bearbeitungszwecke "
                    "und insbesondere die Angabe der Staaten, in die Personendaten übermittelt werden (Art. 16 revDSG)."
                ),
                "recommendation": "Ergänzen Sie die Datenschutzerklärung um Bezüge zum Schweizer revDSG, den EDÖB als Aufsichtsbehörde und die Auslandsbekanntgabe.",
                "snippet": "Kein revDSG-Bezug in Datenschutzerklärung vorhanden"
            })

        if is_privacy_text and has_revdsg and not has_ch_abroad_transfer:
            findings.append({
                "id": "MISSING_CH_TRANSFER_NOTICE",
                "title": "Fehlende Angabe zur Datenbekanntgabe ins Ausland nach Art. 19 Abs. 2 lit. b revDSG",
                "severity": SEVERITY_MEDIUM,
                "category": "CH",
                "legalBasis": "Art. 19 Abs. 2 lit. b i.V.m. Art. 16/17 revDSG",
                "description": (
                    "Das revDSG schreibt zwingend vor, dass die Staaten genannt werden müssen, in welche Personendaten "
                    "übermittelt werden (z. B. USA bei Nutzung von Cloud-, CDN- oder Maildiensten), sowie allfällige Garantien."
                ),
                "recommendation": "Benennen Sie explizit die Empfängerstaaten (z.B. Schweiz, EU/EWR, USA) und Garantien (z.B. Swiss-US Data Privacy Framework / SCC).",
                "snippet": "Hinweis auf Staaten der Datenübermittlung fehlt"
            })

        # Schweizer Impressumspflicht (Art. 3 Abs. 1 lit. s UWG)
        is_impressum_text = bool(re.search(r"(?:impressum|kontakt|über uns)", text, re.IGNORECASE))
        if is_impressum_text and (country == "CH" or (has_ch_signals and "schweiz" in text.lower())):
            if not has_ch_uid and not re.search(r"(?:UID|Unternehmens-Identifikationsnummer)", text, re.IGNORECASE):
                findings.append({
                    "id": "MISSING_CH_UID",
                    "title": "Fehlende Schweizer UID (CHE-Nummer)",
                    "severity": SEVERITY_LOW,
                    "category": "CH",
                    "legalBasis": "Art. 3 Abs. 1 lit. s UWG & Bundesgesetz über die Unternehmens-Identifikationsnummer (UIDG)",
                    "description": (
                        "Im Schweizer Handelsregister eingetragene Unternehmen müssen im elektronischen Geschäftsverkehr "
                        "ihre UID-Nummer im Format CHE-xxx.xxx.xxx angeben."
                    ),
                    "recommendation": "Geben Sie die UID-Nummer im Impressum an: 'UID: CHE-xxx.xxx.xxx MWST/HR'.",
                    "snippet": "Keine CHE-Nummer gefunden"
                })

    # 7. Österreich (AT) – ECG & MedienG Checks
    if country in ("AT", "ALL"):
        has_at_signals = bool(re.search(r"\b(?:österreich|austria|wien|graz|linz|salzburg|innsbruck|atu|wko|firmenbuch|firmenbuchgericht)\b", text, re.IGNORECASE))
        has_ecg = bool(re.search(r"(?:§\s*5\s+ECG|E-Commerce-Gesetz)", text, re.IGNORECASE))
        has_medieng = bool(re.search(r"(?:§\s*25\s+MedienG|Mediengesetz|Offenlegung|Blattlinie|grundlegende Richtung)", text, re.IGNORECASE))
        has_blattlinie = bool(re.search(r"(?:Blattlinie|grundlegende Richtung)", text, re.IGNORECASE))

        is_impressum_text = bool(re.search(r"(?:impressum|kontakt|offenlegung)", text, re.IGNORECASE))
        if is_impressum_text and (country == "AT" or (has_at_signals and "österreich" in text.lower())):
            if not has_ecg:
                findings.append({
                    "id": "MISSING_AT_ECG",
                    "title": "Fehlende Ausweisung der Informationspflichten nach § 5 ECG (Österreich)",
                    "severity": SEVERITY_HIGH,
                    "category": "AT",
                    "legalBasis": "§ 5 E-Commerce-Gesetz (ECG) Österreich",
                    "description": (
                        "In Österreich regelt § 5 ECG die allgemeinen Informationspflichten für kommerzielle Websites. "
                        "Erforderlich sind Firmenbuchnummer, Firmenbuchgericht, zuständige Kammer (WKO) sowie die UID (ATU...)."
                    ),
                    "recommendation": "Verweisen Sie im Impressum auf 'Angaben gemäß § 5 E-Commerce-Gesetz (ECG)' und listen Sie Kammer, Behörde und FN auf.",
                    "snippet": "Kein Hinweis auf § 5 ECG gefunden"
                })

            if not has_medieng or not has_blattlinie:
                findings.append({
                    "id": "MISSING_AT_BLATTLINIE",
                    "title": "Fehlende Offenlegung / Blattlinie nach § 25 Mediengesetz (MedienG AT)",
                    "severity": SEVERITY_HIGH,
                    "category": "AT",
                    "legalBasis": "§ 25 MedienG (Österreich)",
                    "description": (
                        "Nach § 25 Mediengesetz (MedienG) besteht in Österreich eine strikte Offenlegungspflicht. "
                        "Bei Websites mit über die reine Firmenpräsentation hinausgehenden Inhalten muss zwingend die "
                        "'grundlegende Richtung des Mediums' ('Blattlinie') sowie Eigentümer- und Vertretungsverhältnisse angegeben werden. "
                        "Das Fehlen der Blattlinie ist einer der häufigsten Abmahngründe der Wirtschaftskammer und von Konkurrenten."
                    ),
                    "recommendation": "Fügen Sie eine Blattlinie ein: 'Grundlegende Richtung des Mediums (Blattlinie): Information über Produkte, Dienstleistungen und Branchentrends von [Firma]'.",
                    "snippet": "Keine Blattlinie / § 25 MedienG Offenlegung gefunden"
                })

    # 8. Externe Google Fonts ohne Einwilligung (LG München I Risiko)
    google_fonts_matches = re.findall(r"fonts\.googleapis\.com|fonts\.gstatic\.com", text, re.IGNORECASE)
    if google_fonts_matches:
        findings.append({
            "id": "REMOTE_GOOGLE_FONTS_RISK",
            "title": "Verdacht auf dynamisches Nachladen von Google Fonts (LG München I Risiko)",
            "severity": SEVERITY_HIGH,
            "category": "ALL",
            "legalBasis": "Art. 6 Abs. 1 DSGVO / LG München I (Az. 3 O 17493/20)",
            "description": (
                "Das dynamische Nachladen von Schriftarten direkt von Google-Servern (fonts.googleapis.com / fonts.gstatic.com) "
                "überträgt die IP-Adresse des Website-Besuchers an Server in den USA. Ohne vorherige ausdrückliche Einwilligung "
                "stellt dies eine Datenschutzverletzung dar und hat zu massenhaften Abmahnwellen geführt."
            ),
            "recommendation": "Hosten Sie alle Webfonts (WOFF2) lokal auf Ihrem eigenen Server oder binden Sie diese erst nach Cookie-Consent ein.",
            "snippet": google_fonts_matches[0]
        })

    # 9. Fehlende Widerrufs- / Widerspruchsrechte in Datenschutzerklärung
    is_privacy_text = bool(re.search(r"(?:datenschutz|privacy|verarbeitung von personendaten)", text, re.IGNORECASE))
    has_widerruf = bool(re.search(r"(?:widerruf|widerspruch|art\.?\s*21\s+dsgvo)", text, re.IGNORECASE))
    if is_privacy_text and not has_widerruf:
        findings.append({
            "id": "MISSING_RIGHT_TO_REVOKE",
            "title": "Fehlender Hinweis auf das Widerspruchs- und Widerrufsrecht",
            "severity": SEVERITY_HIGH,
            "category": "ALL",
            "legalBasis": "Art. 7 Abs. 3, Art. 21 DSGVO & Art. 25 ff. revDSG",
            "description": (
                "Betroffene Personen müssen ausdrücklich und transparent darüber aufgeklärt werden, "
                "dass sie erteilte Einwilligungen jederzeit mit Wirkung für die Zukunft widerrufen und Verarbeitungen "
                "auf Grundlage von berechtigten Interessen widersprechen können."
            ),
            "recommendation": "Fügen Sie einen prominenten Abschnitt über das Recht auf Widerruf der Einwilligung und das Widerspruchsrecht ein.",
            "snippet": "Keine Widerrufs-/Widerspruchsklausel in Datenschutzerklärung gefunden"
        })

    # 10. SSL/TLS Verschlüsselungshinweis
    has_ssl = bool(re.search(r"(?:ssl|tls|verschlüsselung|https)", text, re.IGNORECASE))
    if is_privacy_text and not has_ssl:
        findings.append({
            "id": "MISSING_SSL_NOTE",
            "title": "Fehlender Hinweis auf SSL-/TLS-Verschlüsselung",
            "severity": SEVERITY_LOW,
            "category": "ALL",
            "legalBasis": "Art. 32 DSGVO / Art. 8 revDSG (Sicherheit der Datenverarbeitung)",
            "description": (
                "Zur Gewährleistung der Datensicherheit und zum Schutz vertraulicher Inhalte (z.B. Bestellungen oder Anfragen) "
                "ist eine Transportverschlüsselung (SSL/TLS) vorgeschrieben und in der Datenschutzerklärung zu erläutern."
            ),
            "recommendation": "Ergänzen Sie den Standard-Passus über SSL-/TLS-Verschlüsselung zum Schutz von Übertragungen.",
            "snippet": "Keine Erwähnung von SSL/TLS-Verschlüsselung gefunden"
        })

    # Compliance-Score-Berechnung (Start bei 100)
    score = 100
    for item in findings:
        sev = item["severity"]
        if sev == SEVERITY_CRITICAL:
            score -= 35
        elif sev == SEVERITY_HIGH:
            score -= 20
        elif sev == SEVERITY_MEDIUM:
            score -= 10
        elif sev == SEVERITY_LOW:
            score -= 5
    score = max(0, min(100, score))

    summary = {
        "critical": sum(1 for f in findings if f["severity"] == SEVERITY_CRITICAL),
        "high": sum(1 for f in findings if f["severity"] == SEVERITY_HIGH),
        "medium": sum(1 for f in findings if f["severity"] == SEVERITY_MEDIUM),
        "low": sum(1 for f in findings if f["severity"] == SEVERITY_LOW),
    }

    return {
        "score": score,
        "isCompliant": score >= 85 and summary["critical"] == 0 and summary["high"] == 0,
        "countryFilter": country,
        "totalFindings": len(findings),
        "summary": summary,
        "findings": findings,
        "liveGeneratorUrl": "https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/"
    }


def generate_impressum(config: Dict[str, Any]) -> str:
    """
    Generiert ein rechtssicheres, an die Rechtslage 2026 angepasstes Impressum für DE, AT oder CH.
    """
    country = config.get("country", "DE").upper()
    company = config.get("companyName", "Musterfirma GmbH")
    person = config.get("personName", "Max Mustermann")
    legal_form = config.get("legalForm", "GmbH")
    street = config.get("street", "Musterstraße 123")
    zip_city = config.get("zipCity", "8001 Zürich" if country == "CH" else ("1010 Wien" if country == "AT" else "10115 Berlin"))
    email = config.get("email", "kontakt@musterfirma.ch" if country == "CH" else "kontakt@musterfirma.de")
    phone = config.get("phone", "+41 44 123 45 67" if country == "CH" else "+49 30 1234567")
    vat_id = config.get("vatId", "CHE-123.456.789 MWST" if country == "CH" else ("ATU12345678" if country == "AT" else "DE123456789"))
    reg_court = config.get("registerCourt", "Handelsregisteramt Zürich" if country == "CH" else ("Handelsgericht Wien" if country == "AT" else "Amtsgericht Charlottenburg"))
    reg_number = config.get("registerNumber", "CH-020.1.234.567-8" if country == "CH" else ("FN 123456 a" if country == "AT" else "HRB 123456 B"))
    editorial_person = config.get("editorialResponsible", person)
    has_editorial = config.get("hasEditorialContent", True)
    chamber = config.get("chamber", "Wirtschaftskammer Österreich (WKO)" if country == "AT" else "IHK Berlin")
    supervisory_authority = config.get("supervisoryAuthority", "Magistratisches Bezirksamt" if country == "AT" else "Gewerbeamt Berlin")

    lines = []
    lines.append(f"# Impressum")
    lines.append("")

    if country == "DE":
        lines.append("## Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)")
        lines.append("")
        lines.append(f"**{company}**  ")
        lines.append(f"{street}  ")
        lines.append(f"{zip_city}  ")
        lines.append(f"Deutschland  ")
        lines.append("")
        lines.append(f"**Vertreten durch die Geschäftsführung:**  ")
        lines.append(f"{person}  ")
        lines.append("")
        lines.append("## Kontakt")
        lines.append(f"Telefon: {phone}  ")
        lines.append(f"E-Mail: {email}  ")
        lines.append("")
        lines.append("## Registereintrag")
        lines.append(f"Eintragung im Handelsregister.  ")
        lines.append(f"Registergericht: {reg_court}  ")
        lines.append(f"Registernummer: {reg_number}  ")
        lines.append("")
        if vat_id:
            lines.append("## Umsatzsteuer-Identifikationsnummer")
            lines.append(f"Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz:  ")
            lines.append(f"**{vat_id}**  ")
            lines.append("")
        if has_editorial:
            lines.append("## Verantwortlich für den redaktionellen Inhalt nach § 18 Abs. 2 MStV")
            lines.append(f"{editorial_person}  ")
            lines.append(f"{street}  ")
            lines.append(f"{zip_city}  ")
            lines.append("")
        lines.append("## Verbraucherstreitbeilegung / Universalschlichtungsstelle (§ 36 VSBG)")
        lines.append(
            "Wir sind zur Teilnahme an einem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle weder "
            "verpflichtet noch bereit (§ 36 VSBG)."
        )

    elif country == "AT":
        lines.append("## Angaben gemäß § 5 E-Commerce-Gesetz (ECG) und Offenlegung nach § 25 Mediengesetz (MedienG)")
        lines.append("")
        lines.append(f"**{company}**  ")
        lines.append(f"{street}  ")
        lines.append(f"{zip_city}  ")
        lines.append(f"Österreich  ")
        lines.append("")
        lines.append(f"**Vertretungsbefugte Organe (Geschäftsführung):**  ")
        lines.append(f"{person}  ")
        lines.append("")
        lines.append("## Kontakt")
        lines.append(f"Telefon: {phone}  ")
        lines.append(f"E-Mail: {email}  ")
        lines.append("")
        lines.append("## Firmenbuchdaten")
        lines.append(f"Firmenbuchnummer: {reg_number}  ")
        lines.append(f"Firmenbuchgericht: {reg_court}  ")
        if vat_id:
            lines.append(f"UID-Nummer: {vat_id}  ")
        lines.append("")
        lines.append("## Kammerzugehörigkeit & Aufsichtsbehörde")
        lines.append(f"Mitglied der: {chamber}  ")
        lines.append(f"Zuständige Aufsichtsbehörde / Gewerbebehörde: {supervisory_authority}  ")
        lines.append(f"Anwendbare berufsrechtliche Vorschriften: Gewerbeordnung 1994 (GewO), abrufbar unter www.ris.bka.gv.at  ")
        lines.append("")
        lines.append("## Grundlegende Richtung des Mediums (Blattlinie nach § 25 MedienG)")
        lines.append(
            f"Diese Website dient der Information über das Unternehmen, dessen Produkte, Dienstleistungen "
            f"sowie branchenspezifische Fachinhalte und Neuigkeiten von {company}."
        )
        lines.append("")
        lines.append("## Verbraucherschlichtung")
        lines.append(
            "Wir sind zur Beilegung von Streitigkeiten mit Verbrauchern vor einer Verbraucherschlichtungsstelle weder "
            "verpflichtet noch bereit."
        )

    else:  # CH
        lines.append("## Angaben gemäß Art. 3 Abs. 1 lit. s UWG & revDSG")
        lines.append("")
        lines.append(f"**{company}**  ")
        lines.append(f"{street}  ")
        lines.append(f"{zip_city}  ")
        lines.append(f"Schweiz  ")
        lines.append("")
        lines.append(f"**Vertretungsberechtigte Person(en):**  ")
        lines.append(f"{person}  ")
        lines.append("")
        lines.append("## Kontakt")
        lines.append(f"Telefon: {phone}  ")
        lines.append(f"E-Mail: {email}  ")
        lines.append("")
        lines.append("## Handelsregistereintrag & Unternehmens-Identifikationsnummer (UID)")
        lines.append(f"Eingetragener Firmenname: {company}  ")
        lines.append(f"Handelsregisteramt: {reg_court}  ")
        lines.append(f"Handelsregister-Nummer: {reg_number}  ")
        if vat_id:
            lines.append(f"UID / MWST-Nummer: **{vat_id}**  ")
        lines.append("")
        if has_editorial:
            lines.append("## Redaktionelle Verantwortung")
            lines.append(f"Inhaltlich verantwortlich: {editorial_person}, {zip_city}  ")
            lines.append("")
        lines.append("## Haftungsausschluss")
        lines.append(
            "Der Autor übernimmt keinerlei Gewähr hinsichtlich der inhaltlichen Richtigkeit, Genauigkeit, "
            "Aktualität, Zuverlässigkeit und Vollständigkeit der Informationen. Haftungsansprüche gegen den Autor "
            "wegen Schäden materieller oder immaterieller Art, welche aus dem Zugriff oder der Nutzung bzw. "
            "Nichtnutzung der veröffentlichten Informationen entstehen, werden ausgeschlossen. "
            "Alle Angebote sind unverbindlich."
        )

    return "\n".join(lines)


def generate_privacy_policy(config: Dict[str, Any]) -> str:
    """
    Generiert eine 100% DSGVO- (DE/AT) bzw. revDSG-konforme (CH) Datenschutzerklärung für 2026.
    """
    country = config.get("country", "DE").upper()
    company = config.get("companyName", "Musterfirma GmbH")
    person = config.get("personName", "Max Mustermann")
    street = config.get("street", "Musterstraße 123")
    zip_city = config.get("zipCity", "8001 Zürich" if country == "CH" else ("1010 Wien" if country == "AT" else "10115 Berlin"))
    email = config.get("email", "datenschutz@musterfirma.de")
    website_url = config.get("websiteUrl", "https://example.com")

    lines = []
    lines.append("# Datenschutzerklärung")
    lines.append("")

    # 1. Verantwortlicher
    lines.append("## 1. Verantwortliche Stelle")
    lines.append("Verantwortlich für die Datenverarbeitung auf dieser Website ist:")
    lines.append("")
    lines.append(f"**{company}**  ")
    lines.append(f"{street}  ")
    lines.append(f"{zip_city}  ")
    lines.append(f"Vertreten durch: {person}  ")
    lines.append(f"E-Mail: {email}  ")
    lines.append("")

    # 2. Rechtsgrundlagen
    lines.append("## 2. Rechtsgrundlagen der Verarbeitung")
    if country == "CH":
        lines.append(
            "Wir bearbeiten Personendaten in Übereinstimmung mit dem Schweizer Datenschutzgesetz, "
            "insbesondere dem Bundesgesetz über den Datenschutz (**revDSG**) und der Datenschutzverordnung (DSV). "
            "Sofern und soweit die EU-Datenschutz-Grundverordnung (DSGVO) anwendbar ist, erfolgt die Bearbeitung "
            "ergänzend auf Grundlage von Art. 6 Abs. 1 DSGVO."
        )
    else:
        lines.append(
            "Die Verarbeitung personenbezogener Daten erfolgt im Einklang mit der Datenschutz-Grundverordnung (**DSGVO**), "
            "dem Bundesdatenschutzgesetz (BDSG, Deutschland) bzw. dem Datenschutzgesetz (DSG, Österreich) sowie "
            "dem **§ 25 Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG)** für Speicherungen und Abrufe auf dem Endgerät."
        )
    lines.append("")

    # 3. Server-Log-Dateien
    lines.append("## 3. Hosting & Server-Log-Dateien")
    lines.append(
        "Beim Aufrufen unserer Website erfasst der Webserver automatisch technische Informationen, die Ihr Browser "
        "automatisch übermittelt. Dies sind: Browsertyp und Browserversion, verwendetes Betriebssystem, Referrer URL, "
        "Hostname des zugreifenden Rechners, Uhrzeit der Serveranfrage sowie die anonymisierte IP-Adresse. "
        "Diese Daten sind nicht bestimmten Personen zuordenbar. Eine Zusammenführung dieser Daten mit anderen Datenquellen "
        "wird nicht vorgenommen. Grundlage für die Datenverarbeitung ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der "
        "technisch fehlerfreien Darstellung und Systemsicherheit) bzw. Art. 6 revDSG."
    )
    lines.append("")

    # 4. Cookies & § 25 TDDDG
    lines.append("## 4. Cookies & Endgerätezugriff nach § 25 TDDDG / revDSG")
    lines.append(
        "Unsere Website verwendet ausschließlich technisch notwendige Cookies oder greift erst nach ausdrücklicher, "
        "informierter Einwilligung auf Speicherfunktionen Ihres Endgerätes (Local Storage, Session Storage, Cookies) zu. "
        "Gemäß **§ 25 Abs. 1 TDDDG** bedarf das Speichern von Informationen in der Endeinrichtung des Endnutzers oder "
        "der Zugriff auf Informationen, die bereits in der Endeinrichtung gespeichert sind, der Einwilligung des Nutzers. "
        "Technisch zwingend erforderliche Speicherungen erfolgen gemäß **§ 25 Abs. 2 TDDDG** bzw. Art. 6 revDSG."
    )
    lines.append("")

    # 5. SSL / TLS
    lines.append("## 5. SSL- bzw. TLS-Verschlüsselung")
    lines.append(
        "Diese Seite nutzt aus Sicherheitsgründen und zum Schutz der Übertragung vertraulicher Inhalte eine "
        "SSL- bzw. TLS-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie daran, dass die Adresszeile des "
        "Browsers von 'http://' auf 'https://' wechselt und an dem Schloss-Symbol in Ihrer Browserzeile. "
        "Wenn die SSL- bzw. TLS-Verschlüsselung aktiviert ist, können Daten, die Sie an uns übermitteln, nicht von Dritten mitgelesen werden."
    )
    lines.append("")

    # 6. Auslandsbekanntgabe (besonders CH revDSG Art. 19 / 16)
    lines.append("## 6. Datenübermittlung in Drittstaaten & Cloud-Dienste")
    if country == "CH":
        lines.append(
            "Gemäß Art. 19 Abs. 2 lit. b revDSG teilen wir Ihnen mit, dass wir Personendaten primär in der Schweiz "
            "und im Europäischen Wirtschaftsraum (EWR) bearbeiten. Soweit Dienste von Drittanbietern mit Sitz in den USA "
            "oder anderen Drittstaaten eingesetzt werden, erfolgt die Bekanntgabe gestützt auf einen Angemessenheitsbeschluss "
            "(wie das Swiss-U.S. Data Privacy Framework) oder Standardvertragsklauseln (SCC) des Eidgenössischen "
            "Datenschutz- und Öffentlichkeitsbeauftragten (EDÖB)."
        )
    else:
        lines.append(
            "Soweit wir Daten in Drittländern (außerhalb der Europäischen Union bzw. des EWR) verarbeiten, erfolgt dies nur, "
            "wenn die besonderen Voraussetzungen der Art. 44 ff. DSGVO erfüllt sind (Angemessenheitsbeschluss der EU-Kommission "
            "wie das EU-U.S. Data Privacy Framework oder anerkannte Standardvertragsklauseln)."
        )
    lines.append("")

    # 7. Betroffenenrechte & Widerruf
    lines.append("## 7. Ihre Rechte (Auskunft, Berichtigung, Löschung, Widerruf & Widerspruch)")
    lines.append(
        "Sie haben jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, "
        "deren Herkunft und Empfänger und den Zweck der Datenverarbeitung sowie ein Recht auf Berichtigung, Sperrung oder Löschung dieser Daten. "
        "Hierzu sowie zu weiteren Fragen zum Thema personenbezogene Daten können Sie sich jederzeit an die im Impressum angegebene Adresse wenden."
    )
    lines.append("")
    lines.append("**Recht auf Widerruf der datenschutzrechtlichen Einwilligung:**  ")
    lines.append(
        "Viele Datenverarbeitungsvorgänge sind nur mit Ihrer ausdrücklichen Einwilligung möglich. Sie können eine bereits "
        "erteilte Einwilligung jederzeit formlos per E-Mail an uns widerrufen. Die Rechtmäßigkeit der bis zum Widerruf "
        "erfolgten Datenverarbeitung bleibt vom Widerruf unberührt."
    )
    lines.append("")
    lines.append("**Widerspruchsrecht gegen die Datenerhebung in besonderen Fällen (Art. 21 DSGVO):**  ")
    lines.append(
        "WENN DIE DATENVERARBEITUNG AUF GRUNDLAGE VON ART. 6 ABS. 1 LIT. E ODER F DSGVO ERFOLGT, HABEN SIE JEDERZEIT DAS RECHT, "
        "AUS GRÜNDEN, DIE SICH AUS IHRER BESONDEREN SITUATION ERGEBEN, GEGEN DIE VERARBEITUNG IHRER PERSONENBEZOGENEN DATEN WIDERSPRUCH EINZULEGEN."
    )
    lines.append("")

    # 8. Aufsichtsbehörde
    lines.append("## 8. Beschwerderecht bei der zuständigen Aufsichtsbehörde")
    if country == "CH":
        lines.append(
            "Zuständige Datenschutz-Aufsichtsbehörde in der Schweiz ist der Eidgenössische Datenschutz- und "
            "Öffentlichkeitsbeauftragte (**EDÖB**), Feldeggweg 1, CH-3003 Bern (https://www.edoeb.admin.ch)."
        )
    elif country == "AT":
        lines.append(
            "Zuständige Aufsichtsbehörde in Österreich ist die **Österreichische Datenschutzbehörde (DSB)**, "
            "Barichgasse 40-42, 1030 Wien (https://www.dsb.gv.at)."
        )
    else:
        lines.append(
            "Im Falle datenschutzrechtlicher Verstöße steht dem Betroffenen ein Beschwerderecht bei einer zuständigen "
            "Datenschutzaufsichtsbehörde zu (in der Regel der Landesbeauftragte für den Datenschutz des Bundeslandes unseres Unternehmenssitzes "
            "oder der Bundesbeauftragte für den Datenschutz und die Informationsfreiheit – **BfDI**)."
        )

    return "\n".join(lines)


def run_self_test() -> bool:
    """
    Führt umfassende Selbsttests für den Compliance-Scanner und die Generatoren durch.
    Gibt True zurück, wenn alle Tests erfolgreich bestanden wurden.
    """
    print("=" * 70)
    print("🧪 DACH IMPRESSUM & DSGVO COMPLIANCE CHECKER – SELBSTTEST-SUITE 2026")
    print("=" * 70)
    passed_all = True

    # Test 1: Erkennung von veraltetem § 5 TMG
    sample_bad_tmg = "Angaben gemäß § 5 TMG. Musterfirma GmbH, Berlin."
    res1 = scan_compliance(sample_bad_tmg, country="DE")
    found_tmg = any(f["id"] == "OUTDATED_TMG" for f in res1["findings"])
    assert found_tmg, "FEHLER: OUTDATED_TMG nicht erkannt!"
    assert res1["score"] < 80, f"FEHLER: Score {res1['score']} zu hoch für TMG-Verstoß!"
    print(f"  [PASS] Test 1: Veraltetes § 5 TMG erkannt (Score: {res1['score']}/100, Befund: {res1['findings'][0]['id']})")

    # Test 2: Erkennung von veraltetem TTDSG
    sample_bad_ttdsg = "Unsere Cookies richten sich nach dem TTDSG. Speicherung auf dem Endgerät."
    res2 = scan_compliance(sample_bad_ttdsg, country="DE")
    found_ttdsg = any(f["id"] == "OUTDATED_TTDSG" for f in res2["findings"])
    assert found_ttdsg, "FEHLER: OUTDATED_TTDSG nicht erkannt!"
    print(f"  [PASS] Test 2: Veraltetes TTDSG erkannt (Score: {res2['score']}/100, Befund: {res2['findings'][0]['id']})")

    # Test 3: Erkennung von RStV statt MStV
    sample_bad_rstv = "Verantwortlich nach § 55 Abs. 2 RStV: Max Mustermann, Berlin."
    res3 = scan_compliance(sample_bad_rstv, country="DE")
    found_rstv = any(f["id"] == "OUTDATED_RSTV" for f in res3["findings"])
    assert found_rstv, "FEHLER: OUTDATED_RSTV nicht erkannt!"
    print(f"  [PASS] Test 3: Veralteter § 55 Abs. 2 RStV erkannt (Score: {res3['score']}/100)")

    # Test 4: Erkennung von fehlendem revDSG bei Schweizer Datenschutz
    sample_ch_missing = "Datenschutzerklärung für unsere Kunden in der Schweiz und weltweit."
    res4 = scan_compliance(sample_ch_missing, country="CH")
    found_revdsg = any(f["id"] == "MISSING_CH_REVDSG" for f in res4["findings"])
    assert found_revdsg, "FEHLER: MISSING_CH_REVDSG nicht erkannt!"
    print(f"  [PASS] Test 4: Fehlendes Schweizer revDSG erkannt (Score: {res4['score']}/100)")

    # Test 5: Erkennung von fehlendem ECG & Blattlinie bei Österreich
    sample_at_missing = "Impressum: Musterfirma GmbH, Wien. Telefon +43 1 234."
    res5 = scan_compliance(sample_at_missing, country="AT")
    found_ecg = any(f["id"] == "MISSING_AT_ECG" for f in res5["findings"])
    found_blattlinie = any(f["id"] == "MISSING_AT_BLATTLINIE" for f in res5["findings"])
    assert found_ecg and found_blattlinie, "FEHLER: Österreichische Pflichtangaben nicht erkannt!"
    print(f"  [PASS] Test 5: Fehlendes § 5 ECG & § 25 MedienG Blattlinie erkannt (Score: {res5['score']}/100)")

    # Test 6: Erkennung von externem Google Fonts Risiko
    sample_fonts = "Wir binden Schriftarten über fonts.googleapis.com und fonts.gstatic.com ein."
    res6 = scan_compliance(sample_fonts, country="ALL")
    found_fonts = any(f["id"] == "REMOTE_GOOGLE_FONTS_RISK" for f in res6["findings"])
    assert found_fonts, "FEHLER: REMOTE_GOOGLE_FONTS_RISK nicht erkannt!"
    print(f"  [PASS] Test 6: Google Fonts Remote-Risiko erkannt (Score: {res6['score']}/100)")

    # Test 7: Generator-Test für Deutschland (DE)
    gen_de_imp = generate_impressum({"country": "DE", "companyName": "TechCorp DE GmbH", "personName": "Erika Muster"})
    gen_de_dpo = generate_privacy_policy({"country": "DE", "companyName": "TechCorp DE GmbH"})
    assert "§ 5 Digitale-Dienste-Gesetz (DDG)" in gen_de_imp, "FEHLER: DDG fehlt im DE-Impressum!"
    assert "§ 18 Abs. 2 MStV" in gen_de_imp, "FEHLER: § 18 Abs. 2 MStV fehlt im DE-Impressum!"
    assert "§ 25 Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG)" in gen_de_dpo, "FEHLER: TDDDG fehlt in DE-Datenschutzerklärung!"
    assert "TMG" not in gen_de_imp, "FEHLER: Altes TMG im neuen Impressum gefunden!"
    assert "TTDSG" not in gen_de_dpo, "FEHLER: Altes TTDSG in neuer Datenschutzerklärung gefunden!"
    res_gen_de = scan_compliance(gen_de_imp + "\n\n" + gen_de_dpo, country="DE")
    assert res_gen_de["score"] == 100, f"FEHLER: Generierter DE-Text hat Score {res_gen_de['score']} statt 100! Findings: {res_gen_de['findings']}"
    print(f"  [PASS] Test 7: Generator DE erzeugt 100 % konformes Impressum & Datenschutz (Score: {res_gen_de['score']}/100)")

    # Test 8: Generator-Test für Österreich (AT)
    gen_at_imp = generate_impressum({"country": "AT", "companyName": "AlpenTech AT GmbH", "personName": "Johann Gruber"})
    gen_at_dpo = generate_privacy_policy({"country": "AT", "companyName": "AlpenTech AT GmbH"})
    assert "§ 5 E-Commerce-Gesetz (ECG)" in gen_at_imp, "FEHLER: ECG fehlt im AT-Impressum!"
    assert "Blattlinie nach § 25 MedienG" in gen_at_imp, "FEHLER: Blattlinie fehlt im AT-Impressum!"
    assert "Datenschutzbehörde (DSB)" in gen_at_dpo, "FEHLER: DSB fehlt in AT-Datenschutzerklärung!"
    res_gen_at = scan_compliance(gen_at_imp + "\n\n" + gen_at_dpo, country="AT")
    assert res_gen_at["score"] == 100, f"FEHLER: Generierter AT-Text hat Score {res_gen_at['score']} statt 100! Findings: {res_gen_at['findings']}"
    print(f"  [PASS] Test 8: Generator AT erzeugt 100 % konformes Impressum & Datenschutz (Score: {res_gen_at['score']}/100)")

    # Test 9: Generator-Test für Schweiz (CH)
    gen_ch_imp = generate_impressum({"country": "CH", "companyName": "Helvetia Digital AG", "personName": "Beat Meier", "vatId": "CHE-123.456.789 MWST"})
    gen_ch_dpo = generate_privacy_policy({"country": "CH", "companyName": "Helvetia Digital AG"})
    assert "Art. 3 Abs. 1 lit. s UWG" in gen_ch_imp, "FEHLER: UWG fehlt im CH-Impressum!"
    assert "CHE-123.456.789" in gen_ch_imp, "FEHLER: UID fehlt im CH-Impressum!"
    assert "revDSG" in gen_ch_dpo, "FEHLER: revDSG fehlt in CH-Datenschutzerklärung!"
    assert "EDÖB" in gen_ch_dpo, "FEHLER: EDÖB fehlt in CH-Datenschutzerklärung!"
    res_gen_ch = scan_compliance(gen_ch_imp + "\n\n" + gen_ch_dpo, country="CH")
    assert res_gen_ch["score"] == 100, f"FEHLER: Generierter CH-Text hat Score {res_gen_ch['score']} statt 100! Findings: {res_gen_ch['findings']}"
    print(f"  [PASS] Test 9: Generator CH erzeugt 100 % konformes Impressum & Datenschutz (Score: {res_gen_ch['score']}/100)")

    print("-" * 70)
    print("✅ ALLE 9 SELBSTTESTS ERFOLGREICH BESTANDEN!")
    print("=" * 70)
    return True


def fetch_url_content(url: str) -> str:
    """Holt HTML oder Text einer Website mit Standard-Header und Timeout."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "DACH-Compliance-Scanner/1.0 (+https://dach-digitalwerk.netlify.app/)"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        html = content.decode(charset, errors="ignore")
        # Entferne HTML Tags für Textanalyse
        text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text


def main():
    parser = argparse.ArgumentParser(description="DACH Impressum & DSGVO Compliance Checker 2026 CLI")
    parser.add_argument("--test", action="store_true", help="Führt die interne Selbsttest-Suite aus")
    parser.add_argument("--country", choices=["DE", "AT", "CH", "ALL"], default="ALL", help="Zielland für spezifische Rechtsnormen")
    parser.add_argument("--file", type=str, help="Pfad zu einer lokalen Text- oder HTML-Datei")
    parser.add_argument("--url", type=str, help="URL einer Website zum Live-Scannen")
    parser.add_argument("--text", type=str, help="Rohtext zur Compliance-Prüfung")
    parser.add_argument("--generate-impressum", action="store_true", help="Generiert ein rechtssicheres Impressum 2026")
    parser.add_argument("--generate-privacy", action="store_true", help="Generiert eine rechtssichere Datenschutzerklärung 2026")
    parser.add_argument("--company", type=str, default="Musterfirma GmbH", help="Firmenname für Generator")
    parser.add_argument("--person", type=str, default="Max Mustermann", help="Name Vertretungsberechtigter")
    parser.add_argument("--street", type=str, default="Musterstraße 123", help="Straße und Hausnummer")
    parser.add_argument("--zip-city", type=str, help="PLZ und Ort")
    parser.add_argument("--email", type=str, default="kontakt@musterfirma.de", help="Kontakt-E-Mail")
    parser.add_argument("--phone", type=str, default="+49 30 1234567", help="Telefonnummer")
    parser.add_argument("--vat-id", type=str, help="USt-IdNr / UID")
    parser.add_argument("--json", action="store_true", help="Ausgabe im JSON-Format")

    args = parser.parse_args()

    if args.test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    # Generator-Modus
    if args.generate_impressum or args.generate_privacy:
        cfg = {
            "country": args.country if args.country != "ALL" else "DE",
            "companyName": args.company,
            "personName": args.person,
            "street": args.street,
            "zipCity": args.zip_city or ("8001 Zürich" if args.country == "CH" else ("1010 Wien" if args.country == "AT" else "10115 Berlin")),
            "email": args.email,
            "phone": args.phone,
            "vatId": args.vat_id,
        }
        output = []
        if args.generate_impressum:
            output.append(generate_impressum(cfg))
        if args.generate_privacy:
            output.append(generate_privacy_policy(cfg))

        combined = "\n\n---\n\n".join(output)
        if args.json:
            print(json.dumps({"generatedContent": combined, "config": cfg}, indent=2, ensure_ascii=False))
        else:
            print(combined)
        return

    # Scanner-Modus
    text_to_scan = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            text_to_scan = f.read()
    elif args.url:
        print(f"Lade Inhalt von {args.url} ...", file=sys.stderr)
        text_to_scan = fetch_url_content(args.url)
    elif args.text:
        text_to_scan = args.text
    else:
        print("Kein Eingabetext angegeben. Bitte nutzen Sie --text, --file, --url, --test oder --generate-impressum.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    result = scan_compliance(text_to_scan, country=args.country)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("=" * 70)
    print(f" ⚖️ DACH COMPLIANCE SCANNER 2026 – ERGEBNIS ({args.country})")
    print("=" * 70)
    print(f"Compliance Score : {result['score']} / 100")
    print(f"Status           : {'✅ RECHTSKONFORM' if result['isCompliant'] else '⚠️ ABMAHNRISIKO / ANPASSUNG ERFORDERLICH'}")
    print(f"Gefundene Risiken: {result['totalFindings']} (Kritisch: {result['summary']['critical']}, Hoch: {result['summary']['high']}, Mittel: {result['summary']['medium']}, Gering: {result['summary']['low']})")
    print("-" * 70)

    if not result["findings"]:
        print("Keine veralteten Gesetzesverweise oder kritischen Abmahnrisiken gefunden.")
    else:
        for idx, f in enumerate(result["findings"], 1):
            badge = f"[{f['severity']}]"
            print(f"{idx}. {badge} {f['title']}")
            print(f"   Norm        : {f['legalBasis']}")
            print(f"   Problem     : {f['description']}")
            print(f"   Empfehlung  : {f['recommendation']}")
            if f.get("snippet"):
                print(f"   Fundstelle  : \"{f['snippet']}\"")
            print()

    print("-" * 70)
    print(f"🌐 Interaktiver Live-Generator: {result['liveGeneratorUrl']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
