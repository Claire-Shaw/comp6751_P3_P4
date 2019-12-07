from nltk.parse import FeatureEarleyChartParser 
from nltk import grammar, parse

keep_caps = ['I', 'Guthrie', 'Mr']

to_parse = [3]
#success = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 27, 29]
#to_parse = success

if len(to_parse) == 0:
    to_parse.extend(range(1,70))
print(to_parse)

sentences = []
with open("train_sent.txt", "r") as f:
    for i, line in enumerate(f):
        if i+1 in to_parse:
            processed_line = line.replace('.', '')
            processed_line = processed_line.replace('!', '')
            processed_line = processed_line.replace('"', ' " ')
            processed_line = processed_line.replace(',',' ,')
            processed_line = processed_line.replace(';',' ;')
            processed_line = processed_line.replace("won't",'will not')
            processed_line = processed_line.replace("it's",'it is')
            processed_line = processed_line.replace("It's",'it is')
            processed_line = processed_line.replace("I've",'I have')
            processed_line = processed_line.replace("n't"," n't")
            processed_line = processed_line.replace("CD's","CDs")
            processed_line = processed_line.replace("'s", " 's").split()
            if processed_line[0] not in keep_caps:
                processed_line[0] = processed_line[0].lower()
            sentences.append([i+1, line, processed_line])


with open("my-grammar.txt", "r") as f:
    data = f.read()
grammar = grammar.FeatureGrammar.fromstring(data)
print(grammar.productions())

parser = FeatureEarleyChartParser(grammar, trace=2)

parsed = []
unparsed = []

for i, original_line, sent in sentences:
    try:
        trees = parser.parse(sent)
        all_trees = [x for x in trees]

        if len(all_trees) == 0:
            print(f'Failed to parse {i}')
            unparsed.append([i, original_line])
        else:
            #for tree in all_trees:
            #    print(tree)
            parsed.append([i, original_line, sent, all_trees])
    except Exception as e:
        print(e)
        unparsed.append([i, original_line])

print('-------------Parsed--------------')
for p in parsed:
    print(p[0])
print('---------------Failed to parse---------------')
for p in unparsed:
    print(p[0]) 

print('\n')
print(f'Total parsed: {len(parsed)} or {len(parsed) / 8}%')
print(f'Total unparsed: {len(unparsed)} or {len(unparsed) / 8}%')

with open('Good_D2.txt', 'w') as f:
    for i, original_line, sent, all_trees in parsed:
        f.write('\n---------------------------------------\n')
        f.write(f'Sentece {i}: {original_line}')
        f.write(f'Num of trees: {len(all_trees)}')
        for tree in all_trees:
            f.write('\n')
            f.write(str(tree))
            f.write('\n')

with open('False_D2.txt', 'w') as f:
    for i, original_line in unparsed:
        f.write(f'Sentece {i}: {original_line}')
