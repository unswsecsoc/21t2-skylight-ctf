#!/bin/bash
mkdir /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown -R ctf /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
sudo -u ctf nsjail \
    -Ml --port 1337 \
    --user ctf \
    --group ctf \
    --max_conns_per_ip 16 \
    -R /usr -R /bin -R /lib -R /lib64 \
    -T /dev -R /dev/urandom -R /dev/null \
    -R /home/ctf/chal:/chal \
    --disable_proc \
    --time_limit 20 \
    --cgroup_cpu_ms_per_sec 100 \
    --cgroup_pids_max 64 \
    --cgroup_mem_max 67108864 \
    -- /usr/bin/python3 /chal/app.py
