def mylist(the_list=None):
    if the_list is None:
        the_list = []
    the_list.append("hi")
    print(the_list)


mylist()
mylist()
mylist()


from dataclasses import dataclass


@dataclass
class File:
    """A class for storing data about a file."""

    name: str
    extension: str
    path: str
    size: str
    created: int
    modified: str
    accessed: str


x = File("test", "test", "test", "test", "test", "test", "test")

print(x)
