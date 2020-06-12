from enum import IntEnum
from secrets import randbelow

class KeyOrder(IntEnum):
    MERSENNE_13      = 0,
    MERSENNE_17      = 1,
    MERSENNE_19      = 2,
    MERSENNE_31      = 3,
    MERSENNE_61      = 4,
    MERSENNE_89      = 5,
    MERSENNE_107     = 6,
    MERSENNE_127     = 7,
    MERSENNE_521     = 8,
    MERSENNE_607     = 9,
    MERSENNE_1279    = 10,
    MERSENNE_2203    = 11,
    MERSENNE_2281    = 12,
    MERSENNE_3127    = 13,
    MERSENNE_4253    = 14,
    MERSENNE_4423    = 15,
    MERSENNE_9689    = 16

def egcd(a, b):
    ''' Euclidean algorithm for computing the greatest common divisor (GCD) of two integers

        Params:
            b, n - Input ingegers
    
        Returns:
            (gcd(b, n), a, m) such that a * b + n * m = gcd(b, n)
    '''
    (x0, x1, y0, y1) = (1, 0, 0, 1)
    
    while b != 0:
        (q, a, b) = (a // b, b, a % b)
        (x0, x1) = (x1, x0 - q * x1)
        (y0, y1) = (y1, y0 - q * y1)

    return (a, x0, y0)

   
def mod_inverse(k, prime):
    k = k % prime

    if k < 0:
        r = egcd(prime, -k)[2]
    else:
        r = egcd(prime, k)[2]
        
    return (prime + r) % prime
    

class ShamirSharing():
    ''' Implementation of Shamir's secret sharing alrogithm '''
    def __init__(self):
        self.__calc_mersenne()
    
    def __calc_mersenne(self):
        ''' Calculate mersenne primes up to 2917 digits (9689-order) lange '''
        PRIME_EXPONENTS = [ 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3127, 4253, 4423, 9689 ]
    
        self.__primes = []
        for exp in PRIME_EXPONENTS:
            self.__primes.append(2**exp - 1)

    def __enough_prime(self, values):
        ''' Returns a prime number that is greater as all values in input array,
            or None if greater numbers are not found '''
        max_value = max(values)
        
        for prime in self.__primes:
            if prime > max_value:
                return prime
        
        return None
    
    def __str_to_int(self, string):
        ''' Mapping string to an integer number '''
        encoded_string = string.encode('utf-8')

        return int.from_bytes(bytes(encoded_string), byteorder='big') * 10000 + len(encoded_string)
    
    def __int_to_str(self, integer):
        ''' Mapping an integer number to a string '''
        length = integer % 10000
        integer = integer // 10000
        
        return integer.to_bytes(length, byteorder='big').decode('utf-8')
    
    def __secret_int_to_points(self, secret, share_threshold, num_points, key_order=None):
        ''' Split an integer secret into shares (x, y) '''
        if key_order is None:
            prime = self.__enough_prime([secret])
        else:
            prime = self.__primes[key_order]
        
        if prime is None:
            raise ValueError("Secret is too big for share calculation")
        
        coefficients = self.__get_random_poly(share_threshold - 1, secret, prime)

        return self.__get_poly_points(coefficients, num_points, prime)

    def __get_random_poly(self, degree, intercept, upper_bound):
        ''' Generate random polynomial '''
        coefficients = [intercept]

        for i in range(degree):
            random_coeff = randbelow(upper_bound)
            coefficients.append(random_coeff)

        return coefficients
    
    def __get_poly_points(self, coefficients, num_points, prime):
        ''' Calculate the first n polynomial points [ (1, f(1)), (2, f(2)), ... (n, f(n)) ] '''
        points = []
        for x in range(1, num_points + 1):
            y = coefficients[0]

            for i in range(1, len(coefficients)):
                exponentiation = (x**i) % prime
                term = (coefficients[i] * exponentiation) % prime
                y = (y + term) % prime

            points.append((x, y))
            
        return points
    
    def __points_to_secret(self, points, prime=None):
        ''' Get secret from points '''
        for point in points:
            x_values, y_values = zip(*points)
            
            if prime is None:
                prime = self.__enough_prime(y_values)
                
            free_coefficient = self.__lagrange_interpolation(0, points, prime)
            secret_int = free_coefficient
            
            return secret_int
        
    def __lagrange_interpolation(self, x, points, prime):
        ''' Lagrange interpolation in finite feld '''
        x_values, y_values = zip(*points)
    
        f_x = 0
        for i in range(len(points)):
            numerator, denominator = 1, 1
            for j in range(len(points)):
                if i == j:
                    continue

                numerator = (numerator * (x - x_values[j])) % prime
                denominator = (denominator * (x_values[i] - x_values[j])) % prime

            lagrange_polynomial = numerator * mod_inverse(denominator, prime)

            f_x = (prime + f_x + (y_values[i] * lagrange_polynomial)) % prime

        return f_x

    def split_secret(self, secret, share_threshold, num_shares, key_order=None):
        ''' Split secret '''
        if share_threshold < 2:
            raise ValueError('Threshold must be >= 2')
        elif share_threshold > num_shares:
            raise ValueError('Threshold must be < the total number of points')
            
        secret_int = self.__str_to_int(secret)

        return self.__secret_int_to_points(secret_int, share_threshold, num_shares, key_order)

    def recover_secret(self, shares):
        ''' Recover secret '''
        secret_int = self.__points_to_secret(shares)

        try:
            secret = self.__int_to_str(secret_int)
        except:
            return secret_int
        
        return secret
    
if __name__ == "__main__":
    s = ShamirSharing()
    print('Split secret to (2, 4)...')
    keys = s.split_secret('Hallo world', 2, 4)
    print(keys)
    
    print('\nRecover secret with keys 1 and 3...')
    print(s.recover_secret([keys[0], keys[2]]))
