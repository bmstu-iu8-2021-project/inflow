
CREATE TABLE IF NOT EXISTS tags
(
    id      SERIAL PRIMARY KEY,
    label   VARCHAR(96),
    color   VARCHAR(6)
);

CREATE TABLE IF NOT EXISTS resources
(
    id      BIGSERIAL PRIMARY KEY,
    label   VARCHAR(256),
    link    TEXT
);

