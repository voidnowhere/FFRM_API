FROM python:3.11.2

ARG USER
ARG UID

RUN useradd -mu $UID $USER

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod u+x /usr/local/bin/entrypoint.sh

USER $USER

ENTRYPOINT ["entrypoint.sh"]