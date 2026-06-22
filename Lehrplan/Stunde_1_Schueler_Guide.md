# 📘 Stunde 1 – Einführung

## 🎯 Ziel der Stunde

In dieser ersten Stunde lernst du die Grundlagen eines eigenen Spiels kennen. Du verstehst, wie ein Spiel überhaupt funktioniert – ganz ohne Mausklicks oder bunte Grafiken.

Nach dieser Stunde kannst du:
- erklären, was ein Spielefenster ist
- beschreiben, was eine Spielschleife tut
- sagen, wie der Spieler das Spiel beenden kann
- Farben am Computer in Rot, Grün und Blau angeben

---

## 🧭 Inhalt dieser Stunde

In **Stunde 1 – Das Fundament** geht es um drei Schritte, die jedes Spiel braucht:

**Schritt 1: Initialisierung**  
Bevor ein Spiel losgeht, muss alles vorbereitet werden. Das Fenster wird erstellt, die Werkzeuge (Pygame) werden geladen. Das passiert genau einmal am Anfang.

**Schritt 2: Spielschleife**  
Danach beginnt eine Schleife, die sich immer wiederholt:  
Eingaben prüfen → Spiel berechnen → Bild zeichnen → und wieder von vorne.

**Schritt 3: Beenden**  
Irgendwann will der Spieler aufhören. Dann wird das Fenster geschlossen und das Programm sauber beendet.

Dieses Muster findest du in **jedem** Spiel wieder – egal ob Tetris, Minecraft oder ein Jump-'n'-Run.

---

## 🧠 Aufgaben für Schüler

### 🔹 Aufgabe 1: Die drei Schritte

Öffne die Datei `Lehrplan/Stunde 1.md` und sieh dir die Kommentare am Anfang an.

📌 **Frage:** Welche drei Dinge werden in Stunde 1 gebaut? Schreibe sie in eigenen Worten auf.

---

### 🔹 Aufgabe 2: Was ist eine Bibliothek?

Im Code wird `import pygame` verwendet. Pygame ist eine sogenannte **Bibliothek**.

📌 **Frage:** Stell dir vor, du baust ein Haus. Was wäre einfacher:  
(A) Jeden Nagel, jede Schraube und jedes Brett selbst herstellen  
oder  
(B) fertige Bauteile aus dem Baumarkt verwenden?  

Übertrage diesen Vergleich auf Pygame. Warum erleichtert eine Bibliothek das Programmieren?

---

### 🔹 Aufgabe 3: Farben entdecken

Im Code siehst du Zeilen wie:  
`FARBE_SCHWARZ = (0, 0, 0)`  
`FARBE_WEISS = (255, 255, 255)`  
`FARBE_BLAU = (0, 0, 255)`

📌 **Aufgabe:**  
a) Welche Farbe würdest du bei `(255, 0, 0)` erwarten?  
b) Was passiert, wenn du `(0, 255, 0)` verwendest?  
c) Wie würdest du ein helles Gelb mischen? (Tipp: Gelb = Rot + Grün)

---

### 🔹 Aufgabe 4: Die Spielschleife verstehen

Die Spielschleife läuft immer und immer wieder. Sie tut jedes Mal das Gleiche.

📌 **Frage:** Was würde der Spieler sehen, wenn die Spielschleife NUR EINMAL durchlaufen würde und dann aufhört? Beschreibe kurz.

---

### 🔹 Aufgabe 5: Ereignisse erkennen

Das Programm prüft ständig, ob der Spieler etwas tut – zum Beispiel eine Taste drückt.

📌 **Frage:** Welche Tasten oder Aktionen fallen dir ein, mit denen der Spieler ein Spiel steuern könnte? Nenne mindestens vier verschiedene Möglichkeiten.

---

### 🔹 Aufgabe 6: Die Besonderheit von `__name__`

Ganz unten im Code steht:  
`if __name__ == "__main__":`

📌 **Frage:** Warum ist diese Zeile wichtig? Was glaubst du passiert, wenn man sie weglässt und die Datei von einer anderen Python-Datei importiert wird? (Tipp: Überlege, ob dann sofort das Fenster aufgehen würde.)

---

## 💡 Hinweise

- **Lies die Kommentare!** Der Code in `Lehrplan/Stunde 1.md` ist voller Erklärungen. Die `# TIPP:`-Kommentare zeigen dir sogar, was in späteren Stunden noch dazukommt.
- **Nicht alles verstehen?** Das ist völlig normal. Konzentriere dich auf die drei Schritte: Initialisierung → Schleife → Beenden. Der Rest wird in den nächsten Stunden klarer.
- **Farben merken:** RGB steht für **R**ot, **G**rün, **B**lau. Werte von 0 bis 255. 0 = aus, 255 = volle Leuchtkraft.
- **Variablen mit Umlauten:** Python unterscheidet `laeuft` und `läuft`. Das sind zwei verschiedene Namen! Deshalb schreibt man lieber `laeuft` statt `läuft`.

---

## 🧪 Reflexion

Nimm dir einen Moment und beantworte diese Fragen für dich:

1. **Was habe ich heute gelernt?**  
   Welcher Teil von Stunde 1 war für dich am interessantesten?

2. **Was war unklar?**  
   Gab es etwas, das du nicht verstanden hast? Schreibe es auf – in der nächsten Stunde kannst du nachfragen.

3. **Was möchte ich noch verstehen?**  
   Wenn du dir etwas wünschen könntest: Was würdest du als Nächstes über Spieleprogrammierung lernen wollen?