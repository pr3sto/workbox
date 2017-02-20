#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "Usage: $0 ip_address. Please specify ip address."
	exit
fi

# apache site config
echo "<VirtualHost $1:80>
    ServerName workbox
    ServerAdmin webmaster@localhost

    WSGIProcessGroup workbox
    WSGIDaemonProcess workbox user=www-data group=www-data threads=4 python-path=/opt/venvs/workbox/lib/python2.7/site-packages
    WSGIScriptAlias / /opt/venvs/workbox/lib/python2.7/site-packages/workbox/wsgiconfig/app.wsgi

    #Serve static files directly without TurboGears
    Alias /images /opt/venvs/workbox/lib/python2.7/site-packages/workbox/public/img
    Alias /css /opt/venvs/workbox/lib/python2.7/site-packages/workbox/public/css
    Alias /js /opt/venvs/workbox/lib/python2.7/site-packages/workbox/public/javascript

    CustomLog \${APACHE_LOG_DIR}/workbox-access_log common
    ErrorLog \${APACHE_LOG_DIR}/workbox-error_log

    # Set access permission
    <Directory \"/opt/venvs/workbox/lib/python2.7/site-packages/workbox\">
        Require all granted
    </Directory>
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet" > /etc/apache2/sites-available/workbox.conf

# bind ip address
echo "" >> /etc/hosts
echo "# workbox service by Chirukhin Alexey" >> /etc/hosts
echo -e "$1\tworkbox" >> /etc/hosts

# enable site
a2ensite workbox.conf
