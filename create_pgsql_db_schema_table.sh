#!/bin/bash
psql -U spotify_role -d spotify -a -f create_pgsql_db_schema_table.sql
