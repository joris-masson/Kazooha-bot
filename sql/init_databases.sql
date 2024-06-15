CREATE DATABASE IF NOT EXISTS Kazooha;
SET NAMES utf8mb4;
ALTER DATABASE Kazooha CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

# DROP TABLE IF EXISTS Kazooha.GameUid;
CREATE TABLE IF NOT EXISTS Kazooha.GameUid
(
    discordId BIGINT       NOT NULL,
    game      VARCHAR(100) NOT NULL,
    server    VARCHAR(100),
    uid       BIGINT       NOT NULL PRIMARY KEY,
    nickname  VARCHAR(255),
    level     INT
);

# DROP TABLE IF EXISTS Kazooha.Character;
CREATE TABLE IF NOT EXISTS Kazooha.Character
(
    id            INT(20)     NOT NULL PRIMARY KEY,
    name          VARCHAR(50) NOT NULL,
    rarity        INT(1)      NOT NULL,
    element       VARCHAR(25) NOT NULL,
    weapon        VARCHAR(25) NOT NULL,
    birthday      VARCHAR(25) NOT NULL,
    constellation VARCHAR(50) NOT NULL,
    affiliation   VARCHAR(100),
    description   VARCHAR(500),
    region        VARCHAR(25) NOT NULL,
    material      VARCHAR(50) NOT NULL,
    beta          BOOLEAN     NOT NULL DEFAULT 1
);

# DROP TABLE IF EXISTS Kazooha.Weapon;
CREATE TABLE IF NOT EXISTS Kazooha.Weapon
(
    id INT(20) NOT NULL PRIMARY KEY,
    name        VARCHAR(50)  NOT NULL,
    rarity      INT(1)       NOT NULL,
    type        VARCHAR(25)  NOT NULL,
    description VARCHAR(500) NOT NULL,
    story       LONGTEXT     NOT NULL,
    material    VARCHAR(50)  NOT NULL,
    beta        BOOLEAN      NOT NULL DEFAULT 1
);

# DROP TABLE IF EXISTS Kazooha.Material;
CREATE TABLE IF NOT EXISTS Kazooha.Material
(
    name    VARCHAR(50) NOT NULL PRIMARY KEY,
    utility VARCHAR(20) NOT NULL,
    region  VARCHAR(25) NOT NULL,
    day     VARCHAR(25)
);

DROP TABLE IF EXISTS Kazooha.Leak;
CREATE TABLE IF NOT EXISTS Kazooha.Leak
(
    id VARCHAR(20) NOT NULL PRIMARY KEY,
    timestamp INT(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    link VARCHAR(50) NOT NULL,
    author_name VARCHAR(50) NOT NULL,
    media_link VARCHAR(300),
    sent BOOLEAN NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS Kazooha.MessageIA;
CREATE TABLE IF NOT EXISTS Kazooha.MessageIa(
    id INT NOT NULL PRIMARY KEY,
    discordUserId BIGINT NOT NULL,
    messageNumber INT NOT NULL,
    sender VARCHAR(20),
    content VARCHAR(1024)
);
