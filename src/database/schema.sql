
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

CREATE TABLE IF NOT EXISTS tags_recources
(
    tag_id INTEGER,
    resource_id INTEGER,
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    FOREIGN KEY (resource_id) REFERENCES resources(id));