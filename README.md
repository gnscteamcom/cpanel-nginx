This is the Cpnginx auto installer script . Please read more about from https://cpnginx.com/documentation/

## Installation
## run the following command .
```
wget https://github.com/peter21581/cpanel-nginx/archive/master.zip -O cpanel-nginx-master.zip && upzip cpanel-nginx-master.zip;
cd cpanel-nginx-master && chmod 755 install.py && ./install.py install;
```

## Uninstallation
### run the following command .
```
wget https://github.com/peter21581/cpanel-nginx/archive/master.zip -O cpanel-nginx-master.zip && upzip cpanel-nginx-master.zip;
cd cpanel-nginx-master && chmod 755 install.py &&  ./install.py remove;
```
## Upgrade
### run the following command
```
/etc/cpnginx/updatecpnginx.py
```
## Nginxctl
### This is a new command line tool for managing your cpnginx server. It is a unique tool developed by cpnginx developers. You can do almost all operations of your nginx server from command line.

### To see the available options , please run the following command
```
nginxctl  help
```   
### 1) build : This option will help you to build some of the nginx tools. To build the nginx server run the following command
```
nginxctl  build nginx
```   
### To build your custom version of nginx run the following command
```
nginxctl build nginx --version 1.11.1
```
### To build all nginx vhosts run the following command
```
nginxctl build vhosts
```
     
### To build all ssl certificates run the following command
```
nginxctl build sslcerts
```
### 2) setupphpfpm : This option will automatically setup all multi-php fpm servers. It will use the cpanel provided multiple php binaries itself. This tool also set the default phpfpm as your servers default php version. Everything is automated . To update the phpfpm binaries please run the following commands
```
nginxctl setupphpfpm
```
    
### 3) rebuildvhost : This option will help you to rebuild the vhost settings of a domain or subdomain. Use the following syntax to run the commmand
```
nginxctl rebuildvhost  < domain name >
```
### eg : nginxctl rebuildvhost fun.com

### 4) rmvhost : This option will help you to remove a vhost entry of domain or subdomain from the server. It will automatically remove ssl and non-ssl vhosts from the nginx pool.
```
nginxctl rmvhost < domain name >
```
### eg: nginxctl rmvhost fun.com

### 5) rebuilduservhost : This option will help you to rebuill all domains vhost files of a cpanel user. This will build that users ssl or non-ssl domains and setup the php-fpm pools of the domains automatically
```
nginxctl rebuilduservhost  < cpanel user name >
```
### eg : nginxctl rebuilduservhost cpuser

### 6) rmuservhost : This option will remove a all nginx vhost files of a cpanel user. This will automatically remove the users php-fpm pool configurations, ssl domains and non-ssl domains. It only remove the nginx related files.
```
nginxctl rmuservhost  < cpanel user name >
```
### eg : nginxctl rmuservhost cpuser

### 7) templaterebuild : This option will rebuild all your nginx templates and apps templates pools. It will be automatically added to the cpnginx interface. You should run this command after making your own nginx vhost template files or app templates
```
nginxctl templaterebuild
```
    
### 8) restart :This options will restart your nginx server. To restart the nginx server run the following command
```
nginxctl restart
```
### 9) help : This option will show the nginxctl help menu
### 10) enable : This option is for enabling cpnginx in your server, if it is disabled by administrator.
### 11) disable : This will disable the cpnginx from your server, if it is enabled.
### 12) status : This will show the nginx service status
### 13) version : This will show the cpnginx version, nginx version and apache version

