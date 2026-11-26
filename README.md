# Adventskalender mit täglicher Astrowoche-Vorschau

1. Entpacke dieses ZIP in den Hauptordner deines GitHub-Repos für den Kalender. Der Ordner `.github` gehört mit ins Repo.
2. Lass deine Bilder im Ordner `fotos/` neben der `index.html`.
3. Wähle auf GitHub unter **Settings → Pages → Build and deployment → Source** den Eintrag **GitHub Actions**.
4. Pushe auf den Standardbranch. Falls du den Pages-Schalter erst nach dem Push umgestellt hast, starte unter **Actions → Adventskalender veröffentlichen → Run workflow** einen neuen Lauf.

Der Workflow veröffentlicht `index.html` und `fotos/` und lädt vom 1. bis 24. Dezember kurze Auszüge aus dem tagesaktuellen Löwe-Horoskop. Der erste geplante Lauf des Tages ist um 00:17 Uhr deutscher Zeit, weitere Läufe folgen im Tagesverlauf. GitHub kann geplante Läufe verzögern. Der Kalender zeigt die Vorschau ausschließlich bei übereinstimmendem Datum und verlinkt auf das vollständige Original. Falls die Quelle vorübergehend fehlt, bleiben das persönliche Horoskop und der Link im heutigen Türchen verfügbar.
