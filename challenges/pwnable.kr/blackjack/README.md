
# `blackjack` Solution

At [blackjack.c](blackjack.c) line 726:

```C
if (bet > cash) //If player tries to bet more money than player has
```

a check for the bet is done. What one can do is put a negative number and lose on purpose. The bet is then:

```C
cash = cash - bet;
```

and you get a million:

    Cash: $500
    -------
    |C    |
    |  1  |
    |    C|
    -------

    Your Total is 1

    The Dealer Has a Total of 10

    Enter Bet: $-1000000

