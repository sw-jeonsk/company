CREATE USER company_admin WITH PASSWORD 'test1234!';
ALTER ROLE company_admin SET client_encoding TO 'utf8';
ALTER ROLE company_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE company_admin SET TIMEZONE TO 'Asia/Seoul';
ALTER ROLE company_admin WITH SUPERUSER;

CREATE DATABASE company_db;
CREATE DATABASE test_company_db;
GRANT ALL PRIVILEGES ON DATABASE company_db TO company_admin;
GRANT ALL PRIVILEGES ON DATABASE test_company_db TO company_admin;
