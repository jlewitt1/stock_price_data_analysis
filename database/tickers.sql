CREATE database stocks; 

SHOW databases;
USE stocks;

DROP database stocks;
DROP TABLE tickers;

CREATE TABLE tickers ( 
	ticker_id INT NOT NULL auto_increment,
    ticker_name VARCHAR(20) NOT NULL,
    announcement_date DATE NOT NULL,
    PRIMARY KEY(ticker_id)
);

SET SQL_SAFE_UPDATES = 0;

UPDATE tickers SET announcement_date = date_format(announcement_date, '%d/%m/%y');

ALTER TABLE tickers AUTO_INCREMENT=1;

SELECT * FROM tickers;

DELETE FROM tickers WHERE ticker_id = 1;
