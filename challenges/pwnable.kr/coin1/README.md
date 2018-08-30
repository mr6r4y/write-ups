# `coin1` Solution

The solution script is [solve.py](solve.py)

Solution generation:

     base64 solve.py | python -c "import sys;print 'echo %s | base64 -d | python' % sys.stdin.read().replace('\n', '')"

and the command to execute on the [pwnable.kr](http://pwnable.kr) server:

    echo IyEvdXNyL2Jpbi9lbnYgcHl0aG9uCgoKZnJvbSBwd24gaW1wb3J0ICoKaW1wb3J0IGFyZ3BhcnNlCmltcG9ydCByZQppbXBvcnQgcmFuZG9tCgoKZGVmIGdldF9hcmdzKCk6CiAgICBwYXJzZXIgPSBhcmdwYXJzZS5Bcmd1bWVudFBhcnNlcihkZXNjcmlwdGlvbj0iUHduYWJsZS5rciAtIGNvaW4xIGNoYWxsZW5nZSBzb2x2ZXIiKQogICAgcmV0dXJuIHBhcnNlci5wYXJzZV9hcmdzKCkKCgpkZWYgcGFyc2VfY29pbnMobGluZSk6CiAgICBwID0gIl5OPShbXGRdKykgQz0oW1xkXSspJCIKICAgIHIgPSByZS5tYXRjaChwLCBsaW5lKQoKICAgIHJldHVybiBpbnQoci5ncm91cCgxKSksIGludChyLmdyb3VwKDIpKQoKCmRlZiBwcm9jZXNzX2NvaW5zKHIpOgogICAgbiwgYyA9IHBhcnNlX2NvaW5zKHIucmVjdmxpbmVfcmVnZXgoIl5OPVtcZF0rIEM9W1xkXSskIikpCiAgICBsb2cuaW5mbygiTj0laSwgYz0laSIgJSAobiwgYykpCgogICAgYWxsX24gPSByYW5nZShuKQoKICAgIGZvciBpIGluIHJhbmdlKGMpOgogICAgICAgIG0gPSBsZW4oYWxsX24pIC8gMgoKICAgICAgICBsZWZ0X24sIHJpZ2h0X24gPSBhbGxfbls6bV0sIGFsbF9uW206XQogICAgICAgIGlucCA9ICIgIi5qb2luKFsiJWkiICUgaSBmb3IgaSBpbiBsZWZ0X25dKQogICAgICAgIHIuc2VuZGxpbmUoaW5wKQoKICAgICAgICBvdXQgPSBpbnQoci5yZWN2bGluZSgpKQogICAgICAgICMgbG9nLmluZm8oIkNvaW5zOiAlcywgV2VpZ2h0OiAlaSIgJSAoaW5wLCBvdXQpKQoKICAgICAgICBpZiBvdXQgPCAxMCAqIGxlbihsZWZ0X24pOgogICAgICAgICAgICBhbGxfbiA9IGxlZnRfbgogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGFsbF9uID0gcmlnaHRfbgoKICAgIHdyb25nX2NvaW4gPSAiJWkiICUgYWxsX25bMF0KICAgIHIuc2VuZGxpbmUod3JvbmdfY29pbikKCiAgICByZXN1bHQgPSByLnJlY3ZsaW5lKCkKICAgIGxvZy5pbmZvKCJSZXN1bHQ6ICVzIiAlIHJlc3VsdCkKCgpkZWYgbWFpbigpOgogICAgYXJncyA9IGdldF9hcmdzKCkKCiAgICAjIGhvc3QsIHBvcnQgPSAicHduYWJsZS5rciIsIDkwMDcKICAgIGhvc3QsIHBvcnQgPSAiMTI3LjAuMC4xIiwgOTAwNwoKICAgIHIgPSByZW1vdGUoaG9zdCwgcG9ydCkKCiAgICB0cnk6CiAgICAgICAgd2hpbGUgVHJ1ZToKICAgICAgICAgICAgcHJvY2Vzc19jb2lucyhyKQogICAgZXhjZXB0IEVPRkVycm9yOgogICAgICAgIGxvZy5pbmZvKCJHYW1lIE92ZXIiKQoKCmlmIF9fbmFtZV9fID09ICdfX21haW5fXyc6CiAgICBtYWluKCkK | base64 -d | python

# Notes

Rules and description:

        ---------------------------------------------------
        -              Shall we play a game?              -
        ---------------------------------------------------
        
        You have given some gold coins in your hand
        however, there is one counterfeit coin among them
        counterfeit coin looks exactly same as real coin
        however, its weight is different from real one
        real coin weighs 10, counterfeit coin weighes 9
        help me to find the counterfeit coin with a scale
        if you find 100 counterfeit coins, you will get reward :)
        FYI, you have 60 seconds.
        
        - How to play - 
        1. you get a number of coins (N) and number of chances (C)
        2. then you specify a set of index numbers of coins to be weighed
        3. you get the weight information
        4. 2~3 repeats C time, then you give the answer
        
        - Example -
        [Server] N=4 C=2    # find counterfeit among 4 coins with 2 trial
        [Client] 0 1        # weigh first and second coin
        [Server] 20         # scale result : 20
        [Client] 3          # weigh fourth coin
        [Server] 10         # scale result : 10
        [Client] 2          # counterfeit coin is third!
        [Server] Correct!

        - Ready? starting in 3 sec... -
    N=828 C=10
    time expired! bye!
