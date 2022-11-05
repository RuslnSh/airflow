create table if not exists airflow.pageview_counts();
alter table airflow.pageview_counts
	add column if not exists pagename VARCHAR(50) NOT NULL
	, add column if not exists pageviewcount INT NOT NULL
	, add column if not exists datetime TIMESTAMP NOT NULL
;
