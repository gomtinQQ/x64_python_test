
import time

def fibonacci(value):
  if value == 0 or value == 1:
    return 1
  return fibonacci(value - 1) + fibonacci(value - 2)

fibValue = 38

for i in range(0, 5):
  print('start fibonacci')
  start = time.time()
  result = fibonacci(fibValue)
  end = time.time()
  print('result(', i, '): ', result)
  print('elapsed time: ', end - start, 's')

d0=1
d1=2
d3=0
start = time.time()
for i in range(2, 38):
    d3=d0+d1
    d0=d1
    d1=d3
    pass
print('result(', d3, '): ')
end = time.time()
print('elapsed time: ', end - start, 's')
