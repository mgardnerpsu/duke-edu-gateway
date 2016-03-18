#!/bin/bash
echo "Starting ..."

echo ">> Delete old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -exec rm -i {} \;

# Optional
echo ">> Drop database tables"
psql -d edugway -c "select 'drop table ' || tablename ||  ' cascade;' from pg_tables where tableowner='matt'" -o tmp-drop-tables.sql -t
cat tmp-drop-tables.sql

read -p "This will DROP ALL DB TABLES...\nAre you sure you want to continue? <yes/no> " prompt
if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]
then
	echo ">> Dropping database tables"
	psql -d edugway -f tmp-drop-tables.sql
else
  	echo ">> Skipping drop tables"
fi

rm tmp-drop-tables.sql

echo ">> Done"
