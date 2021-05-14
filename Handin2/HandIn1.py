import numpy as np
import math

# Entropy and MutualInformation by ol3270ma-s


class InfoTheory():

    def Entropy(self,P):
        """Input P:
        Matrix (2-dim array): Each row is a probability
        distribution, calculate its entropy,
        Row vector (1Xm matrix): The row is a probability
        distribution, calculate its entropy,
        Column vector (nX1 matrix): Derive the binary entropy
        function for each entry,
        Single value (1X1 matrix): Derive the binary entropy
        function
        Output:
        array with entropies"""
        H = 0
        # Checks for binary entropies
        if len(P.shape) == 1:
            # Single value
            H = np.array([self.binEntropy(P[0])])
        else:
            if P.shape[1] == 1:
                # Column vector
                res = np.empty([1, P.shape[0]])
                for i,col in enumerate(res[0]):
                    res[0][i] = self.binEntropy(col)
                H = res[0]
            else:
                if P.shape[0] == 1:
                    # Row vector
                    H = np.array([self.rowEntropy(P[0])])
                else:
                    # Matrix
                    res = np.empty([1,P.shape[0]])
                    for i,row in enumerate(P):
                        res[0][i] = self.rowEntropy(row)
                    H = res[0]
        return H
    
    def binEntropy(self, p):
        """ Input p:
        p(x) that is used to calculate the binary entropy.
        Output: H(p)
        """
        if p == 0 or (1-p) == 0:
            return 0
        else:
            H = ((-p)*math.log(p,2)) - ((1-p)*math.log(1-p,2))
            return H
    
    def rowEntropy(self, p_row):
        """ Input p_row:
        The row containing the probability distribution that is used to calculate the entropy.
        Output: H(p)
        """
        H = 0
        for p in p_row:
            if p != 0:
                H += ((-p) * math.log(p,2))
        return H

    def MutualInformation(self,P):
        """Derive the mutual information I(X;Y).
        Input P: P(X,Y).
        Output: I(X;Y) """
        
        # Calculate p_x and p_y
        p_x, p_y = np.zeros([1, P.shape[0]]), np.zeros([1, P.shape[1]])
        for i,row in enumerate(P):
            for i_x,cell in enumerate(row):
                # print("I: ", i , " ROW: ", row, " I_X: ", i_x, " CELL: ", cell, "P_X: ", p_x[0][i], " P_Y: ", p_y[0][i_x])
                p_x[0][i] += cell
                p_y[0][i_x] += cell
        
        H_x = self.Entropy(p_x)
        H_y = self.Entropy(p_y)
        H_xy = np.sum(self.Entropy(P))

        I = H_x + H_y - H_xy
        return I

if __name__=='__main__':
    # <Tests of your code when running from prompt>
    IT = InfoTheory()
    ### 1st test
    P1 = np.transpose(np.array([np.arange(0.0,1.1,0.25)]))# column vector
    H1 = IT.Entropy(P1)
    print('H1 =',H1)

    ### 2nd test
    P2 = np.array([[0.3, 0.1, 0.3, 0.3],
    [0.4, 0.3, 0.2, 0.1],
    [0.8, 0.0, 0.2, 0.0]])
    H2 = IT.Entropy(P2)
    print('H2 =',H2)

    ### 3rd test
    P3 = np.array([[0, 3/4],[1/8, 1/8]])
    I3 = IT.MutualInformation(P3)
    print('I3 =',I3)

    ### 4th test
    P4 = np.array([[1/12, 1/6, 1/3],
    [1/4, 0, 1/6]])
    I4 = IT.MutualInformation(P4)
    print('I4 =',I4)

    ### 5th test, my own to test a row vector
    P5 = np.array([np.arange(0.5, 1, 0.3)]) # row vector
    H5 = IT.Entropy(P5)
    print('H5 =',H5)