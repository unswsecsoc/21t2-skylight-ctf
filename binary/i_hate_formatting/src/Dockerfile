# Basic Xinetd Docker Container
FROM ubuntu:18.04

# Apt-get update
RUN apt-get update && \
    apt-get install -y xinetd && \
    rm -rf /var/lib/apt/lists/*

# install 32-bit libraries
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386

# Create CTF user
RUN mkdir /home/ctf && \
    chmod 755 /home/ctf && \
    useradd -M -U -d /home/ctf ctf && \
    chown ctf:ctf /home/ctf
COPY xinetd.conf /etc/

# Copy binary
COPY ./vuln_real /home/ctf/

# Make the binary and flag
RUN chmod 755 /home/ctf/vuln_real && \
    chown -R ctf: /home/ctf

# Expose container
EXPOSE 9999

# Run script when the container launches
CMD ["script", "-c", "xinetd -d -dontfork"]
