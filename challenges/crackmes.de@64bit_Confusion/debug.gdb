# This is the check of our_key vs their_calculated_key
# Set a breakpoint there
break *(main+0x1fd)

# Run with 1 arg
run aaaa

# The key is stored in local variable [rbp - 0x40]
# Save the key in key.txt
python open("key.txt", "w").write(str(gdb.parse_and_eval("*(int*)($rbp-0x40)")))
quit
