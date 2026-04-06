DROP DATABASE IF EXISTS memo_app;
CREATE DATABASE memo_app;
USE memo_app;

CREATE TABLE user_info (
    user_id VARCHAR(20) NOT NULL PRIMARY KEY,
    user_pw VARCHAR(20) NOT NULL
);

CREATE TABLE memos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    important BOOLEAN DEFAULT FALSE,
    deleted BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);