age_of_alice       = 19
legal_drinking_age = 21


alice_is_old_enough = age_of_alice >= legal_drinking_age

print('old enough:', alice_is_old_enough)



amount_of_money  = 5
drinking_cost    = 13

alice_has_enough_money = amount_of_money >= drinking_cost
print('enough money:', alice_has_enough_money)


alice_is_in_wonderland = True


if (alice_has_enough_money and alice_is_old_enough) or alice_is_in_wonderland:
    print('cheers!')

    print('have fun!')


    

else:
    print('get out!')

    print('do not come back!')
 