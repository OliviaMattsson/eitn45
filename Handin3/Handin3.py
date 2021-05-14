# Code is described in the handin
# Look at syndrome decoding algorithm
# 8 rows in the table, codeword is defined by 8
import numpy as np

class ReedMuller:

    def __init__(self):
        return

    def G(self, r, m):
        """
        Derives the generator matrix. 
        Input: Non-negative integer r, positive integer m.
        """
        g0 = np.ones((1,pow(2,m)))
        print(g0)
        gm = np.identity((pow(2, m)))
        gm = np.matrix(gm)
        print(gm)
        G = np.hstack()
        return gm
    
    def _helper_function_G(self, r, m):
        return

def main():
    RM = ReedMuller()
    RM.G(1,3)
    return 

if __name__ == '__main__':
    main()
