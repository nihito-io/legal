---
title: Auftragsverarbeitungsvertrag (AVV) nihito planner
version: legal-2026-10-19
effective: 2026-10-19
---

## 1. Gegenstand

Dieser Auftragsverarbeitungsvertrag («AVV») ist Anhang der [Nutzungsbedingungen](https://nihito-io.github.io/legal/latest/terms.html) des nihito planner und wird mit ihnen angenommen. Er gilt, soweit die nihito gmbh, c/o ETH Zürich, D-MAVT ML H42.1, Sonneggstrasse 3, 8092 Zürich, Schweiz («nihito»), als Auftragsverarbeiterin Personendaten für den Kunden als Verantwortlichen bearbeitet. In Fragen des Datenschutzes geht er den Nutzungsbedingungen vor. Massgebend sind das DSG und, soweit anwendbar, Art. 28 DSGVO.

## 2. Bearbeitung und Weisungen

nihito bearbeitet die Daten nur, um den planner bereitzustellen (Anhang 1), und nur nach den Weisungen des Kunden. Diese ergeben sich aus den Nutzungsbedingungen, diesem AVV und der Nutzung des planner; weitere Weisungen erteilt der Kunde per E-Mail. Hält nihito eine Weisung für rechtswidrig, informiert sie den Kunden. Alle Personen mit Zugriff auf die Daten sind zur Vertraulichkeit verpflichtet.

## 3. Zugriff durch nihito

Nur die Administratorinnen und Administratoren von nihito haben Zugriff auf die planner-Instanz des Kunden. Sie können sie öffnen, ihre Protokolle lesen, Backups anlegen, wiederherstellen und löschen, den Zugang freigeben oder entziehen und Updates auslösen, und zwar nur, soweit es für Betrieb, Support oder Fehlersuche nötig ist. Eine Anmeldung unter dem Konto des Kunden ist nicht möglich.

## 4. Sicherheit

nihito trifft die Massnahmen nach Anhang 2 und passt sie dem Stand der Technik an, ohne das Schutzniveau zu senken.

## 5. Unterauftragsverarbeiter und Bearbeitung in den USA

Der Kunde genehmigt die Unterauftragsverarbeiter in Anhang 3. nihito verpflichtet sie zu einem gleichwertigen Datenschutz. Neue Unterauftragsverarbeiter führt nihito mit einer neuen Fassung dieses AVV ein, die der Kunde nach Ziffer 12 der Nutzungsbedingungen annimmt oder ablehnt.

Die Daten liegen bei AWS in der Region us-east-1 (USA). Mit der Nutzung des planner weist der Kunde nihito an, sie dort zu bearbeiten. Die Übermittlung stützt sich auf das EU-U.S. und das Swiss-U.S. Data Privacy Framework und ergänzend auf die Standardvertragsklauseln der EU-Kommission mit den Anpassungen für die Schweiz, die nihito mit den Unterauftragsverarbeitern vereinbart hat.

## 6. Unterstützung und Verletzungen der Datensicherheit

nihito unterstützt den Kunden angemessen bei Anfragen betroffener Personen, bei Datenschutz-Folgenabschätzungen und gegenüber Behörden. Von einer Verletzung der Datensicherheit, die Daten des Kunden betrifft, informiert nihito den Kunden unverzüglich, mit den Angaben, die er für seine eigenen Meldepflichten braucht.

## 7. Rückgabe und Löschung

Der Kunde kann seine Daten jederzeit im planner herunterladen. Nach Ende des Vertrags oder des Zugangs löscht nihito die Daten nach Ziffer 10 der Nutzungsbedingungen: die planner-Instanz nach 30 Tagen, Backups spätestens 7 Tage später.

## 8. Nachweise

nihito gibt dem Kunden auf Anfrage die Informationen, die er zur Prüfung dieses AVV braucht. Weitergehende Kontrollen sind nach Absprache höchstens einmal pro Jahr und auf Kosten des Kunden möglich.

## Anhang 1: Beschreibung der Bearbeitung

| Merkmal | Beschreibung |
|---|---|
| Betroffene Personen | Nutzerinnen und Nutzer des Kunden und Personen, deren Daten der Kunde erfasst, etwa Mitarbeitende oder Fahrerinnen und Fahrer |
| Daten | Eingaben im planner (Depots, Fahrzeuge, Einsatzpläne, Zuordnungen), Ergebnisse und Berichte, Protokolle der planner-Instanz, Inhalte von Support-Anfragen |
| Besondere Kategorien | Keine; der Kunde erfasst keine besonders schützenswerten Personendaten |
| Bearbeitungen | Speichern, Berechnen, Anzeigen, Sichern, Wiederherstellen, Löschen; Einsicht für Support und Fehlersuche |
| Dauer | Vertragsdauer und Löschfrist nach Ziffer 7 |

## Anhang 2: Technische und organisatorische Massnahmen

- Eigene planner-Instanz mit eigenen Datenträgern für jeden Kunden.
- TLS-Verschlüsselung aller Verbindungen; verschlüsselte Datenträger, Backups und Dateispeicher (Amazon S3).
- Anmeldung für planner und planner-Instanz; Zugriff von nihito nur durch die Administratorengruppe (Ziffer 3).
- Dateispeicher ohne öffentlichen Zugriff; Download-Links gelten höchstens 45 Minuten.
- Backups täglich um 03:00 UTC sowie vor jeder Pause und jedem Update; Löschung nach 7 Tagen.
- Härtung der planner-Instanzen bei der Einrichtung, unter anderem mit einer Firewall.

## Anhang 3: Unterauftragsverarbeiter

| Unterauftragsverarbeiter | Zweck | Ort |
|---|---|---|
| Amazon Web Services, Inc. | Hosting von planner-Instanzen, Backups, Dateispeicher, Anmeldedienst und Backend | USA (us-east-1) |
| Twilio Inc. (SendGrid) | E-Mail-Versand von Support-Nachrichten, soweit sie Daten des Kunden enthalten | USA |
