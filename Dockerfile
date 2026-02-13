FROM odoo:17

USER root

# Instalar Docker CLI
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://get.docker.com | sh && \
    rm -rf /var/lib/apt/lists/*

# Crear wrapper docker-compose (método correcto)
RUN printf '#!/bin/sh\nexec docker compose "$@"\n' > /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

USER odoo