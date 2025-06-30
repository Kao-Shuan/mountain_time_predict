CREATE DATABASE IF NOT EXISTS mountain_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mountain_db;

CREATE TABLE IF NOT EXISTS weather (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    station_id VARCHAR(20) NOT NULL,
    season VARCHAR(10),
    temperature FLOAT,
    humidity INT,
    wind_speed FLOAT,
    wind_direction INT,
    rainfall FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_weather (station_id, date)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

DESC weather;
SELECT count(*) FROM weather;
DROP table weather;