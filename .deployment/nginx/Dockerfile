FROM nginx:alpine

WORKDIR /var/www/html

RUN mkdir /var/www/html/staticfiles
RUN mkdir /var/www/html/mediafiles

COPY nginx.conf /etc/nginx/conf.d/default.conf
