import random
import math
import sys

def prime_test(n,k):
    """
        Miller-Rabin Primality Testing
        
        Bryan Mayson 
        10.06.2020
    """
    if (n%2 == 0):
        return False
    s= 0
    t= n-1
    if t > 0:
        while (t%2 ==0):
            s+=1
            t = t/2
        #print(n-1,math.pow(2,s)*t)
        for _ in range(k):
            a = random.randint(2,n-1)
            if math.pow(a,n-1)%n != 1:
                return False
            for i in range(1,s+1):
                if( math.pow(a,math.pow(2,i)*t) == 1 )and ((math.pow(a,math.pow(2,i-1)*t) != 1 ) or(math.pow(a,math.pow(2,i-1)*t) != -1 )):
                    return False
    return True
    
    
def genPrime(k):
    """
        Generate a prime number with bit size k
        
        Bryan Mayson 
        10.06.2020
    """
    val_a = math.pow(2,k-1)
    val_b = math.pow(2,k)-1
    isPrime = False
    # while the previous generated value is not a prime
    while isPrime is False:
        # generate a value for this bit size
        n = random.randint(val_a,val_b)
        isPrime= prime_test(n,k)
    
    return n/1
