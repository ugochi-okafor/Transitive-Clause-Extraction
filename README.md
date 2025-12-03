# Transitive-Clause-Extraction
This project explores different ways of identifying simple transitive clauses in sentences, using both dependency-tree methods and a linear word-order method. The recursive tree search walks through every subtree in a pyconll dependency tree and applies an extract function to each one; while the linear method checks NOUN–VERB–NOUN sequences. 
