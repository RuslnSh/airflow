-- set max_connections=50; -- parameter "shared_preload_libraries" cannot be changed without restarting the server

-- set shared_buffers='1GB'; -- parameter "shared_preload_libraries" cannot be changed without restarting the server

set effective_cache_size='4GB';

set work_mem='16MB';

set maintenance_work_mem='512MB';

set random_page_cost=1.1;

set temp_file_limit='10GB';

set log_min_duration_statement='200ms';

set idle_in_transaction_session_timeout='10s';

set lock_timeout='1s';

set statement_timeout='60s';

-- set shared_preload_libraries=pg_stat_statements; -- parameter "shared_preload_libraries" cannot be changed without restarting the server

-- set pg_stat_statements.max=10000; -- parameter "shared_preload_libraries" cannot be changed without restarting the server

set pg_stat_statements.track='all';
