CREATE DATABASE backup;
\c backup;
DROP DATABASE IF EXISTS fictional;
CREATE DATABASE fictional;
\c fictional;

CREATE TABLE movies (
    id int,
    name VARCHAR(50) NOT NULL,
    grossing VARCHAR(12),
    PRIMARY KEY (id)
);

INSERT INTO movies VALUES (1, 'Youth in Revolt', '$19.62');
INSERT INTO movies VALUES (2, 'You Will Meet a Tall Dark Stranger', '$26.66');
INSERT INTO movies VALUES (3, 'When in Rome', '$43.04');
INSERT INTO movies VALUES (4, 'What Happens in Vegas', '$219.37');
INSERT INTO movies VALUES (5, 'Water For Elephants', '$117.09');
INSERT INTO movies VALUES (6, 'WALL-E', '$521.28');
INSERT INTO movies VALUES (7, 'Waitress', '$22.18');
INSERT INTO movies VALUES (8, 'Waiting For Forever', '$0.03');
INSERT INTO movies VALUES (9, 'Twilight: Breaking Dawn', '$702.17');
INSERT INTO movies VALUES (10, 'Twilight', '$376.66');
INSERT INTO movies VALUES (11, 'The Ugly Truth', '$205.30');
INSERT INTO movies VALUES (12, 'The Twilight Saga: New Moon', '$709.82');
INSERT INTO movies VALUES (13, 'The Proposal', '$314.70');
INSERT INTO movies VALUES (14, 'The Invention of Lying', '$32.40');
INSERT INTO movies VALUES (15, 'The Heartbreak Kid', '$127.77');
INSERT INTO movies VALUES (16, 'The Duchess', '$43.31');
INSERT INTO movies VALUES (17, 'The Curious Case of Benjamin Button', '$285.43');
INSERT INTO movies VALUES (18, 'The Back-up Plan', '$77.09');
INSERT INTO movies VALUES (19, 'Tangled', '$355.01');
INSERT INTO movies VALUES (20, 'Something Borrowed', '$60.18');


CREATE TABLE cash_moneys_logbook (
    indebtor_name VARCHAR(32) PRIMARY KEY,
    indebtor_owed VARCHAR(255)
);

INSERT INTO cash_moneys_logbook
VALUES
    ('ramen', '$5251'),
    ('honeycomb', '$1000'),
    ('frankie', '$663'),
    ('cavins', '$722'),
    ('triangle doritos', '$819');


INSERT INTO cash_moneys_logbook
VALUES 
  ('SecSoc', 'SKYLIGHT{I75_NO7_S3Qu3l_1Ts_$-Q-L_f1tE_M3}');

select * from movies;
select * from cash_moneys_logbook;