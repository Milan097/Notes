#!/usr/bin/env bash

echo "enabling btree_gist on database $POSTGRES_DB"
psql -U $POSTGRES_USER --dbname="$POSTGRES_DB" <<-'EOSQL'
  create extension if not exists btree_gist;
EOSQL
echo "finished with exit code $?"