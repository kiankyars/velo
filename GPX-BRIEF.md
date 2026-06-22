# Projet GPX — Boucle cyclable Europe 2026 (cahier des charges)

> **STATUT (2026-06-22)**
> Ce fichier est le cahier des charges autoritaire pour la génération GPX de la
> boucle Francfort↔Francfort 2026. Il **remplace/élargit** l'ancien « Frankfurt
> Loop » décrit dans `ITINERARY.md` (qui ne couvrait qu'une étape EV15).
>
> **Blocage actuel :** la politique réseau de la session où ce brief a été reçu
> est restrictive — les moteurs de routage (brouter, OpenRouteService, OSRM),
> le routage OpenStreetMap et les téléchargements GPX d'eurovelo.com sont
> bloqués (403). Conformément à la **section 8**, aucun GPX ne doit être
> fabriqué « de mémoire ». Pour produire de **vrais** GPX routables, lancer une
> nouvelle session dans un environnement réglé sur **Network access = Full**
> (ou Custom avec : `eurovelo.com`, `*.eurovelo.com`, `cycle.travel`,
> `api.openrouteservice.org`, `brouter.de`, `routing.openstreetmap.de`,
> `*.komoot.com`, `*.strava.com`).
>
> **Deux confirmations à obtenir avant l'export final :**
> 1. le **point GPS exact** où le vélo sera monté à Francfort (aéroport ? hôtel ?
>    magasin de vélo ?) — détermine le connecteur Francfort→Mayence ;
> 2. le **type de vélo / largeur des pneus** — détermine la tolérance au gravier
>    (Innradweg, plaine du Pô, Turchino) vs. routage 100 % asphalte.
>
> **Déjà disponible dans le repo (réutilisable) :** `gpx/ev15_mittelbuchen-mainz_to_karlsruhe.gpx`
> — tronçon EV15 réel Mayence→Karlsruhe (1 769 points avec altitude), à intégrer
> dans le module `01_Frankfurt_Andermatt.gpx`.

---

## 1. Objectif général

Créer un itinéraire cyclable continu, sûr et légal, partant de Francfort et
revenant au même endroit, dans le sens antihoraire.

* Départ : mardi 23 juin 2026.
* Arrivée de l'avion à Francfort vers 11 h ; départ cyclable probable vers 13 h–14 h.
* Fin souhaitée : dimanche 12 juillet.
* Le 13 juillet est une journée de secours, mais constitue la date limite.
* Objectif : environ 4 000 km pédalés en 20 jours, soit environ 200 km/jour.
* Le total peut raisonnablement varier ; ne pas ajouter des détours absurdes uniquement pour atteindre exactement 4 000 km.
* Aucun jour de repos planifié.
* Le premier jour est plus court à cause de l'arrivée en avion.
* Les étapes alpines peuvent être plus courtes ; les journées plates peuvent atteindre 230–260 km.
* L'utilisateur est déjà adapté au fuseau horaire européen et peut partir vers 4 h 30–5 h les jours suivants.
* Hébergements réservés tardivement : choisir des fins d'étape dans des villes ayant plusieurs hôtels, auberges ou chambres disponibles.
* Les mentions antérieures d'« autoroute 7 » ou « autoroute 6 » signifiaient EuroVelo 7 et EuroVelo 6. Ne jamais emprunter une véritable autoroute.

## 2. Itinéraire directeur obligatoire

### A. Francfort → Mayence
Créer une liaison cyclable légale entre le point de départ exact à Francfort et Mainz/Mayence.
Si le départ est à l'aéroport de Francfort, éviter absolument les bretelles des A3, A5 et autres voies rapides. Utiliser un corridor cyclable sûr vers Rüsselsheim/Mainz.

### B. Mayence → Andermatt : EuroVelo 15 vers le sud
Suivre aussi fidèlement que possible l'EuroVelo 15 / Route du Rhin, en remontant le Rhin :
Mainz → Worms → Mannheim/Ludwigshafen → Speyer → Karlsruhe → Strasbourg/Kehl → Basel → Schaffhausen → Stein am Rhein/Lac de Constance → Rorschach → vallée du Rhin alpin → Chur/Coire → Disentis → col de l'Oberalp → Andermatt.
L'EV15 officielle représente environ 415 km entre Mayence et Bâle et environ 429 km entre Bâle et Andermatt.

### C. Andermatt → Beaucaire/Tarascon : EuroVelo 17
À Andermatt, quitter l'EV15 et commencer l'EuroVelo 17 / Route du Rhône :
Andermatt → Realp → col de la Furka → Oberwald → Brig/Brigue → Sion → Montreux/Lausanne → Genève → Seyssel → Lyon → Vienne → Valence → Montélimar → Beaucaire/Tarascon.
Andermatt est bien le point de départ commun de l'EV17 ; la route suit ensuite le Rhône vers la Méditerranée.
Ne pas continuer jusqu'au terminus méditerranéen occidental de l'EV17 : effectuer la transition vers l'EV8 à Beaucaire/Tarascon.

### D. Beaucaire → Vintimille : EuroVelo 8 vers l'est
Suivre l'EuroVelo 8 / La Méditerranée à vélo :
Beaucaire/Tarascon → Saint-Rémy-de-Provence → Cavaillon → Apt → Céreste → Manosque.
À Manosque, ne pas incorporer de train dans le GPX. L'itinéraire officiel comporte encore une discontinuité entre Manosque et Meyrargues ; utiliser plutôt l'alternative routière :
Manosque → Gréoux-les-Bains → Saint-Julien-le-Montagnier → La Verdière → Varages → Barjols → Sillans-la-Cascade → Salernes → Lorgues → Flayosc → Draguignan.
Cette alternative Manosque–Varages est destinée aux cyclistes expérimentés et demande une vérification attentive du trafic et des pentes.
Continuer ensuite : Draguignan → Cannes → Nice → Menton → Vintimille/Ventimiglia.

### E. Vintimille → Plaisance sans train
Ne pas remonter la vallée de la Roya comme si elle constituait une EV8 aménagée. La section près de Vintimille est officiellement signalée comme non développée et le train est normalement recommandé.
Pour créer une variante entièrement pédalée, utiliser :
Ventimiglia → Sanremo → Imperia → Albenga → Savona → Arenzano/Voltri → Passo del Turchino → Ovada → Tortona → Piacenza/Plaisance.
Règles particulières :
* utiliser les pistes de l'ancienne voie ferrée et les véloroutes côtières lorsqu'elles existent ;
* inspecter chaque tunnel ;
* ne jamais utiliser l'autostrada ;
* ne pas emprunter un tunnel interdit aux vélos ;
* préférer une petite route parallèle à la SS1/Aurelia lorsqu'elle est nettement plus sûre ;
* maintenir une variante de secours ferroviaire séparée, sans l'intégrer à l'itinéraire principal.

### F. Plaisance → Bolzano
Rejoindre l'axe du Pô et l'EV7 :
Piacenza → Cremona → Mantova/Mantoue → Peschiera del Garda → Verona → Trento → Bolzano.
Utiliser de préférence les sections EV8/Bicitalia dans la plaine du Pô, puis l'axe cyclable de l'Adige vers Vérone, Trente et Bolzano.

### G. Bolzano → Passau sans le train de Mallnitz
Ne pas continuer vers Mallnitz–Böckstein, car cette option nécessite normalement une liaison ferroviaire à travers les Tauern.
Quitter ce corridor et utiliser :
Bolzano → Bressanone/Brixen → Vipiteno/Sterzing → col du Brenner → Innsbruck → Kufstein → Rosenheim → Wasserburg → Mühldorf → Braunau → Schärding → Passau.
Le corridor cyclable Bolzano–Brenner est une véloroute balisée d'environ 96–103 km ; l'Innradweg relie ensuite le Tyrol à Passau.
Lorsque l'Innradweg comporte du gravier médiocre, proposer une variante asphaltée parallèle et légale.

### H. Passau → Francfort
Suivre : Passau → Regensburg, principalement le long du Danube/EV6.
Puis quitter l'EV6, qui continuerait trop loin vers l'ouest, et choisir un corridor direct et cyclable :
Regensburg → Nürnberg/Nuremberg → Würzburg → Aschaffenburg → Frankfurt.
À partir de Würzburg, privilégier le Main-Radweg ou des variantes asphaltées proches du Main jusqu'à Francfort.

## 3. Principes de routage

L'itinéraire principal doit être :
* entièrement pédalable, sans train ;
* continu, sans lignes droites artificielles ;
* légal pour les vélos ;
* exempt d'autoroutes et de voies express interdites ;
* sans escaliers, sentiers de randonnée ou sections de VTT technique ;
* principalement asphalté ;
* compatible avec un vélo chargé ;
* sur gravier compact uniquement lorsque cela apporte un avantage important et que le vélo le permet ;
* aussi fidèle que raisonnablement possible aux EuroVelo officielles ;
* suffisamment direct pour maintenir une moyenne proche de 200 km/jour.

Ne pas laisser un moteur de routage raccourcir automatiquement une EuroVelo en envoyant le cycliste sur une route dangereuse. Utiliser les GPX officiels comme colonne vertébrale et ajouter manuellement les connecteurs.

Pour chaque section non officielle, vérifier :
* classification de la route ;
* interdictions cyclistes ;
* surface ;
* tunnels ;
* trafic probable ;
* fermeture actuelle ;
* ponts et traversées réellement ouverts.

## 4. Passages alpins et restrictions connues

Les deux passages suisses sont des cols routiers, pas des frontières :
* Oberalp : 2 044 m, entre Disentis et Andermatt ;
* Furka : 2 429 m, entre Realp et Oberwald.

Restrictions actuellement annoncées :
* Oberalp : fermeture le 26 juin de 17 h à 18 h ;
* Furka : fermeture le 27 juin de 7 h 30 à 8 h 45.

Il faut simplement prévoir un point d'attente sûr ; ne pas inventer un détour sur un chemin de montagne. Vérifier de nouveau l'état des cols le matin même.

## 5. Répartition provisoire des 20 jours

Ces zones servent à répartir la charge. L'agent doit recalculer les distances et le dénivelé réels avant de fixer les villes exactes.

| Jour | Date | Zone d'arrivée visée |
|---|---|---|
| 1 | 23 juin | Speyer ; Karlsruhe seulement comme objectif extensible |
| 2 | 24 juin | Strasbourg, Breisach ou Freiburg |
| 3 | 25 juin | Bâle, Schaffhouse ou secteur du lac de Constance |
| 4 | 26 juin | Rorschach, Coire ou Disentis |
| 5 | 27 juin | Andermatt, Furka, Brigue ou Sion selon l'avancement |
| 6 | 28 juin | Genève ou Seyssel |
| 7 | 29 juin | Lyon ou Vienne |
| 8 | 30 juin | Valence ou Montélimar |
| 9 | 1er juillet | Beaucaire, Cavaillon ou Apt |
| 10 | 2 juillet | Manosque, Varages ou Draguignan |
| 11 | 3 juillet | Nice, Menton ou Vintimille |
| 12 | 4 juillet | Savone ou Arenzano |
| 13 | 5 juillet | Ovada, Tortona ou Plaisance |
| 14 | 6 juillet | Crémone, Mantoue ou Peschiera |
| 15 | 7 juillet | Vérone, Trente ou Bolzano |
| 16 | 8 juillet | Brenner, Innsbruck ou Kufstein |
| 17 | 9 juillet | Wasserburg, Mühldorf ou Braunau |
| 18 | 10 juillet | Passau ou Regensburg |
| 19 | 11 juillet | Nuremberg ou Würzburg |
| 20 | 12 juillet | Francfort |

Produire également une version de secours de 21 jours :
* 10 juillet : Passau ;
* 11 juillet : Regensburg/Nuremberg ;
* 12 juillet : Würzburg ;
* 13 juillet : Francfort.

## 6. Fichiers demandés

**Route maîtresse** — `00_MASTER_Frankfurt_Frankfurt_CCW.gpx` : une seule trace continue représentant la boucle complète.

**Grands modules régionaux** — environ huit fichiers de 350 à 650 km, avec environ 10–20 km de chevauchement :
1. `01_Frankfurt_Andermatt.gpx`
2. `02_Andermatt_Geneva.gpx`
3. `03_Geneva_Beaucaire.gpx`
4. `04_Beaucaire_Ventimiglia.gpx`
5. `05_Ventimiglia_Piacenza.gpx`
6. `06_Piacenza_Bolzano.gpx`
7. `07_Bolzano_Passau.gpx`
8. `08_Passau_Frankfurt.gpx`

**Étapes quotidiennes** — 20 fichiers provisoires :
`D01_2026-06-23_[départ]_[arrivée].gpx` … `D20_2026-07-12_[départ]_Frankfurt.gpx`
Les trois premiers doivent être particulièrement vérifiés et immédiatement utilisables. Les étapes suivantes sont provisoires et devront pouvoir être redécoupées chaque soir à partir de la position réelle.

**Tableau récapitulatif** — pour chaque fichier, fournir : départ et arrivée ; distance ; dénivelé positif et négatif ; altitude maximale ; pourcentage asphalté/gravier/inconnu ; principales montées ; sections potentiellement délicates ; villes de repli vers 120, 160 et 200 km ; gares servant uniquement de secours ; villes comportant plusieurs hébergements ; heure de départ conseillée.

## 7. Format technique

* GPX 1.1 ;
* coordonnées WGS84 ;
* encodage UTF-8 ;
* une seule balise `<trk>` par fichier ;
* une seule trace continue, sauf obstacle réellement impossible ;
* inclure l'altitude `<ele>` lorsqu'elle est disponible ;
* ne pas créer une trace ferroviaire ou une ligne droite traversant un obstacle ;
* noms courts et lisibles dans Polar Flow ;
* garder chaque fichier nettement sous 25 MB (Polar Flow : limite 25 MB par fichier, GPX ou TCX).

## 8. Validation obligatoire

**Ne pas générer les coordonnées de mémoire.** L'agent doit utiliser un véritable
moteur de routage cyclable, les données OpenStreetMap et les traces officielles
disponibles. **S'il n'a pas accès à ces outils, il doit produire une liste de
points de passage plutôt qu'un faux GPX.**

Avant livraison :
1. valider le XML de chaque GPX ;
2. vérifier que chaque trace est continue ;
3. chercher les autoroutes, voies interdites, escaliers, tunnels et ferries ;
4. vérifier les surfaces inconnues ;
5. recalculer le total réel ;
6. signaler toute journée dépassant 250 km ou présentant un dénivelé exceptionnel ;
7. proposer un rééquilibrage plutôt que de prétendre que chaque journée fait exactement 200 km ;
8. fournir une carte ou un aperçu visuel de la route complète.

> **Point essentiel :** construire une trace à partir de données routables réelles,
> et non transformer cette liste de villes en coordonnées approximatives.
