# This is the check of our_key vs their_calculated_key
# Set a breakpoint there
break *(main+0x1fd)

# Run with 1 arg
run aaaa

# Print their_calculated_key stored in local variable [rbp - 0x40]
printf "%d\n", *(int*)($rbp-0x40)
quit
