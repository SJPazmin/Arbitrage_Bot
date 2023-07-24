import json

# your code to generate the pairs list goes here
symbols = ["AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD",
           "CADCHF", "CADJPY", "CHFJPY",
           "EURAUD", "EURCAD", "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD",
           "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD", "GBPUSD",
           "NZDUSD", "NZDCAD", "NZDJPY", "NZDCHF",
           "USDCAD", "USDCHF", "USDJPY"]
pairs = []
for i in range(len(symbols)):
    for j in range(i+1, len(symbols)):
        if symbols[i][-3:] == symbols[j][-3:]:
            pairs.append([symbols[i], symbols[j]])

# write the pairs list to a file
with open('pairs.json', 'w') as f:
    json.dump(pairs, f)