# Code is described in the handin
# Look at syndrome decoding algorithm
# 8 rows in the table, codeword is defined by 8
import numpy as np
import math

class ReedMuller:

    def __init__(self):
        return

    def G(self, r, m):
        """
        Derives the generator matrix. 
        Input: Non-negative integer r, positive integer m.
        """
        G = self._helper_function_G(r,m)
        return G
    
    def _helper_function_G(self, r, m):
        g0 = np.ones((1,pow(2,m)))
        gm = np.identity((pow(2, m)))
        if r == 0:
            return g0
        elif r == m:
            return gm
        else:
            # Adding the values to the matrix:
            a = b = self._helper_function_G(r, m-1)
            d = self._helper_function_G(r-1, m-1)
            c = np.zeros(d.shape)
            # Putting the matrix together:
            top_row = np.concatenate((a,b), axis=1)
            bottom_row = np.concatenate((c,d), axis=1)
            G = np.concatenate((top_row, bottom_row), axis=0)
            return G

    def generate_information_words(self):
        nbrs = np.empty((16,1), dtype=np.uint8)
        # Convert 0 to 15 to a bit array, which will get us 0000 - 1111
        for i in range(16):
            nbrs[i] = i
        u = np.empty((16,4),dtype=np.uint8)
        for index, b in enumerate(np.unpackbits(nbrs, axis=1)):
            _, new_b = np.array_split((b),2)
            new_b = np.atleast_2d(new_b)
            u[index] = new_b
        return u
    
    def generate_codewords(self, u, G):
        codewords = np.empty((16,8))
        print('--- Codewords: --- ')
        for index, info in enumerate(u):
            x = info.dot(G)
            # Transform x to base 2:
            for val in x:
                x = x%2
            print( info, ': ', x)
            codewords[index] = x
        return codewords



    # Uses formula (7.8) in the book on page 173: 
    def calc_d_min(self, G):
        # Sets d_min to max diff
        d_min = 8
        for row_index, row in enumerate(G):
            for i,_ in enumerate(G):
                if row_index != i:
                    diff = 0
                    for row_current, row_diff in zip(G[row_index], G[i]):
                        if row_current != row_diff:
                            diff += 1
                    if diff < d_min:
                        d_min = diff
        print('d_min = ', d_min)
        
        # Detection of errors with d_min, theorem 7.2 in the book (p.176), example (7.20)
        detect = d_min-1
        print('Can detect max', detect, 'errors')

        # Correction of errors with d_min, theorem 7.2 in the book (p.176), example (7.21)
        corr = math.floor((d_min-1)/2)
        print('Can correct', corr, 'errors')
        return d_min

    def verify(self, G):
        G_t = np.transpose(G)
        res = np.dot(G, G_t)
        # Since we work in binary, we need to compute the matrix to binary values:
        for row_i, row in enumerate(res):
            for col_i, col in enumerate(row):
                res[row_i][col_i] = col % 2
        print(res)
        print('-- Matrix contains of only multiples of 2s, the code is self dual --')
        return 

def main():
    RM = ReedMuller()
    G = RM.G(1,3)
    # Find all codewords:
    # first, finding out u - the information words:
    u = RM.generate_information_words()
    codewords = RM.generate_codewords(u, G)
    d_min = RM.calc_d_min(G)
    RM.verify(G)
    return 

if __name__ == '__main__':
    main()
