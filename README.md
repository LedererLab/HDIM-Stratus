# How to set-up HDIM Stratus from scratch

## Start AWS EC2 instance

From EC2 Management Console choose `Launch Instance`.

At the Choose AMI screen choose `Ubuntu Server 16.04 LTS (HVM), SSD Volume Type - ami-835b4efa`
or similar.

Choose whatever instance type is appropriate and launch it.

You will be prompted to create a new key pair for the AWS instance -- create one
and copy the `*.pem` file to local machine. This is the key-pair that will be used
to login to the default `ubuntu` user.

## Setup initial Admin User

Log into EC2 instance as default user `ubuntu`.

`sudo apt-get update`

`sudo apt-get upgrade`

`sudo adduser $USERNAME` Create a new user to replace default `ubuntu` user

Type password and credentials for new user

`sudo adduser $USERNAME sudo` Give new user sudo privileges

`sudo su $USERNAME` Login into new user so that subsequent privileges will be set correctly.

`mkdir .ssh`

`chmod 700 ./.ssh`

`touch .ssh/authorized_keys`

`chmod 600 .ssh/authorized_keys`

Copy public key for new user into `.ssh/authorized_keys`

The new user, `$USERNAME` should now be able to login using ssh. At this point it
is a good idea to remove the default user `ubuntu` with `userdel -r ubuntu`.

## Install Dependencies

`sudo apt-get install gcc build-essential apache2 python3-dev python3-numpy python3-pip python3-pandas`

`sudo apt-get install python3-flask libapache2-mod-wsgi-py3`

`sudo apt-get install libeigen3-dev swig`

## Install HDIM-Stratus

`cd /usr/local`

`mkdir packages`

`cd packages`

`git clone https://bitbucket.org/johanneslederer/hdim-stratus HDIM-Stratus`

`cd /var/www`

`sudo mkdir HDIM_Stratus`

`sudo mkdir wsgi-scripts`

Copy WSGI start-up script `cp /usr/local/packages/HDIM-Stratus/hdim_app.wsgi ./wsgi-scripts/`.

Copy all other files, excluding `git` specific files `wsgi` files and Apache2 `*.conf`
from `/usr/local/packages/HDIM-Stratus` to `/var/www/HDIM-Stratus`.


## Install HDIM-Algorithm package

`cd /var/www/HDIM-Stratus`

`git clone https://github.com/LedererLab/FOS.git HDIM-Algo`

`./HDIM-Algo/Python_Wrapper/nix_build.sh`

## Set permissions for HDIM-Stratus root directory

### If A Single User is Maintaining App

Navigate to public website directory `cd /var/www`

Set permissions for app root directory for user who will be maintaining the App,
denoted by `$USERNAME`.

`chown -R $USERNAME ./HDIM-Stratus`

`chgrp -R www-data ./HDIM-Stratus`

`chmod -R 750 ./HDIM-Stratus`

`chmod g+s ./HDIM-Stratus`

### If Multiple Users are Maintaining App

Create group for app developers `sudo groupadd hdim-dev`.

Add all app developers to dev group with `sudo usermode -a -G hdim-dev #USERNAME`.

Navigate to public website directory `cd /var/www`

Set permissions for app root directory.

`sudo chown -R root ./HDIM-Stratus`

`sudo chgrp -R hdim-dev ./HDIM-Stratus`

`sudo chmod -R 775 ./HDIM-Stratus`

`sudo chmod g+s ./HDIM-Stratus`

## Setup SSL certificates through Let's Encrypt
`sudo add-apt-repository ppa:certbot/certbot`

`sudo apt-get update`

`sudo apt-get install python-certbot-apache`

`sudo certbot --apache -d hdim-stratus.com`

Select `HDIM_Stratus.conf` when prompted

`sudo crontab -e`

Add the following line to crontab
`15 3 * * * /usr/bin/certbot renew --quiet`
to enable automatic renewal of certificates.
