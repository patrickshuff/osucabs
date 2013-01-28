osucabs
=======

1. Installation

# Here is where I put the directory.  Not ideal, you can change this.  
sudo mkdir /webdata/osucabs
cd /webdata/osucabs

# Pull down the latest git repo
git clone https://github.com/patrickshuff/osucabs.git

# Install you need apache installed. 
sudo yum install -y httpd

# Copy our apache configuration into place
cp /webdata/osucabs/osucabs_apache.conf /etc/httpd/conf.d/osucabs.conf

2. Run it!

# Start the apache process
service httpd start

# Make sure apache starts on boot
chkconfig


