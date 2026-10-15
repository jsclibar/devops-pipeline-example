# Imagem oficial do Nginx
FROM nginx:1.31.5-alpine

# Atualiza os pacotes do sistema (opcional)
# RUN apk upgrade --no-cache

# Instala o curl para o HEALTHCHECK
RUN apk add --no-cache curl

# Remove a configuração padrão
RUN rm /etc/nginx/conf.d/default.conf

# Copia a configuração do Nginx
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# Expõe a porta HTTP
EXPOSE 80

# Verifica se o Nginx está respondendo
HEALTHCHECK CMD curl --fail http://localhost/nginx-health || exit 1

# Inicializa o Nginx em primeiro plano
CMD ["nginx", "-g", "daemon off;"]