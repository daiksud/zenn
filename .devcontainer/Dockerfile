# ref: https://github.com/devcontainers/images/blob/main/src/base-ubuntu/.devcontainer/Dockerfile
ARG VARIANT="noble"
FROM buildpack-deps:${VARIANT}-curl

RUN if [ "$VARIANT" = "noble" ]; then \
      if id "ubuntu" &>/dev/null; then \
        echo "Deleting user 'ubuntu'  for $VARIANT" && userdel -f -r ubuntu || echo "Failed to delete ubuntu user for $VARIANT"; \
      else \
        echo "User 'ubuntu' does not exist for $VARIANT"; \
      fi; \
    fi

RUN set -ex; \
    apt-get update; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get full-upgrade -y --no-install-recommends; \
    apt-get install -y --no-install-recommends \
        neovim \
    ; \
    rm -rf \
        /var/lib/apt/lists/* \
    ; \
    true

# Local fix for issue with timezone data at 'buildpack-deps'. Ref# https://github.com/devcontainers/images/issues/1709
RUN apt-get update; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get -y reinstall --no-install-recommends tzdata; \
    rm -rf /var/lib/apt/lists/*; \
    true
