-----------------------------------------------
-- DELETE TABLES
-----------------------------------------------

DROP TABLE IF EXISTS METRIC;


-----------------------------------------------
-- MAKE TABLES
-----------------------------------------------

CREATE TABLE METRIC (
	CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP PRIMARY KEY NOT NULL,
	UUID TEXT NOT NULL,
	SENSOR_TYPE TEXT NOT NULL,
	RASPBERRY_UUID TEXT NOT NULL,
	VALUE DOUBLE NOT NULL
);
