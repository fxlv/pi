CREATE TABLE "temperature" (
    `id`    INTEGER NOT NULL,
    `source_name`   VARCHAR(200),
    `temperature`   FLOAT,
    `insert_time`   TIMESTAMP,
    `success`   BOOLEAN,
    PRIMARY KEY(id)
);
