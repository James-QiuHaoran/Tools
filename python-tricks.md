## Python Tricks

### Auto `requirements.txt` Generation

```
pip install pipreqs
pipreqs /path/to/project
```

### Interchange Values Between Two Variables

```
x, y = 10, 20
print(x, y)

x, y = y, x
print(x, y)

#1 (10, 20)
#2 (20, 10)
```

### Chain of Comparison

```
n = 10
result = 1 < n < 20
print(result)

# True

result = 1 > n <= 9
print(result)

# False
```

### If-Sels Assignment

```
x = 10 if (y == 9) else 20
x = (classA if y == 1 else classB)(param1, param2)
[m**2 if m > 10 else m**4 for m in range(50)]
```

### List Assignment

```
testList = [1,2,3]
x, y, z = testList

print(x, y, z)

#-> 1 2 3
```

### Printing Path of Imported Library

```
import threading
import socket

print(threading)
print(socket)

#1- <module 'threading' from '/usr/lib/python2.7/threading.py'>
#2- <module 'socket' from '/usr/lib/python2.7/socket.py'>
```

### Temporary Variable for Last Expression

```
>>> 2 + 1
3
>>> _
3
>>> print _
3
```

### Dictionary/Set Comprehension

```
testDict = {i: i * i for i in xrange(10)}
testSet = {i * 2 for i in xrange(10)}

print(testSet)
print(testDict)

#set([0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
#{0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}
```

### Debugging Scripts - Set Breaking Points

```
import pdb
pdb.set_trace()
```

### Inspect Objects

```
test = [1, 3, 5, 7]
print(dir(test))
```

### Check Python Version At Runtime

```
import sys

# or you can use sys.version_info >= (3, 5)
if not hasattr(sys, "hexversion") or sys.hexversion != 50660080:
    print("Sorry, you aren't running on Python 3.5n")
    print("Please upgrade to 3.5.n")
    sys.exit(1)

# print Python version in a readable format.
print("Current Python version: ", sys.version)
```

### Use Splat Operator to Unpack Parameters

```
def test(x, y, z):
    print(x, y, z)

testDict = {'x': 1, 'y': 2, 'z': 3}
testList = [10, 20, 30]

test(*testDict)
test(**testDict)
test(*testList)

#1-> x y z
#2-> 1 2 3
#3-> 10 20 30
```

### Check Memory Usage for Variables

```
import sys

x=1
print(sys.getsizeof(x))
```

In Python 2.7, a 32-bit integer uses 24 bytes, while in Python 3.5, it uses 28 bytes.
