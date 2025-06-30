-- enable vector indexing at the cluster level (assumes CRDB version 25.2 or higher)
SET CLUSTER SETTING feature.vector_index.enabled = true;

-- create our vb (vector battleship) database:
CREATE DATABASE IF NOT EXISTS vb;

-- switch to using the vb database:
USE vb;

-- dropping tables may be useful if you want to clean up:
drop table IF EXISTS vb.battleship;

-- look at what tables exist in your database:
SHOW tables;

-- create the battleship table:  note the use of the vector embedding for coordinates
-- the Vector index has a prefix (quadrant) to limit the scope of the Vector search work
CREATE TABLE IF NOT EXISTS vb.battleship(
   pk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
   battleship_class CHAR(20) NOT NULL DEFAULT 'destroyer' CHECK (battleship_class in ('aircraft_carrier', 'skiff','destroyer','submarine')),
   quadrant SMALLINT NOT NULL DEFAULT 2 CHECK (quadrant BETWEEN 1 AND 4),
   anchorpoint SMALLINT NOT NULL DEFAULT 23 CHECK (anchorpoint BETWEEN 1 AND 48),
   coordinates_embedding VECTOR(100),
   VECTOR INDEX (quadrant, coordinates_embedding)
);

-- add some initial data to establish the ships in various quadrants
INSERT into battleship (battleship_class,quadrant,anchorpoint) values ('submarine',1,43);
INSERT into battleship (battleship_class,quadrant,anchorpoint) values ('submarine',1,27);
INSERT into battleship (battleship_class,quadrant,anchorpoint) values ('aircraft_carrier',1,32);

UPDATE battleship SET coordinates_embedding ='[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]' WHERE anchorpoint=43;
UPDATE battleship SET coordinates_embedding ='[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]' WHERE anchorpoint=27;

UPDATE battleship SET coordinates_embedding='[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]' WHERE anchorpoint=32;

-- some useful calculations: (the larger the number the greater the euclidian distance)
-- <= 0.33 filters is roughly ~75%+ similarity or better
-- <= 1 filters to ~50%+ similarity or better
-- <= 4 corresponds to ~20% match or higher
-- filter on percentage match option: 
-- ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100, 2) >= 75

-- sample vector query in CRDB: (for above battleship no match due to quadrant mismatch)
WITH target_vector AS (SELECT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "v"
)
SELECT battleship_class, pk, anchorpoint,
ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100, 2) AS "Percent Match"
FROM battleship, target_vector 
WHERE quadrant = 1
  AND (coordinates_embedding <-> v)  <= 4
ORDER BY "Percent Match" DESC
LIMIT 2;

-- sample vector query in CRDB: (match due to quadrant accuracy & near vector)
WITH target_vector AS (SELECT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "v"
)
SELECT battleship_class, pk, anchorpoint,
ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100,
    2
  ) AS "Percent Match"
FROM battleship, target_vector 
WHERE quadrant = 1
  AND (coordinates_embedding <-> v)  <= 4
ORDER BY "Percent Match" DESC
LIMIT 2;

-- Exact match: Aircraft Carrier
EXPLAIN ANALYZE 
WITH target_vector AS (SELECT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "v"
)
SELECT battleship_class, pk, anchorpoint,
ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100,
    2
  ) AS "Percent Match"
FROM battleship, target_vector 
WHERE quadrant = 1
  AND (coordinates_embedding <-> v)  <= 4
ORDER BY "Percent Match" DESC
LIMIT 2;

-- miss
WITH target_vector AS (SELECT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "v"
)
SELECT battleship_class, pk, anchorpoint,
ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100,
    2
  ) AS "Percent Match"
FROM battleship, target_vector 
WHERE quadrant = 1
  AND (coordinates_embedding <-> v)  <= 3
ORDER BY "Percent Match" DESC
LIMIT 2;

-- non-exact hit?
WITH target_vector AS (SELECT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "v"
)
SELECT battleship_class, pk, anchorpoint,
ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100,
    2
  ) AS "Percent Match"
FROM battleship, target_vector 
WHERE quadrant = 1
  AND (coordinates_embedding <-> v)  <= 4
ORDER BY "Percent Match" DESC
LIMIT 2;

-- generous hit!
WITH target_vector AS (SELECT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "v"
)
SELECT battleship_class, pk, anchorpoint,
ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100,
    2
  ) AS "Percent Match"
FROM battleship, target_vector 
WHERE quadrant = 1
  AND (coordinates_embedding <-> v)  <= 4
ORDER BY "Percent Match" DESC
LIMIT 2;

-- anchorpoint of 12 used when generating vector for filter
explain 
WITH target_vector AS (SELECT  '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "v"
)
SELECT
  battleship_class,
  pk,
  anchorpoint,
  ROUND((1 / (1 + (coordinates_embedding <-> v))) * 100,
    2
  ) AS "Percent Match"
FROM battleship, target_vector 
WHERE quadrant = 1
  AND (coordinates_embedding <-> v)  <= 4
ORDER BY "Percent Match" DESC
LIMIT 2;


WITH target_vector AS (SELECT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::vector AS "target"
)
SELECT
  'DESIGNED TO MISS' as "tv.target DESIGNED TO MISS",
  bs.battleship_class,
  bs.pk,
  bs.anchorpoint,
  ROUND((1 / (1 + (bs.coordinates_embedding <-> tv.target ))) * 100,
    2
  ) AS "Percent Match"
FROM battleship bs, target_vector tv
WHERE quadrant = 1
  AND (bs.coordinates_embedding <-> tv.target )  <= 3
ORDER BY "Percent Match" DESC
LIMIT 2;