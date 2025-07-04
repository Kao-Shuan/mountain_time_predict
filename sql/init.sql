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
    UNIQUE KEY uniq_weather (date, station_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS gpx (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name_x VARCHAR(255),
    end_date DATE,
    max_elevation_time TIME,
    time_to_max_elevation_min INT,
    time_from_max_to_end_min INT,
    total_time INT,
    file_name_y VARCHAR(255),
    distance FLOAT,
    total_ascent FLOAT,
    total_descent FLOAT,
    user VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- join成 VIEW 當gpx/weather更新時 能夠自動更新 如果令建新表會是靜態表 要手動更新麻煩
CREATE OR REPLACE VIEW hiking AS
SELECT
    gpx.end_date,                
    gpx.user,                   
    gpx.distance,     
    gpx.total_ascent,   
    gpx.total_descent, 
    gpx.total_time,      
    gpx.time_to_max_elevation_min,         
    gpx.time_from_max_to_end_min,    
    weather.station_id,
    weather.season,
    weather.temperature,
    weather.humidity,
    weather.wind_speed,
    weather.wind_direction,
    weather.rainfall
FROM gpx
LEFT JOIN weather
    ON gpx.end_date = weather.date
ORDER BY gpx.end_date;