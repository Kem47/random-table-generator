
# TOP PRIORITY

- [ ] Bug: 2 consecutive tables references do not resolve with a space in between them.
- [X] Bug: 2 consecutive elements, no space at the beginning of the line, brings the result of only the first one. (tested with number and table, in both orders)
- [x] Combine Boolean and Option into 1 feature:
    - Always require brackets
    - The first one in success
    - If the second part is left blank then it will just output nothing (replicating the feature of Option)
- [x] Running of this .py in terminal with input file or phrase - HOW?
- [ ] Add error handling for 'No table found' (try,else,finally)
    
    
# TODO

- [ ] Creat more options for number generation:
    - Allow Geometric, Uniform, Normal distributions.
    - Allow for uniform fraction - between 0 and 1.
    - Bake in default ranges for them in a dict form
    - Create syntax so that custom distribution discriptors can be input
- [ ] Loop limit
    
   
# DO LATER

- [ ] Rework replace if mapping[0][2] ... part. 
- [ ] Add logging
- [x] Change the process input file to called separately from __init__
- [ ] reattempt dict approach to patterns and getattr
- [ ] A tool for checking all the lines in all of the tables in input folder
- [ ] Add syntax for making something all caps.