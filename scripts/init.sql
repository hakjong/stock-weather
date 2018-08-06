DROP DATABASE IF EXISTS stock_weather;
CREATE DATABASE stock_weather CHARACTER SET utf8 COLLATE utf8_general_ci;
USE stock_weather;

CREATE TABLE stock (
    id          INT             NOT NULL AUTO_INCREMENT,
    name        VARCHAR(128)    NOT NULL,
    keyword     VARCHAR(1024),
    PRIMARY KEY (id)
);

CREATE TABLE news (
    id          INT            NOT NULL AUTO_INCREMENT,
    title       VARCHAR(4096),
    title_ori  VARCHAR(4096),
    link        VARCHAR(2048),
    description VARCHAR(10240),
    pubdate     TIMESTAMP,
    hash        CHAR(32),
    sentiment   CHAR(3),
    fk_stock_id INT,
    UNIQUE (hash),
    PRIMARY KEY (id),
    FOREIGN KEY (fk_stock_id) REFERENCES stock(id)
);

INSERT INTO stock VALUES (NULL, '카카오', '카카오,카톡,카카오톡');
INSERT INTO stock VALUES (NULL, '네이버', '네이버,클로바');
INSERT INTO stock VALUES (NULL, '미래에셋대우', '미래에셋대우');

