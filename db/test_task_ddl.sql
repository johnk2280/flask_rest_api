
USE test_task;

DROP TABLE IF EXISTS urls;

CREATE TABLE urls(
	id SERIAL PRIMARY KEY,
	`urls` TEXT,
	`short_urls` TEXT,
	created_at DATETIME DEFAULT NOW()
);
