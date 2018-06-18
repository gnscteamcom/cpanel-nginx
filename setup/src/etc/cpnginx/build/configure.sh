#!/bin/bash
./configure --prefix=/usr/local/nginx \
	--with-http_ssl_module \
	--with-http_ssl_module \
	--with-http_v2_module \
	--with-http_realip_module \
	--with-http_flv_module \
	--with-http_mp4_module \
	--with-ipv6 \
	--with-http_stub_status_module 

