osucabs
=======
Introduction
------------
This site is for the Ohio State Campus Area Bus Service.  

This installation guide is setup up assuming you have a brand new server compatible with Redhat Enterprise Linux  (e.g. CentOS, Scientific Linux, Amazon AMI).  

Installation
------------
### Add the 10gen Mondo DB repo 
#### Copied from http://docs.mongodb.org/manual/tutorial/install-mongodb-on-redhat-centos-or-fedora-linux/
    cat << EOF | sudo tee /etc/yum.repos.d/10gen.repo
    [10gen]
    name=10gen Repository
    baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
    gpgcheck=0
    enabled=1
    EOF
    
### You need to have git to clone our repo, and apache to execute
    sudo yum install -y git httpd mod_wsgi python-setuptools python-devel gcc libxslt-devel mongo18-10gen-server
    sudo easy_install web.py lxml pymongo
NOTE: I don't like the fact that we have to install gcc...but it is needed for lxml. 

### Here is where I put the directory.  This should be changed to /var/www/
    sudo mkdir /webdata
    sudo chmod -R 755 /webdata
    cd /webdata/
    
### Pull down the latest git repo
    sudo git clone https://github.com/patrickshuff/osucabs.git
    
### Copy our apache configuration into place
    sudo cp /webdata/osucabs/osucabs_apache.conf /etc/httpd/conf.d/osucabs.conf
    
# Run it!

### Make sure MongoDB is enable on reboot
    sudo chkconfig mongod on
    
### Start MongoDB
    sudo service mongod start
    
### Make sure apache starts on boot
    sudo chkconfig httpd on
    
### Start the apache process
    sudo service httpd start
    


Troubleshooting
---------------
The first place you should probably start (assuming you have apache in installed, and the config in place) is looking at the apache error_log:

sudo less /var/log/httpd/error_log

### The bus times on the webpage are way way off?  what's up?
Well the problem is likely your server is in a different timezone.  Make sure your server is set up to use eastern time zone

    sudo cp /usr/share/zoneinfo/US/Eastern /etc/localtime

