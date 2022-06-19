y = lambda f: (lambda s: lambda n: f(s(s))(n))(lambda s: lambda n: f(s(s))(n))
print(y(lambda f: lambda n: 1 if n == 0 else f(n-1) * n)(6))
