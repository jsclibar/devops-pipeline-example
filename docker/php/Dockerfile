# Imagem oficial do PHP com PHP-FPM

FROM php:8.5-fpm-alpine

# Instala o cliente FastCGI para o HEALTHCHECK

RUN apk add --no-cache fcgi

# Diretório da aplicação

WORKDIR /var/www/html

# Copia a aplicação

COPY public/ public/

# Habilita o ping do PHP-FPM

COPY docker/php/healthcheck.conf /usr/local/etc/php-fpm.d/healthcheck.conf

# Expõe a porta do PHP-FPM

EXPOSE 9000

# Verifica se o PHP-FPM está respondendo

HEALTHCHECK CMD SCRIPT_NAME=/ping SCRIPT_FILENAME=/ping REQUEST_METHOD=GET cgi-fcgi -bind -connect 127.0.0.1:9000 | grep -q "pong" || exit 1

# Inicializa o PHP-FPM

CMD ["php-fpm"]