FROM alpine

# Parameters from the Dockerfile
ARG SFTP_ROOT_DIRECTORY
ARG SFTP_GROUPNAME
ARG SFTP_USERNAME
ARG SFTP_PASSWORD
ARG SFTP_UID_GID

# Install OpenSSH Server
RUN apk add --no-cache openssh
COPY ./sshd_config /etc/ssh/



# Create de default directories
RUN mkdir /osawards \
  && mkdir /osawards/metrics && chmod 777 /osawards/metrics \
  && mkdir /osawards/user_stories && chmod 777 /osawards/user_stories \
  && mkdir /osawards/reports && chmod 777 /osawards/reports \
  && mkdir /osawards/templates && chmod 777 /osawards/templates

# Copy the template files
COPY templates/* /osawards/templates/



# Create the Group
RUN addgroup --gid $SFTP_UID_GID $SFTP_GROUPNAME

# Create the users
RUN adduser -h $SFTP_ROOT_DIRECTORY -H -u $SFTP_UID_GID \
    -G $SFTP_GROUPNAME $SFTP_USERNAME;\
    echo $SFTP_USERNAME:$SFTP_PASSWORD | chpasswd

COPY ./entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh

EXPOSE 22

CMD ["/usr/bin/entrypoint.sh"]
