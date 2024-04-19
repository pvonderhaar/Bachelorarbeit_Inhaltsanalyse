# Bachelorarbeit Inhaltsanalysee von Twitter-Dialogen

## Titel der Arbeit: Eine Inhaltsanalyse von Zwiegesprächen auf Twitter über Migration

## Fragestellung: Wie verhalten sich Twitter-User:innen in Zwiegesprächen über Migration, in denen Uneinigkeit herrscht?

Die Arbeit widmet sich einer sozialwissenschaftlichen Fragestellung, die aber mit Hilfe von Werkzeugen aus der Informatik bzw. der Data Science beantwortet wird. Der Code für den Informatikteil ist in diesem Git-Repository gespeichert. Die verschiedenen ordner beeinhalten:

### scripts:
- dialogue_fuctions.py : Funktionen, die die Daten in Paths, die Dialoge enthalten, sortieren

### tests
- Testfunktionen und Testdaten

### statistics
- statistische Auswertung der Ergebnisse der Inhaltsanalyse und Plots, die in der Arbeit zu finden sind.

### daten
- Dieser Ordner steht im gitignore, weil die Datensätze personenbezogene Daten enthalten und nicht öffentlich einsehbar sein sollten.

## Vorraussetzungen
- Um die Funktionen zur Erkennung von Dialogen zu nutzen muss der Datensatz folgende Vorraussetzungen erfüllen: 
    - Der Datensatz kann als Delab-Tree gespeichert werden. Mehr Informationen dazu hier: https://github.com/juliandehne/delab-trees
    - Weiterhin muss der Datensatz die Spalte "in_reply_to_user_id" enthalten.
- Vorrausgesetzte Libraries in requirement.txt


