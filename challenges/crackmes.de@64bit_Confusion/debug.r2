# This is the check of our_key vs their_calculated_key
s main + 0x1fd
# Set a breakpoint there
db main + 0x1fd
dc
# Print their_calculated_key stored in local variable [rbp - 0x40]
pf d 4 @  `dr?rbp` - 0x40