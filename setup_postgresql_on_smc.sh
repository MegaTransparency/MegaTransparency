# see https://github.com/sagemathinc/smc/wiki/Using-PostgreSQL-in-SageMathCloud
cd
pg_ctl initdb -D data
echo "unix_socket_directories = '$HOME/data'" >> data/postgresql.conf
echo "unix_socket_permissions = 0700" >> data/postgresql.conf
pg_ctl -D data -l logfile -o "-p 43212" start