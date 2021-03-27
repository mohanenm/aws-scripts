#!/bin/bash

# do not need to get into root - ec2 already runs commands in sudo
yum update -y 
yum install -y httpd.x86_64
systemctl start httpd.service
systemctl enable httpd.service #enable on reboot
echo "hello world from $(hostname -f)" > /var/www/html/index.html
