# PutnamInteractive
Allows users to select sets of Putnam problems via the command-line, filtering by year, difficulty, and other characteristics, and creates LaTeX documents consisting of the desired problems.

To run the program, place the Putnam exam source files 1996.tex through 2016.tex from http://kskedlaya.org/putnam-archive/, as well as putnamData.txt, in the same directory as putnamInteractive.py and run with 'python putnamInteractive.py'. After the program starts, type 'help' for a list of possible commands. The command 'writepset' and 'openpset', which write the problemset to a LaTeX file and compile to PDF, and open the PDF file, respectively, require pdflatex to be installed on the system. 

The problems are ordered using three different metrics. The first, pctsolved, is the percentage of the top ~200 contestants scoring at least 8 points on the problem. The second, sloppiness, is the average number of points lost by contestants scoring between 8 and 10. The third, partial, is the average number of points scored by contestants scoring between 0 and 2 on the problem. This data is stored in putnamData.txt, which was compiled from http://kskedlaya.org/putnam-archive/putnam2016stats.html (and similar pages for other years).

Here are some example inputs and outputs from the program:

```========== Putnam Database ==========
Loading data...
Dataset loaded.
>makepset myproblemset.tex
>hardest 3 year 2016
Problem  %Solved  Sloppiness  Partial
=======  =======  ==========  =======
2016 A6    1.07%        0.00     0.02
2016 A5   17.65%        0.18     0.18
2016 B5   20.32%        0.58     0.11
>addprobs
>addprob 2015 B6
>top 5 partial year 2000-2009 pctsolved 30-40
Problem  %Solved  Sloppiness  Partial
=======  =======  ==========  =======
2007 A1   31.55%        1.02     1.45
2009 B2   32.50%        0.05     1.03
2000 A1   38.46%        0.25     0.68
2002 A5   39.05%        1.10     0.40
2003 B1   35.82%        0.19     0.26
>addprobs
>writepset
C:\Users\...\Documents\...\Putnam\myproblemset.tex
This is pdfTeX, Version 3.14159265-2.6-1.40.18 (MiKTeX 2.9.6350 64-bit)
entering extended mode
... pdflatex output omitted for brevity ...
Output written on myproblemset.pdf (1 page, 70298 bytes).
Transcript written on myproblemset.log.
>openpset myproblemset.tex
```

![alt text](https://github.com/VietaFan/PutnamInteractive/blob/master/myproblemset.pdf)
