import inspect
from pprint import pprint

def private(prop_name):
    return "_" in prop_name


def repeat_property(path, prop_name):
    methods = path.split(".")
    if len(methods) < 2:
        return False

    return prop_name in methods[:-1]


def past_depth(path, depth):
    return len(path.split(".")) > depth


def is_exception(obj, prop_name):
    try:
        return issubclass(Exception, obj)
    except TypeError:
        return False


def no_args(method):
    try:
        spec = inspect.getargspec(method)
        passed_args = set(spec.args) - set(['self'])
        if len(passed_args) - len(spec.defaults) > 0:
            return False
    except TypeError:
        return True


def known_pesky(prop_name):
    for bad_substr in ["FIELD", "field"]:
        if prop_name.find(bad_substr) != -1:
            return True

    return prop_name in [
        "DoesNotExist", "MultipleObjectsReturned", "__doc__",
        "__eq__", "__lt__", "__gt__", "__init__", "__ne__", "__dict__",
        "__new__", "__getattribute__", "__getattr__", "__weakref__", "__ge__",
        "__subclasshook__", "__getitem__", "__hash__", "__cmp__",
        "__delattr__", "__setattr__", "__repr__", "__le__", "__module__",
        "__mod__", "__reduce__", "__sizeof__", "__self__", "__metaclass__",
        "__class__", "__format__", "__reduce_ex__", "_default_manager"]

def get_all_property_paths(obj, prefix=""):
    props = []
    for prop_name, prop in inspect.getmembers(obj):
        path = prefix +  prop_name
        if is_exception(prop, prop_name) or known_pesky(prop_name):
            continue

        if (
            not private(prop_name) and
            not repeat_property(path, prop_name) and
            not past_depth(path, 4) and
            not is_exception(prop, prop_name) and
            no_args(prop) and
            not known_pesky(prop_name) and
            not inspect.isabstract(prop) and
            not inspect.istraceback(prop) and
            not inspect.isgenerator(prop) and
            not inspect.ismodule(prop)
        ):
            #print path, prop_name, private(prop_name), repeat_property(path, prop_name)
            props += get_all_property_paths(prop, prefix + prop_name + ".")

        if not inspect.isclass(prop):
            props.append(path)

    return props

