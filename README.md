Delegation
==========
Delegation implements a DSL in Python that generates getters and setters
to delegate attribute access through one object to another.

Currently, this is simply implemented as code that you cam copy into your
own project (but see LICENSE) and is not an import package.

Usage Example
--------------
```python
from delegation import DelegatesAttrs


class Inner:
    color = None

    def say_hello(self):
        print('Hello from Inner!')


class Wrapper(DelegatesAttrs):
    delegate('color to inner', setter=True)
    delegate('say_hello to inner as say_hi')

    def __init__(self, inner):
        self.inner = inner


inner = Inner()
wrapper = Wrapper(inner)

wrapper.say_hi()
# Prints "Hello from Inner!"

wrapper.color = 'blue'
print(inner.color)
# Prints "blue"
```
