/**
 * DACH Impressum & DSGVO/revDSG Compliance Checker 2026
 * Zero-Dependency Node.js & Browser ES Modul.
 * Erkennt Abmahnfallen nach aktuellem Recht in Deutschland, Österreich und der Schweiz:
 * - DDG (ehemals § 5 TMG)
 * - § 25 TDDDG (ehemals TTDSG)
 * - § 18 Abs. 2 MStV (ehemals § 55 Abs. 2 RStV)
 * - Schweizer revDSG (Art. 19, Art. 16/17) & Art. 3 Abs. 1 lit. s UWG
 * - Österreichisches ECG (§ 5) & MedienG (§ 25 Blattlinie/Offenlegung)
 *
 * Live Web-App: https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/
 * Copyright (c) 2026 DACH Digitalwerk (MIT License)
 */

(function (root, factory) {
  if (typeof module === 'object' && typeof module.exports === 'object') {
    module.exports = factory();
  } else if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else {
    root.DachComplianceChecker = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const SEVERITY = {
    CRITICAL: 'CRITICAL',
    HIGH: 'HIGH',
    MEDIUM: 'MEDIUM',
    LOW: 'LOW'
  };

  /**
   * Scannt Text auf rechtliche Risiken 2026 im DACH-Raum
   * @param {string} text - Rohtext oder HTML-Inhalt
   * @param {object|string} [options] - Optionen oder Ländercode (DE, AT, CH, ALL)
   * @returns {object} Scan-Ergebnis mit Score, Findings und Empfehlungen
   */
  function scanCompliance(text, options) {
    if (!text || typeof text !== 'string') {
      text = '';
    }
    const country = (typeof options === 'string' ? options : (options && options.country) || 'ALL').toUpperCase();
    const findings = [];

    // 1. Veraltetes TMG -> DDG
    const tmgMatch = text.match(/(?:§\s*5\s+)?TMG|Telemediengesetz/i);
    if (tmgMatch) {
      findings.push({
        id: 'OUTDATED_TMG',
        title: 'Veralteter Verweis auf § 5 TMG statt § 5 DDG',
        severity: SEVERITY.CRITICAL,
        category: 'DE',
        legalBasis: 'Digitale-Dienste-Gesetz (DDG) vom 14. Mai 2024 / Rechtsstand 2026',
        description: 'Das Telemediengesetz (TMG) wurde durch das Digitale-Dienste-Gesetz (DDG) abgelöst. Die Impressumspflicht für digitale Dienste folgt aus § 5 DDG.',
        recommendation: "Ersetzen Sie sämtliche Verweise auf '§ 5 TMG' durch '§ 5 DDG' oder 'Angaben gemäß § 5 DDG'.",
        snippet: tmgMatch[0]
      });
    }

    // 2. Veraltetes TTDSG -> TDDDG
    const ttdsgMatch = text.match(/TTDSG|Telekommunikation-Telemedien-Datenschutz-Gesetz/i);
    if (ttdsgMatch) {
      findings.push({
        id: 'OUTDATED_TTDSG',
        title: 'Veralteter Verweis auf TTDSG statt § 25 TDDDG',
        severity: SEVERITY.CRITICAL,
        category: 'DE',
        legalBasis: 'Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG)',
        description: 'Das TTDSG wurde zum TDDDG umbenannt. Rechtsgrundlage für Cookies und Geräteabfragen ist zwingend § 25 TDDDG.',
        recommendation: "Ersetzen Sie 'TTDSG' bzw. '§ 25 TTDSG' durch '§ 25 TDDDG'.",
        snippet: ttdsgMatch[0]
      });
    }

    // 3. Veralteter Rundfunkstaatsvertrag (RStV -> MStV)
    const rstvMatch = text.match(/(?:§\s*55\s+Abs\.?\s*2\s+)?RStV|Rundfunkstaatsvertrag/i);
    if (rstvMatch) {
      findings.push({
        id: 'OUTDATED_RSTV',
        title: 'Veralteter Verweis auf § 55 Abs. 2 RStV statt § 18 Abs. 2 MStV',
        severity: SEVERITY.HIGH,
        category: 'DE',
        legalBasis: 'Medienstaatsvertrag (MStV) § 18 Abs. 2',
        description: 'Der Rundfunkstaatsvertrag ist außer Kraft. Redaktionell Verantwortliche sind nach § 18 Abs. 2 MStV zu benennen.',
        recommendation: "Aktualisieren Sie auf: 'Verantwortlich für den redaktionellen Inhalt nach § 18 Abs. 2 MStV'.",
        snippet: rstvMatch[0]
      });
    }

    // 4. MStV bei redaktionellen Inhalten
    const editorialSignals = /blog|magazin|news|artikel|beitrag|podcast|kommentar|redaktion/i;
    const hasEditorialHint = editorialSignals.test(text);
    const hasMstv = /(?:§\s*18\s+Abs\.?\s*2\s+MStV|Medienstaatsvertrag)/i.test(text);
    if ((country === 'DE' || country === 'ALL') && hasEditorialHint && !hasMstv && !rstvMatch) {
      findings.push({
        id: 'MISSING_MSTV',
        title: 'Möglicherweise fehlende Angabe nach § 18 Abs. 2 MStV für redaktionelle Inhalte',
        severity: SEVERITY.MEDIUM,
        category: 'DE',
        legalBasis: '§ 18 Abs. 2 MStV (Deutschland)',
        description: 'Bei Vorhandensein von redaktionellen Inhalten (Blog, News, Fachartikel) muss ein Verantwortlicher mit voller Anschrift benannt werden.',
        recommendation: "Fügen Sie hinzu: 'Verantwortlich für den redaktionellen Inhalt nach § 18 Abs. 2 MStV: Vorname Nachname, Wohnanschrift'.",
        snippet: 'Redaktionelle Signalwörter erkannt, kein § 18 Abs. 2 MStV gefunden'
      });
    }

    // 5. Veraltetes ODR-Link / VSBG
    const odrMatch = text.match(/ec\.europa\.eu\/consumers\/odr/i);
    const hasVsbg = /(?:§\s*36\s+VSBG|Verbraucherstreitbeilegung|Universalschlichtungsstelle|Verbraucherschlichtung)/i.test(text);
    if (odrMatch) {
      const hasSunsetNotice = /(?:eingestellt|stillgelegt|außer betrieb|abgeschaltet|historisch|einstellung)/i.test(text);
      if (!hasSunsetNotice) {
        findings.push({
          id: 'OBSOLETE_ODR_LINK',
          title: 'Abmahngefahr: Veralteter Link auf die stillgelegte EU-OS-Plattform',
          severity: SEVERITY.MEDIUM,
          category: 'DE/AT',
          legalBasis: 'EU-Verordnung über die Einstellung der europäischen OS-Plattform & § 36 VSBG',
          description: 'Die Europäische Kommission hat die bisherige interaktive OS-Plattform stillgelegt. Die bisherige Verlinkungspflicht ist entfallen; tote Links stellen ein Abmahnrisiko dar.',
          recommendation: "Entfernen Sie den toten OS-Link und belassen Sie die standardmäßige Erklärung nach § 36 VSBG.",
          snippet: odrMatch[0]
        });
      }
    } else if ((country === 'DE' || country === 'ALL') && !hasVsbg && (/impressum/i.test(text) || /anbieterkennzeichnung/i.test(text))) {
      findings.push({
        id: 'MISSING_VSBG',
        title: 'Fehlender Hinweis zur Verbraucherstreitbeilegung nach § 36 VSBG',
        severity: SEVERITY.LOW,
        category: 'DE',
        legalBasis: '§ 36 Verbraucherstreitbeilegungsgesetz (VSBG)',
        description: 'Unternehmen müssen im Impressum klar darüber informieren, ob sie an einem Streitbeilegungsverfahren teilnehmen.',
        recommendation: 'Fügen Sie eine klare Erklärung nach § 36 VSBG hinzu.',
        snippet: 'Keine VSBG-Erklärung im Impressum gefunden'
      });
    }

    // 6. Schweiz (CH) – revDSG & UWG
    if (country === 'CH' || country === 'ALL') {
      const hasChSignals = /\b(?:schweiz|switzerland|ch|gmbh|ag|chf|eidgenössisch|edöb|uid|che-)\b/i.test(text);
      const hasRevdsg = /\b(?:revDSG|Datenschutzgesetz|DSG|EDÖB)\b/i.test(text);
      const hasChAbroadTransfer = /(?:ausland|drittstaat|bekanntgabe ins ausland|art\.?\s*16|art\.?\s*17|standardvertragsklauseln|swiss-us)/i.test(text);
      const hasChUid = /CHE-\d{3}\.\d{3}\.\d{3}/i.test(text);

      const isPrivacyText = /(?:datenschutz|privacy|personendaten|bearbeitung)/i.test(text);
      if (isPrivacyText && !hasRevdsg && (country === 'CH' || (hasChSignals && /schweiz/i.test(text)))) {
        findings.push({
          id: 'MISSING_CH_REVDSG',
          title: 'Fehlende Übereinstimmung mit dem neuen Schweizer Datenschutzgesetz (revDSG)',
          severity: SEVERITY.HIGH,
          category: 'CH',
          legalBasis: 'Bundesgesetz über den Datenschutz (revDSG, Art. 19)',
          description: 'Für Websites mit Schweizer Nutzern oder Anbietern gilt das revDSG. Erforderlich sind Angaben über Bearbeitungszwecke und Empfängerstaaten (Art. 16/19 revDSG).',
          recommendation: 'Ergänzen Sie die Datenschutzerklärung um Bezüge zum Schweizer revDSG und den EDÖB.',
          snippet: 'Kein revDSG-Bezug in Datenschutzerklärung vorhanden'
        });
      }

      if (isPrivacyText && hasRevdsg && !hasChAbroadTransfer) {
        findings.push({
          id: 'MISSING_CH_TRANSFER_NOTICE',
          title: 'Fehlende Angabe zur Datenbekanntgabe ins Ausland nach Art. 19 Abs. 2 lit. b revDSG',
          severity: SEVERITY.MEDIUM,
          category: 'CH',
          legalBasis: 'Art. 19 Abs. 2 lit. b i.V.m. Art. 16/17 revDSG',
          description: 'Das revDSG schreibt vor, Staaten zu benennen, in die Daten übermittelt werden (z. B. USA bei Cloud-/Mail-Diensten).',
          recommendation: 'Benennen Sie die Staaten und Garantien (z. B. Swiss-US DPF / Standardvertragsklauseln).',
          snippet: 'Hinweis auf Staaten der Datenübermittlung fehlt'
        });
      }

      const isImpressumText = /(?:impressum|kontakt|über uns)/i.test(text);
      if (isImpressumText && (country === 'CH' || (hasChSignals && /schweiz/i.test(text)))) {
        if (!hasChUid && !/UID|Unternehmens-Identifikationsnummer/i.test(text)) {
          findings.push({
            id: 'MISSING_CH_UID',
            title: 'Fehlende Schweizer UID (CHE-Nummer)',
            severity: SEVERITY.LOW,
            category: 'CH',
            legalBasis: 'Art. 3 Abs. 1 lit. s UWG & UIDG',
            description: 'Im Schweizer Handelsregister eingetragene Unternehmen müssen im elektronischen Rechtsverkehr ihre UID (CHE-xxx.xxx.xxx) angeben.',
            recommendation: "Geben Sie die UID-Nummer an: 'UID: CHE-xxx.xxx.xxx MWST/HR'.",
            snippet: 'Keine CHE-Nummer gefunden'
          });
        }
      }
    }

    // 7. Österreich (AT) – ECG & MedienG
    if (country === 'AT' || country === 'ALL') {
      const hasAtSignals = /\b(?:österreich|austria|wien|graz|linz|salzburg|innsbruck|atu|wko|firmenbuch|firmenbuchgericht)\b/i.test(text);
      const hasEcg = /(?:§\s*5\s+ECG|E-Commerce-Gesetz)/i.test(text);
      const hasBlattlinie = /(?:Blattlinie|grundlegende Richtung)/i.test(text);

      const isImpressumText = /(?:impressum|kontakt|offenlegung)/i.test(text);
      if (isImpressumText && (country === 'AT' || (hasAtSignals && /österreich/i.test(text)))) {
        if (!hasEcg) {
          findings.push({
            id: 'MISSING_AT_ECG',
            title: 'Fehlende Ausweisung der Informationspflichten nach § 5 ECG (Österreich)',
            severity: SEVERITY.HIGH,
            category: 'AT',
            legalBasis: '§ 5 E-Commerce-Gesetz (ECG) Österreich',
            description: 'In Österreich regelt § 5 ECG die Impressumspflichten (Firmenbuchnummer, Gericht, Kammerzugehörigkeit, UID).',
            recommendation: "Verweisen Sie im Impressum auf 'Angaben gemäß § 5 E-Commerce-Gesetz (ECG)'.",
            snippet: 'Kein Hinweis auf § 5 ECG gefunden'
          });
        }

        if (!hasBlattlinie) {
          findings.push({
            id: 'MISSING_AT_BLATTLINIE',
            title: 'Fehlende Offenlegung / Blattlinie nach § 25 Mediengesetz (MedienG AT)',
            severity: SEVERITY.HIGH,
            category: 'AT',
            legalBasis: '§ 25 MedienG (Österreich)',
            description: 'Nach § 25 MedienG muss bei Webangeboten mit journalistischen/fachlichen Inhalten die Blattlinie (grundlegende Richtung des Mediums) angegeben werden.',
            recommendation: "Fügen Sie eine Blattlinie ein: 'Grundlegende Richtung des Mediums (Blattlinie): ...'.",
            snippet: 'Keine Blattlinie / § 25 MedienG Offenlegung gefunden'
          });
        }
      }
    }

    // 8. Externe Google Fonts ohne Consent
    const googleFontsMatch = text.match(/fonts\.googleapis\.com|fonts\.gstatic\.com/i);
    if (googleFontsMatch) {
      findings.push({
        id: 'REMOTE_GOOGLE_FONTS_RISK',
        title: 'Verdacht auf dynamisches Nachladen von Google Fonts (LG München I Risiko)',
        severity: SEVERITY.HIGH,
        category: 'ALL',
        legalBasis: 'Art. 6 Abs. 1 DSGVO / LG München I (Az. 3 O 17493/20)',
        description: 'Das dynamische Laden von Google Fonts ohne vorherigen Consent überträgt IP-Adressen an US-Server und ist abmahnfähig.',
        recommendation: 'Hosten Sie alle Webfonts (WOFF2) lokal auf dem eigenen Server.',
        snippet: googleFontsMatch[0]
      });
    }

    // 9. Widerrufsrechte in Datenschutzerklärung
    const isPrivacyText = /(?:datenschutz|privacy|verarbeitung von personendaten)/i.test(text);
    const hasWiderruf = /(?:widerruf|widerspruch|art\.?\s*21\s+dsgvo)/i.test(text);
    if (isPrivacyText && !hasWiderruf) {
      findings.push({
        id: 'MISSING_RIGHT_TO_REVOKE',
        title: 'Fehlender Hinweis auf das Widerspruchs- und Widerrufsrecht',
        severity: SEVERITY.HIGH,
        category: 'ALL',
        legalBasis: 'Art. 7 Abs. 3, Art. 21 DSGVO & Art. 25 ff. revDSG',
        description: 'Betroffene Personen müssen über das jederzeitige Recht zum Widerruf einer Einwilligung und das Widerspruchsrecht belehrt werden.',
        recommendation: 'Ergänzen Sie einen Abschnitt über das Widerrufs- und Widerspruchsrecht.',
        snippet: 'Keine Widerrufs-/Widerspruchsklausel in Datenschutzerklärung gefunden'
      });
    }

    // 10. SSL/TLS Hinweis
    const hasSsl = /(?:ssl|tls|verschlüsselung|https)/i.test(text);
    if (isPrivacyText && !hasSsl) {
      findings.push({
        id: 'MISSING_SSL_NOTE',
        title: 'Fehlender Hinweis auf SSL-/TLS-Verschlüsselung',
        severity: SEVERITY.LOW,
        category: 'ALL',
        legalBasis: 'Art. 32 DSGVO / Art. 8 revDSG',
        description: 'Zur Datensicherheit ist der Einsatz einer Transportverschlüsselung in der Erklärung zu erwähnen.',
        recommendation: 'Fügen Sie den Standard-Absatz zur SSL/TLS-Verschlüsselung hinzu.',
        snippet: 'Keine Erwähnung von SSL/TLS-Verschlüsselung gefunden'
      });
    }

    // Score-Berechnung
    let score = 100;
    findings.forEach(f => {
      if (f.severity === SEVERITY.CRITICAL) score -= 35;
      else if (f.severity === SEVERITY.HIGH) score -= 20;
      else if (f.severity === SEVERITY.MEDIUM) score -= 10;
      else if (f.severity === SEVERITY.LOW) score -= 5;
    });
    score = Math.max(0, Math.min(100, score));

    const summary = {
      critical: findings.filter(f => f.severity === SEVERITY.CRITICAL).length,
      high: findings.filter(f => f.severity === SEVERITY.HIGH).length,
      medium: findings.filter(f => f.severity === SEVERITY.MEDIUM).length,
      low: findings.filter(f => f.severity === SEVERITY.LOW).length
    };

    return {
      score: score,
      isCompliant: score >= 85 && summary.critical === 0 && summary.high === 0,
      countryFilter: country,
      totalFindings: findings.length,
      summary: summary,
      findings: findings,
      liveGeneratorUrl: 'https://dach-digitalwerk.netlify.app/impressum-datenschutz-generator/'
    };
  }

  /**
   * Generiert ein rechtssicheres Impressum für 2026
   */
  function generateImpressum(config) {
    config = config || {};
    const country = (config.country || 'DE').toUpperCase();
    const company = config.companyName || 'Musterfirma GmbH';
    const person = config.personName || 'Max Mustermann';
    const street = config.street || 'Musterstraße 123';
    const zipCity = config.zipCity || (country === 'CH' ? '8001 Zürich' : (country === 'AT' ? '1010 Wien' : '10115 Berlin'));
    const email = config.email || (country === 'CH' ? 'kontakt@musterfirma.ch' : 'kontakt@musterfirma.de');
    const phone = config.phone || (country === 'CH' ? '+41 44 123 45 67' : '+49 30 1234567');
    const vatId = config.vatId || (country === 'CH' ? 'CHE-123.456.789 MWST' : (country === 'AT' ? 'ATU12345678' : 'DE123456789'));
    const regCourt = config.registerCourt || (country === 'CH' ? 'Handelsregisteramt Zürich' : (country === 'AT' ? 'Handelsgericht Wien' : 'Amtsgericht Charlottenburg'));
    const regNumber = config.registerNumber || (country === 'CH' ? 'CH-020.1.234.567-8' : (country === 'AT' ? 'FN 123456 a' : 'HRB 123456 B'));
    const editorialPerson = config.editorialResponsible || person;
    const hasEditorial = config.hasEditorialContent !== false;
    const chamber = config.chamber || (country === 'AT' ? 'Wirtschaftskammer Österreich (WKO)' : 'IHK Berlin');
    const supervisoryAuthority = config.supervisoryAuthority || (country === 'AT' ? 'Magistratisches Bezirksamt' : 'Gewerbeamt Berlin');

    const lines = [];
    lines.push('# Impressum');
    lines.push('');

    if (country === 'DE') {
      lines.push('## Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)');
      lines.push('');
      lines.push(`**${company}**  `);
      lines.push(`${street}  `);
      lines.push(`${zipCity}  `);
      lines.push('Deutschland  ');
      lines.push('');
      lines.push('**Vertreten durch die Geschäftsführung:**  ');
      lines.push(`${person}  `);
      lines.push('');
      lines.push('## Kontakt');
      lines.push(`Telefon: ${phone}  `);
      lines.push(`E-Mail: ${email}  `);
      lines.push('');
      lines.push('## Registereintrag');
      lines.push('Eintragung im Handelsregister.  ');
      lines.push(`Registergericht: ${regCourt}  `);
      lines.push(`Registernummer: ${regNumber}  `);
      lines.push('');
      if (vatId) {
        lines.push('## Umsatzsteuer-Identifikationsnummer');
        lines.push('Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz:  ');
        lines.push(`**${vatId}**  `);
        lines.push('');
      }
      if (hasEditorial) {
        lines.push('## Verantwortlich für den redaktionellen Inhalt nach § 18 Abs. 2 MStV');
        lines.push(`${editorialPerson}  `);
        lines.push(`${street}  `);
        lines.push(`${zipCity}  `);
        lines.push('');
      }
      lines.push('## Verbraucherstreitbeilegung / Universalschlichtungsstelle (§ 36 VSBG)');
      lines.push('Wir sind zur Teilnahme an einem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle weder verpflichtet noch bereit (§ 36 VSBG).');

    } else if (country === 'AT') {
      lines.push('## Angaben gemäß § 5 E-Commerce-Gesetz (ECG) und Offenlegung nach § 25 Mediengesetz (MedienG)');
      lines.push('');
      lines.push(`**${company}**  `);
      lines.push(`${street}  `);
      lines.push(`${zipCity}  `);
      lines.push('Österreich  ');
      lines.push('');
      lines.push('**Vertretungsbefugte Organe (Geschäftsführung):**  ');
      lines.push(`${person}  `);
      lines.push('');
      lines.push('## Kontakt');
      lines.push(`Telefon: ${phone}  `);
      lines.push(`E-Mail: ${email}  `);
      lines.push('');
      lines.push('## Firmenbuchdaten');
      lines.push(`Firmenbuchnummer: ${regNumber}  `);
      lines.push(`Firmenbuchgericht: ${regCourt}  `);
      if (vatId) {
        lines.push(`UID-Nummer: ${vatId}  `);
      }
      lines.push('');
      lines.push('## Kammerzugehörigkeit & Aufsichtsbehörde');
      lines.push(`Mitglied der: ${chamber}  `);
      lines.push(`Zuständige Aufsichtsbehörde / Gewerbebehörde: ${supervisoryAuthority}  `);
      lines.push('Anwendbare berufsrechtliche Vorschriften: Gewerbeordnung 1994 (GewO), abrufbar unter www.ris.bka.gv.at  ');
      lines.push('');
      lines.push('## Grundlegende Richtung des Mediums (Blattlinie nach § 25 MedienG)');
      lines.push(`Diese Website dient der Information über das Unternehmen, dessen Produkte, Dienstleistungen sowie branchenspezifische Fachinhalte und Neuigkeiten von ${company}.`);
      lines.push('');
      lines.push('## Verbraucherschlichtung');
      lines.push('Wir sind zur Beilegung von Streitigkeiten mit Verbrauchern vor einer Verbraucherschlichtungsstelle weder verpflichtet noch bereit.');

    } else { // CH
      lines.push('## Angaben gemäß Art. 3 Abs. 1 lit. s UWG & revDSG');
      lines.push('');
      lines.push(`**${company}**  `);
      lines.push(`${street}  `);
      lines.push(`${zipCity}  `);
      lines.push('Schweiz  ');
      lines.push('');
      lines.push('**Vertretungsberechtigte Person(en):**  ');
      lines.push(`${person}  `);
      lines.push('');
      lines.push('## Kontakt');
      lines.push(`Telefon: ${phone}  `);
      lines.push(`E-Mail: ${email}  `);
      lines.push('');
      lines.push('## Handelsregistereintrag & Unternehmens-Identifikationsnummer (UID)');
      lines.push(`Eingetragener Firmenname: ${company}  `);
      lines.push(`Handelsregisteramt: ${regCourt}  `);
      lines.push(`Handelsregister-Nummer: ${regNumber}  `);
      if (vatId) {
        lines.push(`UID / MWST-Nummer: **${vatId}**  `);
      }
      lines.push('');
      if (hasEditorial) {
        lines.push('## Redaktionelle Verantwortung');
        lines.push(`Inhaltlich verantwortlich: ${editorialPerson}, ${zipCity}  `);
        lines.push('');
      }
      lines.push('## Haftungsausschluss');
      lines.push('Der Autor übernimmt keinerlei Gewähr hinsichtlich der inhaltlichen Richtigkeit, Genauigkeit, Aktualität, Zuverlässigkeit und Vollständigkeit der Informationen. Haftungsansprüche gegen den Autor wegen Schäden materieller oder immaterieller Art, welche aus dem Zugriff oder der Nutzung bzw. Nichtnutzung der veröffentlichten Informationen entstehen, werden ausgeschlossen. Alle Angebote sind unverbindlich.');
    }

    return lines.join('\n');
  }

  /**
   * Generiert eine 100% DSGVO- bzw. revDSG-konforme Datenschutzerklärung 2026
   */
  function generatePrivacyPolicy(config) {
    config = config || {};
    const country = (config.country || 'DE').toUpperCase();
    const company = config.companyName || 'Musterfirma GmbH';
    const person = config.personName || 'Max Mustermann';
    const street = config.street || 'Musterstraße 123';
    const zipCity = config.zipCity || (country === 'CH' ? '8001 Zürich' : (country === 'AT' ? '1010 Wien' : '10115 Berlin'));
    const email = config.email || 'datenschutz@musterfirma.de';

    const lines = [];
    lines.push('# Datenschutzerklärung');
    lines.push('');
    lines.push('## 1. Verantwortliche Stelle');
    lines.push('Verantwortlich für die Datenverarbeitung auf dieser Website ist:');
    lines.push('');
    lines.push(`**${company}**  `);
    lines.push(`${street}  `);
    lines.push(`${zipCity}  `);
    lines.push(`Vertreten durch: ${person}  `);
    lines.push(`E-Mail: ${email}  `);
    lines.push('');

    lines.push('## 2. Rechtsgrundlagen der Verarbeitung');
    if (country === 'CH') {
      lines.push('Wir bearbeiten Personendaten in Übereinstimmung mit dem Schweizer Datenschutzgesetz, insbesondere dem Bundesgesetz über den Datenschutz (**revDSG**) und der Datenschutzverordnung (DSV). Sofern und soweit die EU-Datenschutz-Grundverordnung (DSGVO) anwendbar ist, erfolgt die Bearbeitung ergänzend auf Grundlage von Art. 6 Abs. 1 DSGVO.');
    } else {
      lines.push('Die Verarbeitung personenbezogener Daten erfolgt im Einklang mit der Datenschutz-Grundverordnung (**DSGVO**), dem Bundesdatenschutzgesetz (BDSG, Deutschland) bzw. dem Datenschutzgesetz (DSG, Österreich) sowie dem **§ 25 Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG)** für Speicherungen und Abrufe auf dem Endgerät.');
    }
    lines.push('');

    lines.push('## 3. Hosting & Server-Log-Dateien');
    lines.push('Beim Aufrufen unserer Website erfasst der Webserver automatisch technische Informationen (Browsertyp, Version, Betriebssystem, Referrer URL, Hostname, Uhrzeit und anonymisierte IP-Adresse). Grundlage für die Datenverarbeitung ist Art. 6 Abs. 1 lit. f DSGVO bzw. Art. 6 revDSG (berechtigtes Interesse an Systemsicherheit und technischer Integrität).');
    lines.push('');

    lines.push('## 4. Cookies & Endgerätezugriff nach § 25 TDDDG / revDSG');
    lines.push('Unsere Website verwendet ausschließlich technisch notwendige Cookies oder greift erst nach ausdrücklicher Einwilligung auf Speicherfunktionen Ihres Endgerätes zu. Gemäß **§ 25 Abs. 1 TDDDG** bedarf der Zugriff auf Informationen in der Endeinrichtung der informierten Einwilligung des Nutzers. Zwingend erforderliche Speicherungen erfolgen gemäß **§ 25 Abs. 2 TDDDG** bzw. Art. 6 revDSG.');
    lines.push('');

    lines.push('## 5. SSL- bzw. TLS-Verschlüsselung');
    lines.push('Diese Seite nutzt aus Sicherheitsgründen und zum Schutz der Übertragung vertraulicher Inhalte eine moderne SSL- bzw. TLS-Verschlüsselung. Wenn die Verschlüsselung aktiviert ist, können Daten nicht von unbefugten Dritten mitgelesen werden.');
    lines.push('');

    lines.push('## 6. Datenübermittlung in Drittstaaten & Cloud-Dienste');
    if (country === 'CH') {
      lines.push('Gemäß Art. 19 Abs. 2 lit. b revDSG teilen wir Ihnen mit, dass wir Personendaten primär in der Schweiz und im EWR bearbeiten. Soweit Dienste von Drittanbietern mit Sitz in den USA genutzt werden, erfolgt die Bekanntgabe gestützt auf das Swiss-U.S. Data Privacy Framework oder Standardvertragsklauseln (SCC) des EDÖB.');
    } else {
      lines.push('Soweit wir Daten in Drittländern (außerhalb der EU bzw. des EWR) verarbeiten, erfolgt dies nur nach Art. 44 ff. DSGVO (EU-U.S. Data Privacy Framework oder Standardvertragsklauseln der EU-Kommission).');
    }
    lines.push('');

    lines.push('## 7. Ihre Rechte (Auskunft, Berichtigung, Löschung, Widerruf & Widerspruch)');
    lines.push('Sie haben jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft, Empfänger und Zweck sowie ein Recht auf Berichtigung, Sperrung oder Löschung.');
    lines.push('');
    lines.push('**Recht auf Widerruf der datenschutzrechtlichen Einwilligung:**  ');
    lines.push('Sie können eine bereits erteilte Einwilligung jederzeit formlos per E-Mail an uns widerrufen. Die Rechtmäßigkeit der bis zum Widerruf erfolgten Datenverarbeitung bleibt unberührt.');
    lines.push('');
    lines.push('**Widerspruchsrecht gegen die Datenerhebung in besonderen Fällen (Art. 21 DSGVO):**  ');
    lines.push('WENN DIE DATENVERARBEITUNG AUF GRUNDLAGE VON ART. 6 ABS. 1 LIT. E ODER F DSGVO ERFOLGT, HABEN SIE JEDERZEIT DAS RECHT, AUS GRÜNDEN IHRER BESONDEREN SITUATION GEGEN DIE VERARBEITUNG WIDERSPRUCH EINZULEGEN.');
    lines.push('');

    lines.push('## 8. Beschwerderecht bei der zuständigen Aufsichtsbehörde');
    if (country === 'CH') {
      lines.push('Zuständige Datenschutz-Aufsichtsbehörde in der Schweiz ist der Eidgenössische Datenschutz- und Öffentlichkeitsbeauftragte (**EDÖB**), Feldeggweg 1, CH-3003 Bern (https://www.edoeb.admin.ch).');
    } else if (country === 'AT') {
      lines.push('Zuständige Aufsichtsbehörde in Österreich ist die **Österreichische Datenschutzbehörde (DSB)**, Barichgasse 40-42, 1030 Wien (https://www.dsb.gv.at).');
    } else {
      lines.push('Zuständige Aufsichtsbehörde ist der zuständige Landesbeauftragte für den Datenschutz bzw. der Bundesbeauftragte für den Datenschutz und die Informationsfreiheit (**BfDI**).');
    }

    return lines.join('\n');
  }

  /**
   * Führt die Selbsttests aus
   */
  function runSelfTest() {
    console.log('='.repeat(70));
    console.log('🧪 DACH IMPRESSUM & DSGVO JS COMPLIANCE CHECKER – SELBSTTEST-SUITE 2026');
    console.log('='.repeat(70));

    // Test 1: Veraltetes TMG
    const res1 = scanCompliance('Angaben nach § 5 TMG. Test GmbH Berlin.', 'DE');
    if (!res1.findings.some(f => f.id === 'OUTDATED_TMG')) {
      throw new Error('Test 1 fehlgeschlagen: OUTDATED_TMG nicht erkannt!');
    }
    console.log(`  [PASS] Test 1: Veraltetes § 5 TMG erkannt (Score: ${res1.score}/100)`);

    // Test 2: Veraltetes TTDSG
    const res2 = scanCompliance('Cookies nach TTDSG einsetzen.', 'DE');
    if (!res2.findings.some(f => f.id === 'OUTDATED_TTDSG')) {
      throw new Error('Test 2 fehlgeschlagen: OUTDATED_TTDSG nicht erkannt!');
    }
    console.log(`  [PASS] Test 2: Veraltetes TTDSG erkannt (Score: ${res2.score}/100)`);

    // Test 3: Veralteter RStV
    const res3 = scanCompliance('Verantwortlich nach § 55 Abs. 2 RStV: Max Mustermann.', 'DE');
    if (!res3.findings.some(f => f.id === 'OUTDATED_RSTV')) {
      throw new Error('Test 3 fehlgeschlagen: OUTDATED_RSTV nicht erkannt!');
    }
    console.log(`  [PASS] Test 3: Veralteter RStV erkannt (Score: ${res3.score}/100)`);

    // Test 4: Fehlendes revDSG (CH)
    const res4 = scanCompliance('Datenschutzerklärung für Schweizer Kunden.', 'CH');
    if (!res4.findings.some(f => f.id === 'MISSING_CH_REVDSG')) {
      throw new Error('Test 4 fehlgeschlagen: MISSING_CH_REVDSG nicht erkannt!');
    }
    console.log(`  [PASS] Test 4: Fehlendes revDSG erkannt (Score: ${res4.score}/100)`);

    // Test 5: Fehlendes ECG & Blattlinie (AT)
    const res5 = scanCompliance('Impressum: Firma AT GmbH, Wien.', 'AT');
    if (!res5.findings.some(f => f.id === 'MISSING_AT_ECG') || !res5.findings.some(f => f.id === 'MISSING_AT_BLATTLINIE')) {
      throw new Error('Test 5 fehlgeschlagen: ECG oder Blattlinie nicht erkannt!');
    }
    console.log(`  [PASS] Test 5: Fehlendes ECG & Blattlinie erkannt (Score: ${res5.score}/100)`);

    // Test 6: Google Fonts Remote
    const res6 = scanCompliance('Import von fonts.googleapis.com im Stylesheet.', 'ALL');
    if (!res6.findings.some(f => f.id === 'REMOTE_GOOGLE_FONTS_RISK')) {
      throw new Error('Test 6 fehlgeschlagen: REMOTE_GOOGLE_FONTS_RISK nicht erkannt!');
    }
    console.log(`  [PASS] Test 6: Google Fonts Remote erkannt (Score: ${res6.score}/100)`);

    // Test 7: Generator DE
    const deImp = generateImpressum({ country: 'DE', companyName: 'Test GmbH DE' });
    const deDpo = generatePrivacyPolicy({ country: 'DE', companyName: 'Test GmbH DE' });
    const resGenDe = scanCompliance(deImp + '\n\n' + deDpo, 'DE');
    if (resGenDe.score !== 100) {
      throw new Error(`Test 7 fehlgeschlagen: DE Score ist ${resGenDe.score} statt 100!`);
    }
    console.log(`  [PASS] Test 7: Generator DE erzeugt 100 % konformen Text (Score: ${resGenDe.score}/100)`);

    // Test 8: Generator AT
    const atImp = generateImpressum({ country: 'AT', companyName: 'Test GmbH AT' });
    const atDpo = generatePrivacyPolicy({ country: 'AT', companyName: 'Test GmbH AT' });
    const resGenAt = scanCompliance(atImp + '\n\n' + atDpo, 'AT');
    if (resGenAt.score !== 100) {
      throw new Error(`Test 8 fehlgeschlagen: AT Score ist ${resGenAt.score} statt 100!`);
    }
    console.log(`  [PASS] Test 8: Generator AT erzeugt 100 % konformen Text (Score: ${resGenAt.score}/100)`);

    // Test 9: Generator CH
    const chImp = generateImpressum({ country: 'CH', companyName: 'Test AG CH', vatId: 'CHE-999.888.777 MWST' });
    const chDpo = generatePrivacyPolicy({ country: 'CH', companyName: 'Test AG CH' });
    const resGenCh = scanCompliance(chImp + '\n\n' + chDpo, 'CH');
    if (resGenCh.score !== 100) {
      throw new Error(`Test 9 fehlgeschlagen: CH Score ist ${resGenCh.score} statt 100!`);
    }
    console.log(`  [PASS] Test 9: Generator CH erzeugt 100 % konformen Text (Score: ${resGenCh.score}/100)`);

    console.log('-'.repeat(70));
    console.log('✅ ALLE 9 JS-SELBSTTESTS ERFOLGREICH BESTANDEN!');
    console.log('='.repeat(70));
    return true;
  }

  // Node CLI Unterstützung
  if (typeof process !== 'undefined' && process.argv && require.main === module) {
    const args = process.argv.slice(2);
    if (args.includes('--test')) {
      try {
        runSelfTest();
        process.exit(0);
      } catch (err) {
        console.error('❌ Test-Fehler:', err.message);
        process.exit(1);
      }
    }

    const fs = require('fs');
    let country = 'ALL';
    let file = null;
    let text = null;
    let isJson = args.includes('--json');
    let genImp = args.includes('--generate-impressum');
    let genDpo = args.includes('--generate-privacy');

    for (let i = 0; i < args.length; i++) {
      if (args[i] === '--country' && args[i + 1]) country = args[++i].toUpperCase();
      if (args[i] === '--file' && args[i + 1]) file = args[++i];
      if (args[i] === '--text' && args[i + 1]) text = args[++i];
    }

    if (genImp || genDpo) {
      const cfg = { country: country === 'ALL' ? 'DE' : country };
      const out = [];
      if (genImp) out.push(generateImpressum(cfg));
      if (genDpo) out.push(generatePrivacyPolicy(cfg));
      console.log(out.join('\n\n---\n\n'));
      process.exit(0);
    }

    let contentToScan = text;
    if (file) {
      contentToScan = fs.readFileSync(file, 'utf8');
    }

    if (!contentToScan) {
      console.log('Nutzung: node impressum_dsgvo_checker.js [--test | --text "..." | --file pfad | --generate-impressum]');
      process.exit(1);
    }

    const result = scanCompliance(contentToScan, country);
    if (isJson) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log('='.repeat(70));
      console.log(` ⚖️ DACH COMPLIANCE SCANNER JS 2026 – ERGEBNIS (${country})`);
      console.log('='.repeat(70));
      console.log(`Compliance Score : ${result.score} / 100`);
      console.log(`Status           : ${result.isCompliant ? '✅ RECHTSKONFORM' : '⚠️ ABMAHNRISIKO / ANPASSUNG ERFORDERLICH'}`);
      console.log(`Befunde          : ${result.totalFindings} (Kritisch: ${result.summary.critical}, Hoch: ${result.summary.high}, Mittel: ${result.summary.medium}, Gering: ${result.summary.low})`);
      console.log('-'.repeat(70));
      result.findings.forEach((f, idx) => {
        console.log(`${idx + 1}. [${f.severity}] ${f.title}`);
        console.log(`   Norm: ${f.legalBasis}`);
        console.log(`   Tipp: ${f.recommendation}`);
      });
      console.log('-'.repeat(70));
      console.log(`🌐 Live Generator: ${result.liveGeneratorUrl}`);
      console.log('='.repeat(70));
    }
  }

  return {
    scanCompliance,
    generateImpressum,
    generatePrivacyPolicy,
    runSelfTest,
    SEVERITY
  };
});
