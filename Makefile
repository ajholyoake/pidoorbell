
.PHONY: install

install:
	cp ./doorbell.service /etc/systemd/system/
	cp ./connect-tunnel.service /etc/systemd/system
	cp ./doorbell.nginx /etc/nginx/sites-available/doorbell
	ln -sf /etc/nginx/sites-available/doorbell /etc/nginx/sites-enabled
	chmod 644 /etc/systemd/system/connect-tunnel.service
	chmod 644 /etc/systemd/system/doorbell.service
	systemctl daemon-reload
	systemctl enable connect-tunnel.service
	systemctl enable doorbell.service
	systemctl restart connect-tunnel.service
	systemctl restart doorbell.service
	systemctl restart nginx

