import pagerank as pr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def winningMatrix(teamsDF, resultsDF, m=-1):
    if m == -1:
        totalMatches = resultsDF.shape[0]
        m = totalMatches
    
    teams = teamsDF["Team"]
    T = pd.DataFrame(columns=teams, index=teams, dtype=float)
    T.fillna(0,inplace=True)

    for index, row in resultsDF.iterrows():            
        if index < m:
            t1 = row["Team1"]
            t2 = row["Team2"]
            winner = row["Winner"]
                        
            if winner == "SCHEDULED":
                break
            elif winner == "TIE" or winner == "N/R":
                T[t2][t1] += 0.5
                T[t1][t2] += 0.5
            elif winner == t1:
                T[t2][t1] += 1  #Note: t2 is col, t1 is row
            elif winner == t2:
                T[t1][t2] += 1  #Note: t1 is col, t2 is row
            else:
                print("Error")
    
    return T


def pointsTable(T):
    won = T.sum(axis=1)
    lost = T.sum(axis=0)

    pointT = pd.DataFrame(columns=['Won','Lost'])
    pointT['Won'] = won
    pointT['Lost'] = lost
    pointT.sort_values(by='Won', ascending=False, inplace=True)
    
    return pointT
    

if __name__ == "__main__":
        
    teamsDF = pd.read_csv('IPL2018_Teams.csv') # input teams in tournament
    resultsDF = pd.read_csv('IPL2018_Results.csv') # input results of tournament

    teams = teamsDF["Team"]
    numTeams = teamsDF.shape[0]
    totalMatches = resultsDF.shape[0]

    interval = np.arange(numTeams,totalMatches+1, numTeams)
    #interval = np.array([8,16,24,32,40,48,56])
    final = pd.DataFrame(index=teams, columns=interval, dtype=float)

    for m in interval:
        T = winningMatrix(teamsDF,resultsDF,m)
        TM = pr.columnStochasticMatrix(T.copy())
        p = pr.calculatePageRank(TM, d=0.5) 

        p = p.flatten().tolist()
        final[m] = pd.Series(p, index=teams, dtype=float)


    print("\nWinning Matrix:")
    print(T.astype('int'))

    pointT = pointsTable(T)
    print("\nPoints Table:")
    print(pointT.astype('int'))

    #print(final)

    sortedfinal = final[interval[-1]].sort_values(ascending=False)
    print("\nRankings using PageRank algorithm:")
    print(sortedfinal)


    final = final.T

    final.plot(marker='o', color=teamsDF["Colour"],alpha=0.6, linewidth=3, title="IPL 2018", xlim=[numTeams,totalMatches])
    plt.xlabel("Number of Matches")
    plt.ylabel("Score")
    plt.legend(loc="best", ncol=2, fontsize="large")
    plt.grid(True, 'major', 'y', ls='--', alpha=.6) 
    plt.xticks(np.arange(numTeams,totalMatches+1, numTeams))
    plt.show()

