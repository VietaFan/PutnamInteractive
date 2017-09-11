import os
def getProblem(year, problem, writing=False, f=None):
    problem = problem.upper()
    if f is None:
        f = open('%s.tex' % (year),'r')
        closing = True
    else:
        closing = False
    on = 0
    if not writing:
        probStr = '%s %s.\n' % (year, problem)
    else:
        probStr = ''
    for line in f:
        if '\\item['+problem[0] in line and problem[1] in line:
            on = 1
            if writing:
                line = '\\item['+str(year)+' '+line[6:]
        if on and line.strip(' \t\n') == '':
            break
        if on:
            probStr += line
    if closing:
        f.close()
    return probStr
def getAllProblems(year):
    f = open('%s.tex' % (year),'r')
    L = []
    for line in f:
        L.append(line)
    f.close()
    probs = {}
    for c in 'AB':
        for n in range(1,7):
            probs[c+str(n)] = getProblem(year, c+str(n), f=L)
    return probs
def getEveryProblem():
    D = {}
    for year in range(1995, 2017):
        A = getAllProblems(year)
        for x in A:
            D[year,x] = A[x]
    return D
def loadData(filename):
    f = open(filename,'r')
    data = []
    for line in f.readlines()[2:]:
        line = line.split()
        data.append((int(line[0]), line[1], float(line[2]), float(line[3]), float(line[4])))
    f.close()
    return sorted(data)
