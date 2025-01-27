
#### Database Definition 
[oracle site: https://www.oracle.com/database/what-is-database/]:
A database is an organized collection of structured information, or data, typically stored electronically in a computer system. A database is usually controlled by a database management system (DBMS). Together, the data and the DBMS, along with the applications that are associated with them, are referred to as a database system, often shortened to just database.

The file : docker-compose.yaml
```
version: '3.8'
services:
  db:
    container_name: pg_container
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_USER: afa_user
      POSTGRES_PASSWORD: afa_password
      POSTGRES_DB: dst_db
    ports:
      - "5432:5432"
  pgadmin:
    container_name: pgadmin4_container
    image: dpage/pgadmin4
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: afa@gmail.com
      PGADMIN_DEFAULT_PASSWORD: afa_data_engineer
    ports:
      - "5050:80"

```
To improve the docker-compose file, let's move sensitive information into an environment file _.env_.

```
POSTGRES_USER=afa_user
POSTGRES_PASSWORD=afa_password
POSTGRES_DB=dst_db
PGADMIN_DEFAULT_EMAIL=afa@gmail.com
PGADMIN_DEFAULT_PASSWORD=afa_data_engineer
```
The best practice is to hide the _.env_ file by adding it to the _.gitignore_ file, while creating a _.env.example_ file that will serves as documentation. This file should have the same structure as the _.env_ file but without real values as follows :

```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db_name
PGADMIN_DEFAULT_EMAIL=your_email
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
```

Then we modify the docker-compose.yml to use these environment variables:

```
version: '3.8'
services:
  db:
    container_name: pg_container
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
  pgadmin:
    container_name: pgadmin4_container
    image: dpage/pgadmin4
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "5050:80"
```
To run the docker-compose file : 
```
docker-compose up -d
```
to check the running containers : 
```
docker ps
``` 

figure

We see that we have two running containers, named *_pg_container_* and  *_pgadmin4_container_*, respectively.

To access the container and run bash commands :
```
docker exec -it pg_container bash
```

To create the database : 

```
createdb -h localhost -U afa_user <db_name>
```

To connect to the DB :
```
psql -h localhost -U afa_user dst_db
```

to list the existing DB : 
```
\l
```
figure to place here.

To create a database : 
```
CREATE DATABASE <db_name>;
```

Considering the dataset for Anime that we present in the table bellows : 

<p align="center">
<img src="./figures/4.anime-dataset.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 4: Anime dataset
</p>

MERISE est une méthode de conception, de développement et de réalisation de projets informatiques.
La méthode MERISE est basée sur la séparation des données et des traitements à effectuer en plusieurs modèles conceptuels et physiques.

<p align="center">
<img src="./figures/5.en-summary-merise-methodology.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 5: steps of Merise methodology
</p>

Pour construire un MLD (Modèle Logique de Données) pour ce dataset d'animes et justiffier des changements effectués :

Le découpage proposé est justifié par les principes de normalisation, la séparation des préoccupations, la gestion des relations entre les entités, et l'extensibilité du modèle. Il permet de créer une base de données robuste, facile à maintenir et à faire évoluer. Le découpage proposé est justifié par les principes de normalisation, la séparation des préoccupations, la gestion des relations entre les entités, et l'extensibilité du modèle. Il permet de créer une base de données robuste, facile à maintenir et à faire évoluer. 
Le choix de découpage des tables et des entités dans un modèle de base de données repose sur les principes de normalisation et les bonnes pratiques de conception de bases de données relationnelles. Voici une justification détaillée pour chaque entité et table proposée :

1. Normalisation
La normalisation est un processus qui vise à éliminer la redondance des données et à organiser les données de manière cohérente. Voici comment elle s'applique ici :

Élimination des données redondantes
Dans la table initiale, les colonnes comme Genres, Producers, et Studios contiennent des listes de valeurs séparées par des virgules (par exemple, [Action, Adventure, Drama]). Cela viole la première forme normale (1NF), qui exige que chaque colonne contienne des valeurs atomiques (indivisibles).

En créant des tables séparées pour Genre, Producer, et Studio, nous respectons la 1NF et évitons la redondance.

Éviter les anomalies de mise à jour
Si les genres, producteurs ou studios étaient stockés directement dans la table Anime, toute modification (par exemple, changer le nom d'un studio) nécessiterait de mettre à jour plusieurs lignes. Cela pourrait entraîner des anomalies de mise à jour.

Avec des tables séparées, une modification ne doit être faite qu'à un seul endroit.

2. Séparation des préoccupations
Chaque table a une responsabilité claire et unique, ce qui améliore la maintenabilité et la lisibilité du modèle.

Anime : Stocke les informations de base sur un anime (nom, score, type, etc.).

Genre : Stocke les différents genres disponibles.

Producer : Stocke les producteurs.

Studio : Stocke les studios.

Aired : Stocke les informations de diffusion (dates de début et de fin).

Premiered : Stocke les informations de première diffusion (saison et année).

3. Relations entre les tables
Le découpage permet de définir des relations claires entre les tables, ce qui est essentiel pour une base de données relationnelle.

Relations 1-n :

Un anime peut avoir une seule diffusion (Aired) et une seule première diffusion (Premiered), mais une diffusion ou une première diffusion ne concerne qu'un seul anime. Cela justifie les relations 1-n entre Anime et Aired, et entre Anime et Premiered.

Relations n-n :

Un anime peut avoir plusieurs genres, et un genre peut être associé à plusieurs animes. De même, un anime peut avoir plusieurs producteurs/studios, et un producteur/studio peut être associé à plusieurs animes. Cela justifie l'utilisation de tables de liaison (Anime_Genre, Anime_Producer, Anime_Studio) pour gérer les relations n-n.

4. Extensibilité
Le découpage rend le modèle plus flexible et extensible.

Ajout de nouveaux genres, producteurs ou studios :

Si de nouveaux genres, producteurs ou studios sont ajoutés, il suffit d'insérer une nouvelle ligne dans la table correspondante sans modifier la structure de la base de données.

Ajout de nouvelles informations :

Si de nouvelles informations doivent être ajoutées (par exemple, des détails supplémentaires sur les studios), elles peuvent être ajoutées à la table concernée sans affecter les autres tables.

6. Avantages du découpage
Réduction de la redondance : Les données ne sont pas dupliquées.

Maintenabilité : Les modifications sont plus faciles à gérer.

Extensibilité : Le modèle peut évoluer sans nécessiter de refonte majeure.

Performance : Les requêtes peuvent être optimisées en fonction des besoins (par exemple, rechercher tous les animes d'un genre spécifique).


here is how to create tables and their relationships:

```
-- Table Anime
CREATE TABLE Anime (
    Anime_ID INT PRIMARY KEY,
    English_name VARCHAR(255) NOT NULL,
    Score FLOAT,
    Type VARCHAR(50),
    Episodes INT,
    Source VARCHAR(50),
    Duration VARCHAR(50),
    Rating VARCHAR(50),
    Ranked FLOAT,
    Popularity INT
);

-- Table Genre
CREATE TABLE Genre (
    Genre_ID INT PRIMARY KEY,
    Genre_name VARCHAR(50) NOT NULL
);

-- Table Producer
CREATE TABLE Producer (
    Producer_ID INT PRIMARY KEY,
    Producer_name VARCHAR(255) NOT NULL
);

-- Table Studio
CREATE TABLE Studio (
    Studio_ID INT PRIMARY KEY,
    Studio_name VARCHAR(255) NOT NULL
);

-- Table Aired
CREATE TABLE Aired (
    Aired_ID INT PRIMARY KEY,
    Anime_ID INT,
    Start_date DATE,
    End_date DATE,
    FOREIGN KEY (Anime_ID) REFERENCES Anime(Anime_ID)
);

-- Table Premiered
CREATE TABLE Premiered (
    Premiered_ID INT PRIMARY KEY,
    Anime_ID INT,
    Season VARCHAR(50),
    Year INT,
    FOREIGN KEY (Anime_ID) REFERENCES Anime(Anime_ID)
);

-- Table de liaison Anime_Genre
CREATE TABLE Anime_Genre (
    Anime_ID INT,
    Genre_ID INT,
    PRIMARY KEY (Anime_ID, Genre_ID),
    FOREIGN KEY (Anime_ID) REFERENCES Anime(Anime_ID),
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);

-- Table de liaison Anime_Producer
CREATE TABLE Anime_Producer (
    Anime_ID INT,
    Producer_ID INT,
    PRIMARY KEY (Anime_ID, Producer_ID),
    FOREIGN KEY (Anime_ID) REFERENCES Anime(Anime_ID),
    FOREIGN KEY (Producer_ID) REFERENCES Producer(Producer_ID)
);

-- Table de liaison Anime_Studio
CREATE TABLE Anime_Studio (
    Anime_ID INT,
    Studio_ID INT,
    PRIMARY KEY (Anime_ID, Studio_ID),
    FOREIGN KEY (Anime_ID) REFERENCES Anime(Anime_ID),
    FOREIGN KEY (Studio_ID) REFERENCES Studio(Studio_ID)
);
```

#### Structure des tables principales :

- anime : Table principale avec toutes les informations sur les animes
- genre : Catalogue des genres possibles
- producer : Liste des producteurs
- studio : Liste des studios d'animation


#### Tables de jonction :

- anime_genre : Lie les animes à leurs genres
- anime_producer : Lie les animes à leurs producteurs
- anime_studio : Lie les animes à leurs studios


#### Contraintes importantes :

Clés primaires sur toutes les tables
Clés étrangères pour maintenir l'intégrité référentielle
Contraintes UNIQUE sur les noms des genres, producteurs et studios
Cascade sur la suppression pour maintenir la cohérence des données


#### Optimisations :

Index créés sur les colonnes fréquemment recherchées
Types de données appropriés pour chaque colonne
SERIAL pour auto-incrémentation des IDs

### Requêtes d'insertions des données:

```
INSERT INTO Anime (Anime_ID, English_name, Score, Type, Episodes, Source, Duration, Rating, Ranked, Popularity)
VALUES
(1, 'Cowboy Bebop', 8.78, 'TV', 26, 'Original', '24 min. per ep.', 'R - 17+ (violence & profanity)', 28.0, 39),
(2, 'Cowboy Bebop: The Movie', 8.39, 'Movie', 1, 'Original', '1 hr. 55 min.', 'R - 17+ (violence & profanity)', 159.0, 518),
(3, 'Naruto', 7.91, 'TV', 220, 'Manga', '23 min. per ep.', 'PG-13 - Teens 13 or older', 660.0, 8),
(4, 'One Piece', 8.52, 'TV', NULL, 'Manga', '24 min.', 'PG-13 - Teens 13 or older', 95.0, 31),
(5, 'Mobile Suit Gundam SEED', 7.79, 'TV', 50, 'Original', '24 min. per ep.', 'R - 17+ (violence & profanity)', 850.0, 1057),
(6, 'Mobile Suit Gundam SEED Destiny', 7.22, 'TV', 50, 'Original', '24 min. per ep.', 'R - 17+ (violence & profanity)', 2687.0, 1530);
```

```
INSERT INTO Genre (Genre_ID, Genre_name)
VALUES
(1, 'Action'),
(2, 'Adventure'),
(3, 'Drama'),
(4, 'Sci-Fi'),
(5, 'Space'),
(6, 'Shounen'),
(7, 'Military');
```

```
INSERT INTO Producer (Producer_ID, Producer_name)
VALUES
(1, 'Bandai Visual'),
(2, 'Sunrise'),
(3, 'TV Tokyo'),
(4, 'Shueisha'),
(5, 'Fuji TV'),
(6, 'Sotsu'),
(7, 'Sony Music Entertainment'),
(8, 'Bones');
```

```
INSERT INTO Studio (Studio_ID, Studio_name)
VALUES
(1, 'Sunrise'),
(2, 'Bones'),
(3, 'Studio Pierrot'),
(4, 'Toei Animation');
```

```
INSERT INTO Aired (Aired_ID, Anime_ID, Start_date, End_date)
VALUES
(1, 1, '1998-04-03', '1999-04-24'),
(2, 2, '2001-09-01', NULL),
(3, 3, '2002-10-03', '2007-02-08'),
(4, 4, '1999-10-20', NULL),
(5, 5, '2002-10-05', '2003-09-27'),
(6, 6, '2004-10-09', '2005-10-01');
```

```
INSERT INTO Premiered (Premiered_ID, Anime_ID, Season, Year)
VALUES
(1, 1, 'Spring', 1998),
(2, 2, NULL, NULL),
(3, 3, 'Fall', 2002),
(4, 4, 'Fall', 1999),
(5, 5, 'Fall', 2002),
(6, 6, 'Fall', 2004);
```

```
INSERT INTO Anime_Genre (Anime_ID, Genre_ID)
VALUES
-- Cowboy Bebop
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
-- Cowboy Bebop: The Movie
(2, 1), (2, 3), (2, 4), (2, 5),
-- Naruto
(3, 1), (3, 2), (3, 6),
-- One Piece
(4, 1), (4, 2), (4, 6),
-- Mobile Suit Gundam SEED
(5, 1), (5, 3), (5, 7), (5, 4), (5, 5),
-- Mobile Suit Gundam SEED Destiny
(6, 1), (6, 3), (6, 7), (6, 4), (6, 5);
```

```
INSERT INTO Anime_Producer (Anime_ID, Producer_ID)
VALUES
-- Cowboy Bebop
(1, 1),
-- Cowboy Bebop: The Movie
(2, 1), (2, 2),
-- Naruto
(3, 3), (3, 4),
-- One Piece
(4, 5), (4, 4),
-- Mobile Suit Gundam SEED
(5, 6), (5, 7),
-- Mobile Suit Gundam SEED Destiny
(6, 6), (6, 7);
```

```
INSERT INTO Anime_Studio (Anime_ID, Studio_ID)
VALUES
-- Cowboy Bebop
(1, 1),
-- Cowboy Bebop: The Movie
(2, 2),
-- Naruto
(3, 3),
-- One Piece
(4, 4),
-- Mobile Suit Gundam SEED
(5, 1),
-- Mobile Suit Gundam SEED Destiny
(6, 1);
```

To show list of tables 
```
\dt
```
<p align="center">
<img src="./figures/6.list-of-tables.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 6: List of tables
</p>


To show details of a table 
```
\d+ <table_name>
```

<p align="center">
<img src="./figures/7.details-of-table-anime.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 7: Details of table Anime
</p>

To insert data from a file, create first a file named insert-data.sql, whithin the our container, that contains all insertions code above, then run the following command
```
\i /path/to/insert_anime.sql
```

<p align="center">
<img src="./figures/8.insert_data_from_file.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 8: output when running the script that inserts data in tables
</p>

### Part II

Download data using this command :

```
cd && wget https://dst-de.s3.eu-west-3.amazonaws.com/bdd_postgres_fr/database/examen.sql
```
We create a database called _examen\_afa_

```
docker exec -i pg_container psql -U afa_user -d postgres -c "CREATE DATABASE examen_afa;"
```
To check that the database was created by listing all databases : 

```
docker exec -i pg_container psql -U afa_user -d postgres -c "\l"
``` 

<p align="center">
<img src="./figures/9.listing-the-existing-databases.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 9: listing the existing databases
</p>

To execute the SQL script on a specified database that is inside a running Docker container, run this command:


```
docker exec -i <container-name> psql -U <user-name> -d <db_name> < <path-to/script-sql>
```

```
docker exec -i pg_container psql -U afa_user -d exam_afa < ./data/examen.sql
```

To display the tables created whithin the database _examen\_afa_, we run the command :

```
docker exec -i pg_container psql -U afa_user -d postgres -c "\dt"
```

<p align="center">
<img src="./figures/10.listing-the-tables_whithin-database.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 10: Display tables whithin the database examan_afa
</p>

#### SQL Requests:

For aim of clarity, we do not run the sql statement from outside the container by running this command:
```
docker exec -it pg_container psql -U afa_user -d examen_afa -c "SQL-statement"
```
However, we prefer connect to the database then after we run sql statements. 

This is the command to connect to the database _examen\_afa_

##### SQL Request 1



```
SELECT 
    t.name_type AS type, COUNT(pt.pokedex_number) AS count 
FROM 
    pokemontype pt JOIN pokemon p 
ON 
    pt.pokedex_number = p.pokedex_number 
JOIN 
    types t 
ON 
    pt.type_id = t.type_id 
GROUP
    BY type 
ORDER
    BY count DESC;
```
This query joins the three tables (pokemon, types and pokemontype) and groups the results by type.

<p align="center">
<img src="./figures/11.group-pokemon-by type.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 11: group pokemon by type and order them according to their number, decreasingly.
</p>


##### SQL Request 2
List pokemon names and base stat total grater than 600 in descending order. 

```
SELECT 
    p.name, p.base_total 
FROM 
    pokemon p 
WHERE 
    p.base_total > 600 
ORDER BY 
    base_total DESC;

```
<p align="center">
<img src="./figures/12.display-pokemon-name-and-base-total.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 12: Display pokemon name and base total with two conditions.
</p>

##### SQL Request 3
 To display the average base stats of Pokemon, grouped by their type, and sorts the results in ascending order according to the average:
```
SELECT 
    t.name_type AS type, 
    AVG(p.base_total)::NUMERIC AS average
FROM 
    pokemon p 
JOIN 
    pokemontype pt ON p.pokedex_number = pt.pokedex_number 
JOIN 
    types t ON t.type_id = pt.type_id 
GROUP BY 
    t.name_type 
ORDER BY 
    average;

```

<p align="center">
<img src="./figures/13.display-pokemon-type-and-avg-base-total.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 13: Display pokemon name and average base total with two conditions.
</p>

##### SQL Request 4

list Pokemons with the special ability 'Overgrow' and sort them by base stats in descending order

```
SELECT 
    p.name, 
    p.base_total 
FROM 
    pokemon p 
JOIN 
    pokemonability pa ON p.pokedex_number = pa.pokedex_number 
JOIN 
    abilities a ON a.ability_id = pa.ability_id 
WHERE 
    a.name_ability = 'Overgrow' 
ORDER BY 
    p.base_total DESC;
```

<p align="center">
<img src="./figures/14.display-pokemon-name-and-base-total-with-ability.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 14: Display pokemon with special ability in descending order according to base stats.
</p>

##### SQL Request 5

To list pokemon by their names and their primary and secondary types, we can group the pokemon by their names, and for each name, print the types by using conditional operations on _type\_id_ as shown through the following query:

```
SELECT 
    p.name,
    MAX(CASE WHEN pt.type_id = LEAST(pt.type_id, pt2.type_id) THEN t.name_type END) AS primary_type,
    MAX(CASE WHEN pt2.type_id IS NOT NULL AND pt.type_id = GREATEST(pt.type_id, pt2.type_id) THEN t.name_type END) AS secondary_type
FROM 
    pokemon p
JOIN 
    pokemontype pt ON p.pokedex_number = pt.pokedex_number
JOIN 
    types t ON t.type_id = pt.type_id
LEFT JOIN 
    pokemontype pt2 ON p.pokedex_number = pt2.pokedex_number AND pt.type_id != pt2.type_id
GROUP BY 
    p.name
ORDER BY 
    p.name;
```
<p align="center">
<img src="./figures/15.display-pokemon-names-and-types.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 15: Display pokemon names and their primary and secondary types.
</p>

##### SQL Request 6
```
SELECT 
    p.name,
    p.generation,
    p.base_total AS total_stats
FROM 
    pokemon p
WHERE 
    p.base_total > (
        SELECT 
            AVG(p2.base_total)
        FROM 
            pokemon p2
        WHERE 
            p2.generation = p.generation
    );
```

To display Pokemon with a _base\_total_ greater than the average _base\_total_ per generation:

<p align="center">
<img src="./figures/16.display-pokemon-when-base-total-greater-then-the-average-per-generation.png" width=80%>
</p>
<p align="center" style="font-weight: bold;">
Figure 16: Display pokemon when base_total is greater the the average base_total per generation.
</p>

##### SQL Request 7

To find pokemon of type "fire" with attack greater than 100 :

```
SELECT 
    p.name, 
    s.attack 
FROM 
    pokemon p
JOIN 
    stats s 
    ON p.pokedex_number = s.pokedex_number
JOIN 
    pokemontype pt 
    ON p.pokedex_number = pt.pokedex_number
JOIN 
    types t 
    ON t.type_id = pt.type_id
WHERE 
    t.name_type = 'fire' 
    AND s.attack > 100;
```

<p align="center">
<img src="./figures/17.display-pokemon-when-type-is-fire-and-attack-greater-then-100.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 17: Display pokemon the type is 'fire' and the attack is greater than 100.
</p>

##### SQL Request 8

```
SELECT 
    p.name,
    p.generation,
    p.base_total,
    CASE
        WHEN p.base_total > (
            SELECT AVG(p2.base_total)
            FROM pokemon p2
            WHERE p2.generation = p.generation
        ) THEN 'greater than the average'
        ELSE 'less or equal to the average'
    END AS total_stats_comparison
FROM 
    pokemon p;
```

<p align="center">
<img src="./figures/18.display-pokemon-with-new-column.png" width=80%>
</p>
<p align="center" style="font-weight: bold;">
Figure 18: Display pokemon with new column.
</p>

### Part III

In our docker there is no python installed, so we start by installing python3 on the alpine distribution.

we copy the script python in the container using this command: 
```
docker cp ./run-queries-python.py pg_container:/home

docker cp ./queries.txt pg_container:/home
```
to cpnnect to the container 
```
docker exec -it pg_container sh
```
install python 3 and the needed dependency : 
```
apk add --no-cache python3

apk add --no-cache py3-psycopg2
```
exit the contaner

```
docker exec -it pg_container python3 /home/run-queries-and-save-result-python.py
```

<p align="center">
<img src="./figures/19.the-output-executed-python.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 19: The output of the executed python command.
</p>

first create the backup inside the container, in a directory that the PostgreSQL user has write access to
```
docker exec -it pg_container pg_dump -U afa_user examen_afa -f /tmp/examen_afa.sql
```

docker cp pg_container:/tmp/examen_afa.sql .

<p align="center">
<img src="./figures/20.the-output-when-copying-backup.png" width=100%>
</p>
<p align="center" style="font-weight: bold;">
Figure 20: The output when copying the backup on local.
</p>




