-- Used to create a simple database for testing.
-- I'm sure the actual table would be setup a bit differently.
CREATE DATABASE url_lookup_testing;
USE url_lookup_testing;
CREATE TABLE url_table (url VARCHAR(128));
INSERT INTO url_table (url) VALUES ('test1'), ('test2'), ('test3');
