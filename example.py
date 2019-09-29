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

import delegation

print(dir(Wrapper.say_hi))
