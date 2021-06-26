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
COPY ./vuln /home/ctf/

# Copy flag.txt
COPY ./flag.txt /home/ctf/

# Make the binary and flag.txt
RUN chmod 755 /home/ctf/vuln && \
    chmod 644 /home/ctf/flag.txt && \
    chown -R ctf: /home/ctf

# Expose container
EXPOSE 9999

# vuln will try to get ./flag.txt so we create a symlink for it
RUN ln -s /home/ctf/flag.txt /flag.txt

# Run script when the container launches
CMD ["script", "-c", "xinetd -d -dontfork"]

