# Imagem oficial do Nginx

FROM nginx:1.31.5-alpine

#RUN apk upgrade --no-cache

# Instala o curl para o HEALTHCHECK

RUN apk add --no-cache curl

# Remove a configuração padrão

RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuração da aplicação

COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos públicos da aplicação

COPY public/ /var/www/html/public/

# Expõe a porta HTTP

EXPOSE 80

# Verifica se o Nginx está respondendo

HEALTHCHECK CMD curl --fail http://localhost/nginx-health || exit 1

# Inicializa o Nginx em primeiro plano

CMD ["nginx", "-g", "daemon off;"]