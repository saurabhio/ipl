import numpy as np

def calculatePageRank(A, d=0.50):
    numTeams = A.shape[0]
    precision = 0.0000001

    B = (1/numTeams) * np.ones((numTeams,numTeams))

    M = d*A + (1-d)*B

    p = (1/numTeams) * np.ones((numTeams,1))

    #evals, evecs = np.linalg.eig(M)
    #print(evecs[:,0])
    #print(M @ evecs[:,0])

    #e = (np.linalg.matrix_power(M, 100)) @ p
    #ss = e / np.linalg.norm(e)
    #print(ss)

    while True:
        prev = p
        p = M @ p

        if all(abs(p-prev) < precision):
            break
    
    return p


def columnStochasticMatrix(T):
    TM = T.values
    ilost = TM.sum(axis=0)
    numTeams = TM.shape[0]
    
    for i in np.arange(numTeams):
        if ilost[i] == 0:
            TM[i,i] = 1
        else:
            TM[:,i] = TM[:,i]/ilost[i]

    return TM
