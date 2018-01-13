import sys
import json
from datetime import datetime
from datetime import date as dat



def parseJSON(filename):
    with open(filename, "r") as f:
        data = f.read()
        return json.loads(data)

def isValidJSON(jsn):
    # TODO
    return True

def findMax(jsn, s, MAX=20):
    for i in range(1,MAX):
        try:
            jsn[s.replace("%%",str(i))]
        except:
            return i
    return MAX

def json2xml(jsn):
    xml = '<?xml version="1.0"?><xsud>'
    date = datetime.strptime(jsn["Datum"], '%d.%m.%Y').isoformat()
    today = dat.today().isoformat()

    xml += '<Global><!--Erstellungsdatum der Exportdatei--><Datum Einheit="Qt::ISODate">%s</Datum></Global>' % date

    xml += '<Version><!--Versionsstand der Datenbank--><Datenbank>22</Datenbank><!--Versionsstand der Exportdatei--><xsud>9</xsud><!--Versionsstand kleiner-brauhelfer--><kleiner-brauhelfer>1.4.3.2</kleiner-brauhelfer></Version>'

    xml += '<Sud>'

    xml += '<!--Bezeichner fuer den Sud--><Sudname>%s</Sudname>' % jsn['Name']

    xml += '<!--Zeitstempel fuer Erstellungsdatum in der Datenbank--><Erstellt Einheit="Qt::ISODate">%s</Erstellt>' % date

    xml += '<!--Zeitstempel wann Sud das letzte-mal in der Datenbank gespeichert wurde--><Gespeichert Einheit="Qt::ISODate">%s</Gespeichert>' % date

    xml += '<!--Soll Wuerze-Anstellmenge--><Menge Einheit="Liter">%s</Menge>' % str(jsn['Ausschlagswuerze'])

    xml += '<!--Soll Stammwuerze--><SW Einheit="Grad Plato">%s</SW>' % str(jsn['Stammwuerze'])

    xml += '<!--Soll CO2 Gehalt--><CO2 Einheit="Gramm/Liter">'
    xml += str(jsn['Karbonisierung'])
    xml += '</CO2>'

    xml += '<!--Soll Bittere--><IBU Einheit="IBU">'
    xml += str(jsn['Bittere'])
    xml += '</IBU>'

    xml += '<!--Angepeilte Reifezeit--><Reifezeit Einheit="Wochen">'
    xml += '4'
    xml += '</Reifezeit>'
    print("Warning: please adjust Reifezeit manually in kb")

    xml += '<!--Allgemeiner Kommentar--><Kommentar><![CDATA['
    xml += jsn['Anmerkung_Autor']
    xml += ']]></Kommentar>'

    xml += '<!--Datum an dem der Sud gebraut wurde--><Braudatum Einheit="Qt::ISODate">'
    xml += today
    xml += '</Braudatum>'

    xml += '<!--Flag ob Sud gebraut wurde--><BierWurdeGebraut Einheit="Bool">0</BierWurdeGebraut><!--Flag ob Sud abgefuellt wurde--><BierWurdeAbgefuellt Einheit="Bool">0</BierWurdeAbgefuellt><!--Flag ob Sud verbraucht wurde--><BierWurdeVerbraucht Einheit="Bool">0</BierWurdeVerbraucht>'

    xml += '<!--Kochdauer nach der ersten Hopfengabe--><KochdauerNachBitterhopfung Einheit="Minuten">'
    xml += str(jsn['Kochzeit_Wuerze'])
    xml += '</KochdauerNachBitterhopfung>'
    print("Warning: maybe you need to manually adjust in kb: Kochdauer nach der ersten Hopfengabe")

    xml += '<!--Faktor zum Berechnen der Hauptgussmenge (Schuettung * Faktor = Hauptgussmenge)--><FaktorHauptguss Einheit="Faktor">0.8</FaktorHauptguss>'
    print("Warning: maybe you need to manually adjust in kb: FaktorHauptguss")

    xml += '<!--Name der Ausgewaehlten Hefe--><AuswahlHefe Einheit="Text">'
    xml += jsn['Hefe']
    xml += '</AuswahlHefe>'

    xml += '<!--Anzahl verwendeter Hefe Einheiten--><HefeAnzahlEinheiten Einheit="Integer">1</HefeAnzahlEinheiten>'

    xml += '<!--Wuerzemenge vor dem Hopfenseihen--><WuerzemengeVorHopfenseihen Einheit="Liter">'
    xml += str(jsn['Ausschlagswuerze'])
    xml += '</WuerzemengeVorHopfenseihen>'

    xml += '<!--Stammwuerze vor dem Hopfenseihen--><SWVorHopfenseihen Einheit="Grad Plato">'
    xml += str(jsn['Stammwuerze'])
    xml += '</SWVorHopfenseihen>'

    xml += '<!--Wuerzemenge nach dem Hopfenseihen--><WuerzemengeKochende Einheit="Liter">'
    xml += str(jsn['Ausschlagswuerze'])
    xml += '</WuerzemengeKochende>'

    xml += '<!--Stammwuerze nach dem Hopfenseihen--><SWKochende Einheit="Grad Plato">'
    xml += str(jsn['Stammwuerze'])
    xml += '</SWKochende>'

    xml += '<!--Abgefuellte Speisemenge--><Speisemenge Einheit="Liter">0</Speisemenge>'

    xml += '<!--Datum der Hefezugabe--><Anstelldatum Einheit="Qt::ISODate">'
    xml += today
    xml += '</Anstelldatum>'

    xml += '<WuerzemengeAnstellen Einheit="Liter">'
    xml += str(jsn['Ausschlagswuerze'])
    xml += '</WuerzemengeAnstellen>'

    xml += '<!--Stammwuerze bei der Hefezugabe--><SWAnstellen Einheit="Grad Plato">'
    xml += str(jsn['Stammwuerze'])
    xml += '</SWAnstellen>'

    xml += '<!--Abfuelldatum--><Abfuelldatum Einheit="Qt::ISODate">'
    xml += today
    xml += '</Abfuelldatum>'

    xml += '<!--Restextrakt der Schnellgaerprobe--><SWSchnellgaerprobe Einheit="Grad Plato">1</SWSchnellgaerprobe>'

    xml += '<!--Restextrakt des Jungbieres aus der Hauptgaerung--><SWJungbier Einheit="Grad Plato">3</SWJungbier>'

    xml += '<!--Temperatur Jungbier beim Abfuellen--><TemperaturJungbier Einheit="Grad Celsius">12</TemperaturJungbier>'

    xml += '<!--Temperatur Einmaischen--><EinmaischenTemp Einheit="Grad Celsius">'
    xml += str(jsn['Infusion_Einmaischtemperatur'])
    xml += '</EinmaischenTemp>'

    xml += '<!--Kosten fuer Wasser / Strom / Gas etc.--><KostenWasserStrom Einheit="Euro">0</KostenWasserStrom>'
    xml += '<!--Dauer die der Hopfen noch nach dem Kochen Bittere abgeben kann--><Nachisomerisierungszeit Einheit="Minuten">0</Nachisomerisierungszeit>'
    xml += '<!--Aktives Tab im kleinen-brauhelfer nach dem Laden--><AktivTab Einheit="Integer">1</AktivTab>'
    xml += '<!--Aktives Tab im Gaerverlauf nach dem Laden--><AktivTab_Gaerverlauf Einheit="Integer">1</AktivTab_Gaerverlauf>'

    xml += '<!--Gewuenschte Restalkalitaet--><RestalkalitaetSoll Einheit="Grad Deutsche Haerte">0</RestalkalitaetSoll>'
    print("Warning: maybe you need to manually adjust in kb: Restalkalität")

    xml += '<!--Flag ob eine Schnellgaeprobe gemacht wurde--><SchnellgaerprobeAktiv Einheit="Bool">0</SchnellgaerprobeAktiv>'

    xml += '<!--Bierfarbe--><erg_Farbe Einheit="EBC">1</erg_Farbe>'

    xml += '<!--Jungbiermenge beim Abfuellen--><JungbiermengeAbfuellen Einheit="Liter">'
    xml += str(jsn['Ausschlagswuerze'])
    xml += '</JungbiermengeAbfuellen>'

    xml += '<!--Beste Bewertung (Anzahl Sterne)--><Bewertung Einheit="Integer">0</Bewertung><!--Reifewoche der Besten Bewertung--><BewertungText Einheit="Text"></BewertungText><!--Maximale Anzahl Sterne bei diesem Sud--><BewertungMaxSterne Einheit="Integer">5</BewertungMaxSterne><!--Art der Hopfenberechnung--><berechnungsArtHopfen Einheit="Integer">0</berechnungsArtHopfen><!--High Gravity Faktor--><highGravityFaktor Einheit="Integer">0</highGravityFaktor>'

    # Rasten
    xml += '<Rasten>'
    
    max_rast = findMax(jsn, 'Infusion_Rasttemperatur%%')
    for i in range(1,max_rast):
        
        xml += '<Rast_%d>' % i
        xml += '<!--1 = Rast ist Aktiv--><RastAktiv Einheit="Bool">1</RastAktiv>'

        xml += '<!--Berschreibung der Rast--><RastName Einheit="Text">%d. Rast</RastName>' % i
        xml += '<!--Temperatur der Rast--><RastTemp Einheit="Grad Celsius">%s</RastTemp>' % jsn['Infusion_Rasttemperatur'+str(i)]
        xml += '<!--Rastdauer--><RastDauer Einheit="Minuten">%s</RastDauer>' % jsn['Infusion_Rastzeit'+str(i)]

        xml += '</Rast_%d>' % i

    xml += '</Rasten>'
    xml += '<Schuettung>'

    # save for later use
    malze = set()

    max_schuettung = findMax(jsn,'Malz%%')

    gesamt_schuettung = 0.0
    for i in range(1,max_schuettung):
        kg = 0.0
        if jsn['Malz%d_Einheit' % i ] == 'g':
            kg = float(jsn['Malz%d_Menge' % i ])/1000.0
        else:
            kg = float(jsn['Malz%d_Menge' % i ])
        gesamt_schuettung += float(kg)

    for i in range(1,max_schuettung):
        xml += '<Anteil_%d>' % i
        
        xml += '<!--Malzbeschreibung (Name)--><Name Einheit="Text">%s</Name>' % jsn['Malz'+str(i)]
        kg = 0.0
        if jsn['Malz%d_Einheit' % i ] == 'g':
            kg = float(jsn['Malz%d_Menge' % i ])/1000.0
        else:
            kg = float(jsn['Malz%d_Menge' % i ])
        xml += '<!--Prozentualer Anteil der Schuettung--><Prozent Einheit="Prozent">%f</Prozent>' % ((kg/gesamt_schuettung)*100.0)
        xml += '<!--Berechneter Gewichtsanteil der Schuettung--><erg_Menge Einheit="Kg">%s</erg_Menge>' % kg
        xml += '<!--Malz - Farbwert--><Farbe Einheit="EBC">1</Farbe>'

        malz = (jsn['Malz'+str(i)], kg)
        malze.add(malz)

        xml += '</Anteil_%d>' % i

    xml += '</Schuettung>'
    
    xml += '<Hopfengaben>'

    # save for later use
    hopfen = set()

    max_hopfen = findMax(jsn, 'Hopfen_%%_Sorte')

    gesamt_hopfen = 0.0
    for i in range(1,max_hopfen):
        gesamt_hopfen += float(jsn['Hopfen_%i_Menge' % i])

    for i in range(1,max_hopfen):
        xml += '<Anteil_%d>' % i
        xml += '<!--1 = Hopfengabe Aktiv--><Aktiv Einheit="Bool">1</Aktiv>'
        xml += '<!--Berschreibung Hopfen (Name)--><Name Einheit="Text">%s</Name>' % jsn['Hopfen_%d_Sorte' % i]
        xml += '<!--Zeit nach Hopfengabe 1--><Zeit Einheit="Minuten">%s</Zeit>' % jsn['Hopfen_%d_Kochzeit' % i]
        xml += '<!--Prozentualer Gewichts-anteil der Hopfengabe--><Prozent Einheit="Prozent">%f</Prozent>' % ((float(jsn['Hopfen_%i_Menge' % i])/gesamt_hopfen)*100)
        xml += '<!--Berechnete Gewichtsmenge--><erg_Menge Einheit="Gramm">%s</erg_Menge>' % jsn['Hopfen_%i_Menge' % i]
        xml += '<!--Beschreibungstext--><erg_Hopfentext Einheit="Text">%s %s %% Alpha</erg_Hopfentext>' % (jsn['Hopfen_%d_Sorte' % i], jsn['Hopfen_%d_alpha' % i])
        xml += '<!--Alphaprozent gehalt des Hopfens--><Alpha Einheit="Alpha Prozent">%s</Alpha>' % jsn['Hopfen_%d_alpha' % i]
        xml += '<!--Hopfenart 1 = Pellets--><Pellets Einheit="Bool">1</Pellets>'
        xml += '<!--Wen diese Gabe eine Vorderwuerzehopfung ist dann = 1--><Vorderwuerze Einheit="Bool">0</Vorderwuerze>'

        hopf = (jsn['Hopfen_%d_Sorte' % i], jsn['Hopfen_%d_alpha' % i])
        hopfen.add(hopf)

        xml += '</Anteil_%d>' % i

    xml += '</Hopfengaben>'
    xml += '<WeitereZutatenGaben/><Schnellgaerverlauf/><Hauptgaerverlauf/><Nachgaerverlauf/><Bewertungen/>'
    xml += '</Sud>'

    xml += '<!--Hier sind die Rohstoffe aufgelistet die Im Sud verwendet wurden--><Rohstoffe>'

    xml += '<Malz>'

    malze = list(malze)

    for i in range(1,len(malze)+1):
        m_name, m_gew = malze[i-1]

        xml += '<Eintrag_%d>' % i

        xml += '<!--Malzbeschreibung (Name)--><Beschreibung Einheit="Text">%s</Beschreibung>' % m_name
        xml += '<!--Malzfarbwert--><Farbe Einheit="EBU">1</Farbe>'
        xml += '<!--Maximal empfohlener Schuettungsanteil--><MaxProzent Einheit="Prozent">100</MaxProzent>'

        xml += '<!--Vorhandene Rohstoffmenge--><Menge Einheit="Kg">%s</Menge>' % m_gew
        xml += '<!--Einkaufspreis--><Preis Einheit="Euro/Kg">0</Preis>'
        xml += '<!--Bemerkung--><Bemerkung Einheit="Text"><![CDATA[]]></Bemerkung>'
        xml += '<!--Anwendung--><Anwendung Einheit="Text"><![CDATA[]]></Anwendung>'
        xml += '<!--Datum Eingelagert--><Eingelagert Einheit="Qt::ISODate">%s</Eingelagert>' % today
        xml += '<!--Datum Mindesthaltbar--><Mindesthaltbar Einheit="Qt::ISODate">%s</Mindesthaltbar>' % today

        xml += '</Eintrag_%d>' % i

    xml += '</Malz>'
    xml += '<Hopfen>'

    hopfen = list(hopfen)

    for i in range(1, len(hopfen)+1):
        h_sorte, h_alpha = hopfen[i-1]

        xml += '<Eintrag_%d>' % i

        xml += '<!--Hopfenbeschreibung (Name)--><Beschreibung Einheit="Text">%s</Beschreibung>' % h_sorte
        xml += '<!--Alphaprozentgehalt--><Alpha Einheit="Alpha Prozent">%s</Alpha>' % h_alpha
        xml += '<!--Vorhandene Menge--><Menge Einheit="Gramm">0</Menge>'
        xml += '<!--Einkaufspreis--><Preis Einheit="Euro/Kg">0</Preis>'
        xml += '<!--Hopfenart 1=Pellets--><Pellets Einheit="Text">1</Pellets>'
        xml += '<!--Bemerkung--><Bemerkung Einheit="Text"><![CDATA[]]></Bemerkung>'
        xml += '<!--Eigenschaften--><Eigenschaften Einheit="Text"><![CDATA[]]></Eigenschaften>'
        xml += '<!--Typ 1=Aroma 2=Bitter 3=Universal--><Typ Einheit="Integer">3</Typ>'
        xml += '<!--Datum Eingelagert--><Eingelagert Einheit="Qt::ISODate">%s</Eingelagert>' % today
        xml += '<!--Datum Mindesthaltbar--><Mindesthaltbar Einheit="Qt::ISODate">%s</Mindesthaltbar>' % today


        xml += '</Eintrag_%d>' % i

    xml += '</Hopfen>'

    xml += '<Hefe>'

    hefe = jsn['Hefe']

    xml += '<Eintrag_1><!--Hefebeschreibung (Name)--><Beschreibung Einheit="Text">%s</Beschreibung>'
    xml += '<!--Vorhandene Menge--><Menge Einheit="Einheiten">0</Menge>'
    xml += '<!--Benoetigte Einheiten--><Einheiten Einheit="Einheiten"></Einheiten>'
    xml += '<!--Einkaufspreis--><Preis Einheit="Euro/Einheit">0</Preis>'
    xml += '<!--Bemerkung--><Bemerkung Einheit="Text"><![CDATA[]]></Bemerkung>'
    xml += '<!--TypOGUG 1=Obergaerig 2=Untergaerig--><TypOGUG Einheit="Integer">1</TypOGUG>'
    xml += '<!--TypTrFl 1=Trocken 2=Fluessig--><TypTrFl Einheit="Integer">1</TypTrFl>'
    xml += '<!--Verpackungsmenge--><Verpackungsmenge Einheit="Text"></Verpackungsmenge>'
    xml += '<!--Wuerzemenge--><Wuerzemenge Einheit="Integer">0</Wuerzemenge>'
    xml += '<!--Eigenschaften--><Eigenschaften Einheit="Text"><![CDATA[]]></Eigenschaften>'
    xml += '<!--SED 1=Hoch 2=Mittel 3=Niedrig--><SED Einheit="Integer">1</SED>'
    xml += '<!--EVG Endvergaerungsgrad--><EVG Einheit="Text"></EVG>'
    xml += '<!--Temperatur--><Temperatur Einheit="Text"></Temperatur>'
    xml += '<!--Datum Eingelagert--><Eingelagert Einheit="Qt::ISODate">%s</Eingelagert>' % today
    xml += '<!--Datum Mindesthaltbar--><Mindesthaltbar Einheit="Qt::ISODate">%s</Mindesthaltbar>' % today
    
    xml += '</Eintrag_1>'

    xml += '</Hefe>'
    # todo add here more code
    xml += '<WeitereZutaten/>'
    xml += '</Rohstoffe>'
    xml += '</xsud>'

    return xml


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: json2xsud file.json")
        sys.exit(1)
    parsed = parseJSON(sys.argv[1])
    if not isValidJSON(parsed):
        print("please provide a valid json file")
        sys.exit(1)
    print("parsed json")
    xml = json2xml(parsed)
    print("generated xml")
    outname = sys.argv[1][:-5] + '.xsud'

    with open(outname, 'w') as f:
        f.write(xml)
    print("saved xml")
    