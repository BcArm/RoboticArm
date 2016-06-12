from numpy import matrix
from numpy.linalg import inv

A = matrix([[1,5,2,7],[1,1,3,31],[1,3,4,17],[1,1,1,1]])
B = matrix([[77,75,74,61],[35,39,36,41],[9.2,9.2,7.2,-20.8],[1,1,1,1]])
C = B*inv(A)

test = matrix([[1],[2],[3],[1]])


print C*test