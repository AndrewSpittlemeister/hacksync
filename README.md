# Hacksync

Do we really *need* async & await? Yeah, we probably do, thread startup time is no joke. But at least you don't need to write the line that starts up the event loop, I call that a productivity boost.

```python
from time import sleep

from hacksync import hacksync


@hacksync()
def func(data: str):
    sleep(0.1)
    print(f'in function {data}')
    sleep(1)
    return data

def main() -> None:

    print('calling functions...')

    res1 = func('a')
    res2 = func('b')
    res3 = func('c')

    print('calls made')

    print(f'res1: {res1.get()}')
    print(f'res2: {res2.get()}')
    print(f'res3: {res3.get()}')

    print("calls completed")


if __name__ == "__main__":
    main()
```

```
calling functions...
calls made
in function a
in function b
in function c
res1: a
res2: b
res3: c
calls completed
```