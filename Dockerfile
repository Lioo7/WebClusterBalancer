FROM nginx:1.25.4

# copy the configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
