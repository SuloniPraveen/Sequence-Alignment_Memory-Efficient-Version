
from resource import *
import time
import psutil
import argparse



def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input and output file paths.')
    parser.add_argument('input_file', type=str, help='Input file path')
    parser.add_argument('output_file', type=str, help='Output file path')
    return parser.parse_args()


missCost = {
    'A': {'A' : 0 ,   'C' : 110, 'G' : 48,  'T' : 94},
    'C': {'A' : 110 , 'C' : 0,   'G' : 118, 'T' : 48},
    'G': {'A' : 48 ,  'C' : 118, 'G' : 0,   'T' : 110},
    'T': {'A' : 94 ,  'C' : 48,  'G' : 110, 'T' : 0}
}

gapCost = 30



def D_P_Route(x, y):
    m = len(x)
    n = len(y)

    dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
    for j in range(m+1):
        dp[0][j] = j * gapCost
    
    for i in range(n+1):
        dp[i][0] = i * gapCost
    for i in range(1, n+1):
        for j in range(1, m+1):
            dp[i][j] = min(dp[i-1][j] + gapCost, dp[i][j-1] + gapCost, dp[i-1][j-1] + missCost[x[j-1]][y[i-1]])
    
    

    x_seq, y_seq = str(), str()

    while m > 0 and n > 0:
        if dp[n-1][m-1] + missCost[x[m-1]][y[n-1]] == dp[n][m]:
            x_seq = x[m-1] + x_seq
            y_seq = y[n-1] + y_seq
            m -= 1
            n -= 1
        
        
        elif dp[n-1][m] + gapCost == dp[n][m]:
            x_seq = '_' + x_seq
            y_seq = y[n-1] + y_seq
            n -= 1
        
        
        else:
            x_seq = x[m-1] + x_seq
            y_seq = '_' + y_seq
            m -= 1


    
    if n == 0 and m > 0:
        while m > 0:
            x_seq = x[m-1] + x_seq
            y_seq = '_' + y_seq
            m -= 1
    

    if m == 0 and n > 0:
        while n > 0:
            x_seq = '_' + x_seq
            y_seq = y[n-1] + y_seq
            n -= 1
    
    
    return (x_seq,y_seq, dp[len(y)][len(x)])

def Mem_eff_route(x, y, flag):
        m = len(x)
        n = len(y)

        
        dp = [[0 for _ in range(n+1)] for _ in range(2)]

        for i in range(n+1):
            dp[0][i] = gapCost * i

        
        if flag == 0:
            for i in range(1, m+1):
                dp[1][0] = i * gapCost
                for j in range(1, n+1):
                    dp[1][j] = min(dp[0][j - 1] + missCost[x[i - 1]][y[j - 1]],
                                   dp[0][j] + gapCost,
                                   dp[1][j - 1] + gapCost)

                for j in range(n+1):
                    dp[0][j] = dp[1][j]
        
        elif flag == 1:
            for i in range(1, m+1):
                dp[1][0] = i * gapCost
                for j in range(1, n+1):
                    dp[1][j] = min(dp[0][j - 1] + missCost[x[m-i]][y[n-j]],
                                   dp[0][j] + gapCost,
                                   dp[1][j - 1] + gapCost)
                for j in range(n+1):
                    dp[0][j] = dp[1][j]

        
        return dp[1]

def D_C_Route(x, y):
        m = len(x)
        n = len(y)
      
        if m < 2 or n < 2:
            return D_P_Route(x, y)
        else:
            mid = m//2
            low = Mem_eff_route(x[:mid], y, 0)

            up = Mem_eff_route(x[mid:], y, 1)

            dummy = [low[j] + up[n - j] for j in range(n + 1)]

            idx = dummy.index(min(dummy))

            lowRem = D_C_Route(x[:mid], y[:idx])
            upRem = D_C_Route(x[mid:], y[idx:])

        return [lowRem[k] + upRem[k] for k in range(3)]






args = parse_arguments()
input_file_path = args.input_file
output_file_path = args.output_file
with open(input_file_path, 'r') as file:
    lines = file.readlines()
next_string = 1
base_string = lines[0].strip()
insertion_indices = []
i = 0
for line in lines[1:]:
    line = line.strip()
    if line.isdigit():
        insertion_indices.append(int(line))
        i = i + 1
    else:
        next_string = i
        break



strings = base_string
for idx in insertion_indices:
    new_string = strings[:idx+1] + strings + strings[idx+1:]
    strings = new_string



base_string_2 = lines[next_string+1].strip()
insertion_indices_2 = [int(line.strip()) for line in lines[next_string+2:]]
strings2 = base_string_2
for idx in insertion_indices_2:
    new_string = strings2[:idx+1] + strings2 + strings2[idx+1:]
    strings2 = new_string



x,y = strings,strings2

p_gap = 30



process = psutil.Process()



start_time = time.time()
result = D_C_Route(x,y)
end_time = time.time()
time_taken = (end_time - start_time) * 1000 
memory_info = process.memory_info()
memory_used = int(memory_info.rss / 1024)    

#print(f"Time taken: {time_taken} ms")
#print(f"Memory used: {memory_used} KB")
#print(result[2])

with open(output_file_path, 'w') as file:
    file.write('\n'.join([str(result[2]),result[0],result[1],str(time_taken),str(memory_used)]))




