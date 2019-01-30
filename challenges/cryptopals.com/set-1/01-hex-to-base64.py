#!/usr/bin/env python3

import base64


def main():
    input_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    output_string = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    my_answ = base64.b64encode(bytes.fromhex(input_string)).decode("ascii")

    print("output_str = {:s}".format(output_string))
    print("my_answ    = {:s}".format(my_answ))

    assert my_answ == output_string


if __name__ == '__main__':
    main()
