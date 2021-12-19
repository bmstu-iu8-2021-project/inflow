
CREATE TABLE IF NOT EXISTS tags
(
    id      SERIAL PRIMARY KEY,
    label   VARCHAR(96),
    color   VARCHAR(7)
);

CREATE TABLE IF NOT EXISTS resources
(
    id      BIGSERIAL PRIMARY KEY,
    title   VARCHAR(256),
    link    TEXT
);

CREATE TABLE IF NOT EXISTS users
(
    id      BIGSERIAL PRIMARY KEY,
    login   VARCHAR(256),
    password    TEXT
);

CREATE TABLE IF NOT EXISTS tags_resources
(
    tag_id INTEGER,
    resource_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    FOREIGN KEY (resource_id) REFERENCES resources(id)
);
