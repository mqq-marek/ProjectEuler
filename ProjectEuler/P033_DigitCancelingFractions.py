"""
The fraction  49/98 is a curious fraction.
An inexperienced mathematician while attempting to simplify it may incorrectly believe
that  49/98 = 4/8 is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

Which means fractions where trailing 0's are cancelled are trivial.
So we will ignore all the cases where we have to cancel 0's.

You will be given 2 integers  N and K.  N represents the number of digits in
Numerator and Denominator, and  K represents the exact number of digits to be "cancelled"
from Numerator and Denominator. Find every non-trivial fraction,
(1) where numerator is less than denominator,
(2) and the value of the reduced fraction is equal to the original fraction.

Sum all the Numerators and the Denominators of the original fractions, and print them separated by a space.

"""