-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS prog;

CREATE TABLE prog (
    id TEXT PRIMARY KEY,
    station TEXT NOT NULL,
    ft TEXT,
    tt TEXT,
    title TEXT,
    pfm TEXT
);

CREATE INDEX stationindex ON prog(station);
CREATE INDEX ftindex ON prog(ft);
CREATE INDEX ttindex ON prog(tt);
