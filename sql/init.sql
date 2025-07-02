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
    date DATE,
    uploader VARCHAR(100),
    total_distance_km FLOAT,
    total_ascent_m FLOAT,
    total_descent_m FLOAT,
    total_duration TIME,
    ascent_time TIME,
    descent_time TIME,
    ascent_speed_kmh FLOAT,
    ascent_speed_vmph FLOAT,
    descent_speed_kmh FLOAT,
    descent_speed_vmph FLOAT,
    avg_speed_kmh FLOAT,
    avg_speed_vmph FLOAT,
    max_elevation_m FLOAT,
    min_elevation_m FLOAT  
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- join成 VIEW 當gpx/weather更新時 能夠自動更新 如果令建新表會是靜態表 要手動更新麻煩
CREATE OR REPLACE VIEW hiking AS
SELECT
    gpx.date,
    gpx.uploader,
    gpx.total_distance_km,
    gpx.total_ascent_m,
    gpx.total_descent_m,
    gpx.total_duration,
    gpx.ascent_time,
    gpx.descent_time,
    gpx.ascent_speed_kmh,
    gpx.ascent_speed_vmph,
    gpx.descent_speed_kmh,
    gpx.descent_speed_vmph,
    gpx.avg_speed_kmh,
    gpx.avg_speed_vmph,
    gpx.max_elevation_m,
    gpx.min_elevation_m,
    weather.station_id,
    weather.season,
    weather.temperature,
    weather.humidity,
    weather.wind_speed,
    weather.wind_direction,
    weather.rainfall
FROM gpx
LEFT JOIN weather
    ON gpx.date = weather.date
ORDER BY gpx.date;
   

select * from hiking;
select * from weather;
select * from gpx;