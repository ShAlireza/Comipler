answers = []

with open('ins.txt', 'r') as file:
    l = file.readlines()
    for q in l:
        to_be_written = q.split('->')
        s1 = to_be_written[0].split()[1]
        s2 = to_be_written[1].split('|')
        for w in s2:
            answers.append(s1 + ' ' + w)

for w in answers:
    print(w)
