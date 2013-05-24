import sys,json,MapReduce,pprint
from operator import *

# globals
mr = MapReduce.MapReduce()
matrixMult = []
maxI = 10
maxJ = 10

# record [matrix, i, j, value] 
def mapper(record):
  global maxI
  global maxJ

  if record[0] == 'a':
    i = record[1]
    for j in range(maxJ+1):
      mr.emit_intermediate((i, j), record)
  elif record[0] == 'b':
    j = record[2]
    for i in range(maxI+1):
      mr.emit_intermediate((i, j), record)
  else:
    pass

# key is (row,col) and values have to be operated on
def reducer(key, values):
  values = list(values)
  a_rows = filter(lambda x : x[0] == 'a', values)
  b_rows = filter(lambda x : x[0] == 'b', values)

  result = 0
  for a in a_rows:
    for b in b_rows:
      if (a[2]==b[1]):
        result += a[3] * b[3]

  # we dont emit here but save it to sort it later
  if (result != 0):
    matrixMult.append([key[0], key[1], result])

def main():
  global maxI
  global maxJ

  # First find max i, j range of the result
  matrix = open(sys.argv[1])
  lines = matrix.readlines()
  for line in lines:
    record = json.loads(line)
    if ((record[0] == 'a') & (maxI < record[1])):
      maxI=record[1]
    if ((record[0] == 'b') & (maxJ < record[2])):
      maxJ=record[2]

  #Now do the matrix Multiply using mapper/reducer
  matrix.seek(0)
  mr.execute(matrix, mapper, reducer)
  matrix.close()

  #Now sort the results and print it out
  #sortedMatrixMult = sorted(matrixMult, key=itemgetter(0,1))
  for element in matrixMult:
    print element

if __name__ == '__main__':
  main()
