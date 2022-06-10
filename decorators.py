def PrintEventName(func):

    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    async def inner1(*args, **kwargs):

        # storing time before function execution
        print(f'function called: {func.__name__} with args: {args}')
        await func(*args, **kwargs)

    return inner1
