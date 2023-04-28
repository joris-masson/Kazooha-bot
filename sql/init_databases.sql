CREATE DATABASE IF NOT EXISTS Kazooha;
SET NAMES utf8mb4;
ALTER DATABASE Kazooha CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS Kazooha.Messages (
    id BIGINT NOT NULL PRIMARY KEY,
    guildId BIGINT NOT NULL,
    guildName VARCHAR(100) NOT NULL,
    channelId BIGINT NOT NULL,
    channelName VARCHAR(100) NOT NULL,
    authorId BIGINT NOT NULL,
    authorName VARCHAR(100) NOT NULL,
    sentTime TIMESTAMP NOT NULL,
    content VARCHAR(4000) NOT NULL,
    modified BOOLEAN,
    deleted BOOLEAN
);

DROP TABLE Kazooha.GameUid;
CREATE TABLE IF NOT EXISTS Kazooha.GameUid (
    discordId BIGINT NOT NULL,
    game VARCHAR(100) NOT NULL,
    server VARCHAR(100),
    uid BIGINT NOT NULL PRIMARY KEY
);
