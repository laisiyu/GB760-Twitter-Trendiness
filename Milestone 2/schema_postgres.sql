CREATE TABLE tweets (
 time_stamp VARCHAR(50) NOT NULL,
 content VARCHAR(1500) NOT NULL
);

CREATE TABLE trendiness (
 cur_t VARCHAR(50) NOT NULL,
 phrase VARCHAR (150) NOT NULL,
 trendiness NUMERIC NOT NULL
);