def displayStats(problems):
    diffs = [x[2] for x in problems]
    diffs = sorted(diffs)
    n = len(diffs)
    print('Statistics on Pct. Solved')
    print('=========================')
    print('N = %s' % (n))
    print('mean = %s' % (round(sum(diffs)/n,2)))
    if n%2:
        print('median = %s' % (round(diffs[(n-1)//2],2)))
    else:
        print('median = %s' % (round((diffs[n//2]+diffs[n//2-1])/2,2)))
    print('Q1 = %s' % (round(diffs[n//4-1],2)))
    print('Q3 = %s' % (round(diffs[n-n//4-1],2)))
pset = ''
psetName = ''
probMemo = []
allProbs = getEveryProblem()
allProbsSplit = {}
for x in allProbs:
    allProbsSplit[x] = set(allProbs[x].split())
def processQuery(query, dataset):
    global pset,psetName,probMemo
    candidates = dataset[:]
    words = [w.lower().strip() for w in query.split()]
    if words[0] == 'help' or words[0] == 'commands':
        print('Commands List')
        print('Limiting commands:')
        print('\"year <startYear>-<endYear>\" or \"year <targetYear>\"')
        print('"pctsolved <minPct>-<maxPct>"')
        print('"sloppiness <minVal>-<maxVal>"')
        print('"number <problemNumber>" or "number in <probNum1>,<probNum2>,...,<probNumN>"')
        print('"partial <minVal>-<maxVal>"')
        print('Ordering commands:')
        print('easiest, hardest, newest, oldest, top, bottom')
        print('Viewing commands:')
        print('"get/view/show/print <yearNum> <probNum>"')
        print('stats <set of problems>')
        print('Problemset commands:')
        print('makepset <filename>')
        print('addprob <year> <probNum>')
        print('addprobs')
        print('writepset')
        print('openpset <filename>')
        return
    for i in range(len(words)-1):
        if i > 0 and words[i-1] in ['top', 'bottom'] or\
           i > 1 and words[i-1].isnumeric() and words[i-2] in ['top', 'bottom']:
            continue
        if words[i] == 'year':
            s = words[i+1]
            if '-' in s:
                low,high = s.split('-')
                remaining = []
                for x in candidates:
                    if x[0] in range(int(low),int(high)+1):
                        remaining.append(x)
                candidates = remaining
            else:
                year = int(s)
                remaining = []
                for x in candidates:
                    if x[0] == year:
                        remaining.append(x)
                candidates = remaining
        if words[i] == 'pctsolved':
            s = words[i+1]
            if '-' in s:
                low,high = s.split('-')
                remaining = []
                for x in candidates:
                    if x[2] >= float(low) and x[2] <= float(high):
                        remaining.append(x)
                candidates = remaining
            else:
                pct = float(s)
                remaining = []
                for x in candidates:
                    if x[2] == pct:
                        remaining.append(x)
                candidates = remaining
        if words[i] == 'sloppiness':
            s = words[i+1]
            if '-' in s:
                low,high = s.split('-')
                remaining = []
                for x in candidates:
                    if x[3] >= float(low) and x[3] <= float(high):
                        remaining.append(x)
                candidates = remaining
            else:
                avgslop = float(s)
                remaining = []
                for x in candidates:
                    if x[4] == avgslop:
                        remaining.append(x)
                candidates = remaining
        if words[i] == 'partial':
            s = words[i+1]
            if '-' in s:
                low,high = s.split('-')
                remaining = []
                for x in candidates:
                    if x[4] >= float(low) and x[4] <= float(high):
                        remaining.append(x)
                candidates = remaining
            else:
                avgpart = float(s)
                remaining = []
                for x in candidates:
                    if x[4] == avgpart:
                        remaining.append(x)
                candidates = remaining
        if words[i] == 'number':
            if words[i+1] == 'in':
                L = words[i+2].split(',')
            else:
                L = [words[i+1]]
            remaining = []
            for x in candidates:
                if x[1].lower() in L:
                    remaining.append(x)
            candidates = remaining
        if words[i] == 'about.or':
            remaining = []
            L = words[i+1].split(',')
            for x in candidates:
                for w in L:
                    if w.lower() in allProbsSplit[x[0],x[1]] or w.title() in allProbsSplit[x[0],x[1]]:
                        remaining.append(x)
                        break
            candidates = remaining
        if words[i] == 'about' or words[i] == 'about.and':
            remaining = []
            L = words[i+1].split(',')
            for x in candidates:
                bad = False
                for w in L:
                    if w.lower() not in allProbsSplit[x[0],x[1]] and w.title() not in allProbsSplit[x[0],x[1]]:
                        bad = True
                        break
                if not bad:
                    remaining.append(x)
            candidates = remaining
            
    dispStats = False
    onlyStats = False
    if words[0] == 'stats':
        words = words[1:]
        if words[0] == 'only':
            words = words[1:]
            onlyStats = True
        dispStats = True
        if len(words) == 0:
            displayStats(probMemo)
            return
    if words[0] == 'easiest':
        L = sorted([(x[2],x[0],x[1],x[3],x[4]) for x in candidates],reverse=1)
        if len(words) > 1 and words[1].isnumeric():
            n = min(int(words[1]),len(candidates))
        elif len(words) > 1 and '-' in words[1]:
            a,b = words[1].split('-')
            a = int(a); b = int(b)
            L = L[a-1:]
            n = b-a+1
        else:
            n = len(candidates)
        if not onlyStats:
            print('Problem  %Solved  Sloppiness  Partial')
            print('=======  =======  ==========  =======')
            for i in range(n):
                print('{1} {2}  {0:6.2f}%  {3:10.2f}  {4:7.2f}'.format(*L[i]))
        probMemo = []
        for x in L[:n]:
            probMemo.append((x[1],x[2],x[0],x[3],x[4]))
    elif words[0] == 'hardest':
        L = sorted([(x[2],x[0],x[1],x[3],x[4]) for x in candidates],reverse=0)
        if len(words) > 1 and words[1].isnumeric():
            n = min(int(words[1]),len(candidates))
        elif len(words) > 1 and '-' in words[1]:
            a,b = words[1].split('-')
            a = int(a); b = int(b)
            L = L[a-1:]
            n = b-a+1
        else:
            n = len(candidates)
        if not onlyStats:
            print('Problem  %Solved  Sloppiness  Partial')
            print('=======  =======  ==========  =======')
            for i in range(n):
                print('{1} {2}  {0:6.2f}%  {3:10.2f}  {4:7.2f}'.format(*L[i]))
        probMemo = []
        for x in L[:n]:
            probMemo.append((x[1],x[2],x[0],x[3],x[4]))
    elif words[0] == 'newest':
        candidates.reverse()
        if len(words) > 1 and words[1].isnumeric():
            n = min(int(words[1]),len(candidates))
        elif len(words) > 1 and '-' in words[1]:
            a,b = words[1].split('-')
            a = int(a); b = int(b)
            L = L[a-1:]
            n = b-a+1
        else:
            n = len(candidates)
        if not onlyStats:
            print('Problem  %Solved  Sloppiness  Partial')
            print('=======  =======  ==========  =======')
            for candidate in candidates[:n]:
                print('{0} {1}  {2:6.2f}%  {3:10.2f}  {4:7.2f}'.format(*candidate))
        probMemo = candidates[:n]
    elif words[0] == 'oldest':
        if not onlyStats:
            print('Problem  %Solved  Sloppiness  Partial')
            print('=======  =======  ==========  =======')
        if len(words) > 1 and words[1].isnumeric():
            n = min(int(words[1]),len(candidates))
        elif len(words) > 1 and '-' in words[1]:
            a,b = words[1].split('-')
            a = int(a); b = int(b)
            L = L[a-1:]
            n = b-a+1
        else:
            n = len(candidates)
        if not onlyStats:
            for candidate in candidates[:n]:
                print('{0} {1}  {2:6.2f}%  {3:10.2f}  {4:7.2f}'.format(*candidate))
        probMemo = candidates[:n]
    elif words[0] in ['all', 'year', 'pctsolved', 'sloppiness', 'partial', 'number']:
        if not onlyStats:
            print('Problem  %Solved  Sloppiness  Partial')
            print('=======  =======  ==========  =======')
            for candidate in candidates:
                print('{0} {1}  {2:6.2f}%  {3:10.2f}  {4:7.2f}'.format(*candidate))
        probMemo = candidates[:]
    elif words[0] in ['view', 'show', 'print', 'get']:
        print(getProblem(words[1],words[2]))
    elif words[0] == 'top':
        if len(words) > 1 and words[1].isnumeric():
            n = min(int(words[1]),len(candidates))
            del words[1]
        else:
            n = len(candidates)
        if words[1] == 'pctsolved':
            L = [(x[1],x[2],x[0],x[3],x[4]) for x in sorted([(x[2],x[0],x[1],x[3],x[4]) for x in candidates],reverse=1)]
        elif words[1] == 'sloppiness':
            L = [(x[1],x[2],x[3],x[0],x[4]) for x in sorted([(x[3],x[0],x[1],x[2],x[4]) for x in candidates],reverse=1)]
        elif words[1] == 'partial':
            L = [(x[1],x[2],x[3],x[4],x[0]) for x in sorted([(x[4],x[0],x[1],x[2],x[3]) for x in candidates],reverse=1)]
        if not onlyStats:
            print('Problem  %Solved  Sloppiness  Partial')
            print('=======  =======  ==========  =======')
            for i in range(n):
                print('{0} {1}  {2:6.2f}%  {3:10.2f}  {4:7.2f}'.format(*L[i]))
        probMemo = L[:n]
    elif words[0] == 'bottom':
        if len(words) > 1 and words[1].isnumeric():
            n = min(int(words[1]),len(candidates))
            del words[1]
        else:
            n = len(candidates)
        if words[1] == 'pctsolved':
            L = [(x[1],x[2],x[0],x[3],x[4]) for x in sorted([(x[2],x[0],x[1],x[3],x[4]) for x in candidates],reverse=0)]
        elif words[1] == 'sloppiness':
            L = [(x[1],x[2],x[3],x[0],x[4]) for x in sorted([(x[3],x[0],x[1],x[2],x[4]) for x in candidates],reverse=0)]
        elif words[1] == 'partial':
            L = [(x[1],x[2],x[3],x[4],x[0]) for x in sorted([(x[4],x[0],x[1],x[2],x[3]) for x in candidates],reverse=0)]
        if not onlyStats:
            print('Problem  %Solved  Sloppiness  Partial')
            print('=======  =======  ==========  =======')
            for i in range(n):
                print('{0} {1}  {2:6.2f}%  {3:10.2f}  {4:7.2f}'.format(*L[i]))
        probMemo = L[:n]
    elif words[0] == 'makepset':
        if len(words) > 1 and words[1][-4:] == '.tex':
            psetName = os.getcwd() + '\\' + words[1]
            pset = '''\\documentclass{article}
\\usepackage{mathptmx,amsmath,amssymb}
\\setlength{\\pdfpagewidth}{8.5 in}
\\setlength{\\pdfpageheight}{11 in}
\\setlength{\\oddsidemargin}{-0.5 in}
\\setlength{\\evensidemargin}{-0.5 in}
\\setlength{\\textwidth}{7.5 in}
\\setlength{\\topmargin}{-1 in}
\\setlength{\\footskip}{0.9 in}
\\setlength{\\textheight}{10 in}
\\begin{document}
\\title{%s}
\\maketitle
\\newcommand{\RR}{\mathbb{R}}
\\begin{itemize}''' % (words[1][:-4])
        else:
            raise RuntimeError('Invalid command!')
    elif words[0] == 'addprob':
        pset += getProblem(words[1],words[2],True)+'\n'
        for x in candidates:
            if x[0] == int(words[1]) and x[1] == words[2].upper():
                pset += '\n$(%s,%s,%s)$\n' % (x[2],x[3],x[4])
                break
    elif words[0] == 'writepset':
        pset += '\\end{itemize}\\end{document}'
        print(psetName)
        f = open(psetName,'w')
        f.write(pset)
        f.close()
        os.system('pdflatex -interaction=nonstopmode "%s"' % (psetName))
    elif words[0] == 'openpset':
        try:
            os.system(words[1][:-4]+'.pdf')
        except:
            print('The problemset "%s" could not be opened.' % (words[1][:-4]+'.pdf'))
            
    elif words[0] == 'addprobs':
        pass
    else:
        raise RuntimeError('Invalid command!')
    if 'addprobs' in words:
        for problem in probMemo:
            pset += getProblem(str(problem[0]),problem[1],True)+'\n'
            pset += '\n$(%s,%s,%s)$\n' % (problem[2],problem[3],problem[4])
    if dispStats:
        displayStats(probMemo)
def main():
    print('========== Putnam Database ==========')
    print('Loading data...')
    dataset = loadData('putnamData.txt')
    print('Dataset loaded.')
    while True:
        query = input('>')
        if query in ['quit', 'exit']:
            break
        #try:
        processQuery(query,dataset)
        #except:
        #    print('Error: Invalid query.')
    print('Exiting Putnam Database... Bye!')
main()
