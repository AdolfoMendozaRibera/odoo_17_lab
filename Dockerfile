FROM ribentek/ribentek_odoo_comm_17:v1.0

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates && \
    curl -fsSL https://get.docker.com | sh && \
    rm -rf /var/lib/apt/lists/*

RUN printf '#!/bin/sh\nexec docker compose "$@"\n' > /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Agregar usuario odoo al grupo docker
RUN usermod -aG docker odoo

USER odoo