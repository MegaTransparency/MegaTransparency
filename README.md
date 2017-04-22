# MegaTransparency.com

The mission of MegaTransparency.com is is to efficiently publish all the world's interesting public information in one well organized place.

### Install

This guide assumes you are using Ubuntu Xenial on Scaleway C2L.

```
adduser main
usermod -aG sudo main
echo "main ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
cp -R .ssh /home/main/.ssh
chown main -R /home/main/.ssh
chmod 700 /home/main/.ssh
chmod 600 /home/main/.ssh/authorized_keys
```
Confirm can login as main. Then we disable ssh into root.
```
sudo sed -z 's/PermitRootLogin without-password\|$/PermitRootLogin no/' /etc/ssh/sshd_config | sudo dd of=/etc/ssh/sshd_config
sudo service ssh restart
sudo apt-get update
sudo apt-get install -y build-essential python-dev git-core python-pip virtualenv nginx
sudo pip install virtualenv uwsgi
sudo apt-get install uwsgi
git clone https://github.com/megatransparency/megatransparency.git
cd megatransparency
cp _config.py.example _config.py
virtualenv --python=/usr/bin/python2 env
source env/bin/activate
python -m pip install -r requirements.txt
sudo apt-get install -y postgresql postgresql-contrib
sudo usermod -a -G sudo postgres
sudo -u postgres psql
CREATE DATABASE megatransparency;
CREATE USER megatransparency WITH PASSWORD '****changeme****';
CREATE USER public_data_query WITH PASSWORD '****changeme****';
GRANT ALL PRIVILEGES ON DATABASE "megatransparency" to megatransparency;
\connect megatransparency
GRANT USAGE ON SCHEMA megatransparency TO public_data_query;
GRANT SELECT ON megatransparency.public_page_views TO public_data_query;
GRANT SELECT ON megatransparency.voters TO public_data_query;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\q
```
Update _config.py
```
python manage.py db upgrade
uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi --callable=app
```

```
sudo cp etc_nginx_sites_available_megatransparency_com /etc/nginx/sites-available/megatransparency.com
sudo ln -s /etc/nginx/sites-available/megatransparency.com /etc/nginx/sites-enabled/megatransparency.com
sudo cp etc_nginx_sites_available_dev_megatransparency_com /etc/nginx/sites-available/dev.megatransparency.com
sudo ln -s /etc/nginx/sites-available/dev.megatransparency.com /etc/nginx/sites-enabled/dev.megatransparency.com
sudo service nginx restart
```
Below is from http://serverfault.com/questions/775965/wiring-uwsgi-to-work-with-django-and-nginx-on-ubuntu-16-04
```
sudo mkdir /etc/uwsgi/
sudo mkdir /etc/uwsgi/sites
sudo cp megatransparency.ini /etc/uwsgi/sites/megatransparency.ini
sudo cp megatransparency_dev.ini /etc/uwsgi/sites/megatransparency_dev.ini
sudo cp uwsgi.service /etc/systemd/system/uwsgi.service
```

If you need to quickly delete page view data because of unwanted leakage do

`DELETE FROM page_views; DELETE FROM public_page_views;`

```
CREATE TABLE voters (
        slug TEXT PRIMARY KEY,
        voters_at_same_address JSONB,
        statevoterid TEXT,
        countyvoterid TEXT,
        title TEXT,
        fname TEXT,
        mname TEXT,
        lname TEXT,
        namesuffix TEXT,
        birthdate DATE,
        gender TEXT,
        regstnum TEXT,
        regstfrac TEXT,
        regstname TEXT,
        regsttype TEXT,
        regunittype TEXT,
        regstpredirection TEXT,
        regstpostdirection TEXT,
        regunitnum TEXT,
        regcity TEXT,
        regstate TEXT,
        regzipcode TEXT,
        countycode TEXT,
        precinctcode TEXT,
        precinctpart TEXT,
        legislativedistrict TEXT,
        congressionaldistrict TEXT,
        mail1 TEXT,
        mail2 TEXT,
        mail3 TEXT,
        mail4 TEXT,
        mailcity TEXT,
        mailzip TEXT,
        mailstate TEXT,
        mailcountry TEXT,
        registrationdate DATE,
        absenteetype TEXT,
        lastvoted DATE,
        statuscode TEXT,
        dflag TEXT
);
COPY voters FROM '/home/main/voters.csv' CSV HEADER DELIMITER AS ',';
```

### Deployment

Currently am running this by hand each time I want to deploy latest code
```
cd ~/MegaTransparency; source env/bin/activate; git pull; python manage.py db upgrade; sudo systemctl restart uwsgi
```

