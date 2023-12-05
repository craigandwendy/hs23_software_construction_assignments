import sys
import json
from datetime import datetime
import random
import os


global_id = []


def do_addition(env, args):
    # return a + b
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return round(left + right, 2)


def do_abs(env, args):
    # return absolute value of a number ex.:
    # -1 -> 1
    # 20 -> 20
    # 0 -> 0
    assert len(args) == 1
    value = do(env, args[0])
    return round(abs(value), 2)


def do_subtraction(env, args):
    # return a - b
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return round(left - right, 2)


def do_multiplication(env, args):
    # return a * b
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return round(left * right, 2)


def do_division(env, args):
    # return a/b -> b != 0
    assert len(args) == 2
    assert args[1] != 0, "Error: Zero division!"
    left = do(env, args[0])
    right = do(env, args[1])
    return round(left / right, 2)


def do_power(env, args):
    # return a ** b
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return round(left ** right, 2)


def do_equal(env, args):
    # check a == b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left == right:
        return True
    return False


def do_largerequal(env, args):
    # check a >= b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left >= right:
        return True
    return False


def do_smallerequal(env, args):
    # check a <= b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left <= right:
        return True
    return False


def do_larger(env, args):
    # check a > b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left > right:
        return True
    return False


def do_smaller(env, args):
    # check a < b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left < right:
        return True
    return False


def do_notequal(env, args):
    # check a != b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left != right:
        return True
    return False


def do_is(env, args):
    # check a is b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left is right:
        return True
    return False


def do_is_not(env, args):
    # check a is not b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left is not right:
        return True
    return False


def do_in(env, args):
    # check a in b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left in right:
        return True
    return False


def do_not_in(env, args):
    # check a not in b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left not in right:
        return True
    return False


def do_and(env, args):
    # check a and b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left and right:
        return True
    return False


def do_or(env, args):
    # check a or b
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    left = do(env, args[0])
    right = do(env, args[1])
    if left or right:
        return True
    return False


def do_not(env, args):
    # check not a
    assert len(args) == 1, f"Expected 1 argument but received {len(args)} arguments!"
    left = do(env, args[0])
    return not left


def do_repeat(env, args):
    # for loop
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    assert isinstance(args[0], int), f"Expected integer type, but received invalid repeat type: {type(args[0])}!"
    assert args[0] > 0, f"Cannot repeat {args[0]} times"
    result = None
    for i in range(0, args[0]):
        do(env, args[1])


def do_while(env, args):
    # while loop
    # Use ["while", ["greater_equal", "a", "b"], ["seq", ["print", ["get", "a"]]]]
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    value = None
    while do(env, args[0]):
        value = do(env, args[1])
    return value


def do_set(env, args):
    # setting variables
    # ["set", "a", 5]
    assert len(args) == 2
    assert isinstance(args[0], str)
    variable_name = args[0]
    value = do(env, args[1])
    env_set(env, variable_name, value)  # insert key value into environment
    return value


def do_get(env, args):
    # getting variables
    # Use ["get", "a"]
    assert len(args) == 1
    assert isinstance(args[0], str), "Received wrong type"
    return env_get(env, args[0])  # -> assert checked in env_get()


def do_array(env, args):
    # Use ["array", 5] -> [None, None, None, None, None]
    assert len(args) == 1
    assert isinstance(args[0], int)
    assert args[0] > 0, f"Cannot create array of length {args[0]}"
    temp = []
    for i in range(args[0]):
        temp.append(None)
    return temp


def do_set_array_index(env, args):
    # Use ["set_array", array_name, index, value]
    assert len(args) == 3
    assert isinstance(args[0], str)
    arr = args[0]
    index = do(env, args[1])  # ["set_array_index", "my_arr", ["get", "a"], ["get", "my_string"]]
    val = do(env, args[2])  # ["set_array_index", "my_arr", ["get", "a"], ["get", "my_string"]]
    array = env_get(env, arr)  # [{"my_arr": [None, 1, None, 3], "my_var": 5}] -> [None, 1, None, 3]
    assert -1 * len(array) <= index < len(array), "Index out of range"  # [1,2,3,4,5,6] -> -6 <= index < 6
    for e in reversed(env):  # env = [{"a": [0,1,2], "b": [0,1,2]}] -> e = {"a": [0,1,2], "b": [0,1,2]}
        if arr in e:
            e[arr][index] = val  # e["a"][0] = 55 -> env = [{"a": [55,1,2], "b": [0,1,2]}]


def do_get_array_index(env, args):
    # Use ["array_index", array_name, index]
    # negative and positive index is accepted
    assert len(args) == 2
    assert isinstance(args[0], str)
    arr = args[0]
    index = do(env, args[1])  # ["get", a] -> 5
    array = env_get(env, arr)
    assert -1 * len(array) <= index < len(array), "Index out of range"  # [1,2,3,4,5,6] -> -6 <= index < 6
    return array[index]


def do_dictionary(env, args):
    # Use ["dictionary"]
    # set an empty dictionary inside env -> env["my_dict"] = {}
    assert len(args) == 0
    return {}


def do_set_key_value(env, args):
    # Use ["set_key_value", dict_name, key, value]
    assert len(args) == 3
    assert isinstance(args[0], str)  # a = {}
    variable_name = args[0]
    key = do(env, args[1])  # handle variables
    value = do(env, args[2])  # handle variables
    assert env_get(env, variable_name) is not False, f"Unknown variable {variable_name}"  # assert needed?
    for e in reversed(env):  # env = [{"a": {"k": "v"}, "b":{"k": "v"}}] -> e = {"a": {"k": "v"}, "b": {"k": "v"}}
        if variable_name in e:
            e[variable_name][key] = value  # e["a"]["k"] = 100 -> env = [{"a": {"k": 100}, "b":{"k": "v"}}]


def do_get_key_value(env, args):
    # Use ["get_key_value", dict_name, key]
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    variable_name = do(env, args[0])  # a = {} or a = b, b = {}
    key = do(env, args[1])
    assert env_get(env, variable_name) is not False, f"Unknown variable {variable_name}"  # assert needed?
    for e in reversed(env):  # env = [{"a": {"k1": "x"}, "b":{"k2": "y"}}] -> e = {"a": {"k1": "x"}, "b": {"k2": "y"}}
        if variable_name in e:  # variable_name = "a", key = "k1"
            return e[variable_name][key]  # returns x


def do_merge_dictionary(env, args):
    # Use ["set", new_dict_name, ["merge_dictionary", ["get", dict1], ["get", dict2] ] ]
    assert len(args) == 2, f"Expected 2 arguments but received {len(args)} arguments!"
    assert env_get(env, args[0][1]) is not False and isinstance(do(env, args[0]), dict)  # check if dict exists
    assert env_get(env, args[1][1]) is not False and isinstance(do(env, args[1]), dict)  # check if dict exists

    d1 = do(env,args[0])  # get dictionary
    d2 = do(env,args[1])  # get dictionary

    return d1|d2


def do_class(env, args):
    # Defining Classes
    assert len(args) == 2
    value = {"_type": "class", "_parent": args[0]}
    do(env, args[1])

    def _inner(val):
        # Setting class methods
        if isinstance(val, list):
            for i in range(len(val)):
                if isinstance(val[i], str) and "_new" in val[i]:
                    value["_new"] = val[i]
                elif isinstance(val[i], str) and "fun." in val[i]:
                    value[val[i][val[i].find("_") + 1:]] = val[i]
                else:
                    _inner(val[i])
    _inner(args[1])
    return value


def do_instance(env, args):
    # ["set", "my_circle", ["instance", "Circle", [name, radius, color, ...]]]
    assert env_get(env, args[0]) is not False, f"Undefined class variable {args[0]}"
    class_dict = env_get(env, args[0])
    args_list = [class_dict["_new"]]
    for e in args[1]:
        args_list.append(e)
    instance_dict = do_call(env, args_list)
    return instance_dict


def do_seq(env, args):
    assert len(args) > 0
    result = None
    for item in args:
        result = do(env, item)
    return result


def do_print(env, args):
    # Use ["print", ["a", "b", "c"]]
    assert len(args) == 1, "Expected an argument"
    assert len(args[0]) > 0, f"Cannot print {len(args[0]) -1} elements"
    res = ""
    for e in args[0]:
        res += f"{do(env, e)}"
    print(res)


def do_if(env, args):
    assert len(args) == 3, f"Too little arguments"
    statement = do(env, args[0])
    if statement is True:
        do(env, args[1])
    else:
        do(env, args[2])


def do_function(env, args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["function", params, body]


def do_call(env, args):
    assert len(args) >= 1
    name = do(env, args[0])
    arguments = args[1:]
    # eager evaluation
    values = [do(env, arg) for arg in arguments]

    func = env_get(env, name)
    assert isinstance(func, list)
    assert func[0] == "function"
    func_params = func[1]
    assert len(func_params) == len(values)

    # inheritance evaluation
    if func_params[0] == "self":  # check if instance is called
        # check if inheritance is valid
        class_name = env_get(env, values[0])["_class"]

        def _inner(cls_name):
            # helper function for checking correct inheritance
            if cls_name != "None":
                if name in env_get(env, cls_name).values():
                    pass
                else:
                    return _inner(env_get(env, cls_name)["_parent"])
            else:
                raise AssertionError("Invalid inheritance")
        _inner(class_name)

    local_frame = dict(zip(func_params, values))
    env.append(local_frame)
    body = func[2]
    result = do(env, body)
    env.pop()

    return result


def env_get(env, name):
    assert isinstance(name, str)
    key = name
    for e in reversed(env):
        if key in e:
            return e[key]  # returns value of key

    assert False, f"Unknown variable name {name}"


def env_set(env, name, value):
    assert isinstance(name, str)
    key = name
    env[-1][key] = value


def list_iterator(my_list):
    # recursive iterating through a list
    if isinstance(my_list, list):
        for e in my_list:
            if isinstance(e, list):
                if "call" in e:
                    return get_name(e)  # get name of called function
                else:
                    list_iterator(e)
    if isinstance(my_list, str):
        return my_list if "fun." in my_list else False  # get called class methods
    return False


def get_name(l):
    # lists that contain "function" and were called
    if isinstance(l, str):
        if "fun." in l:  # already found in list_iterator
            return None
        return l
    elif isinstance(l, list):
        return get_name(l[1])
    else:
        return None


def file_logging(my_string):
    # write in .log file
    try:
        with open(sys.argv[3], "a") as log_file:
            log_file.write("\n"+my_string)
    except:
        pass


def trace(func):
    # tracing functions and methods that were defined and called in the .gsc file
    def _inner(*args, **kwargs):
        my_id = next(num for num in iter(lambda: random.randint(100000, 999999), None) if num not in global_id)  # setting a unique id
        global_id.append(my_id)
        ele = list_iterator(args[1])
        if ele:
            file_logging(f"{my_id},{ele},start,{datetime.now()}")  # check-in
        res = func(*args, **kwargs)  # run the function
        if ele:
            file_logging(f"{my_id},{ele},stop,{datetime.now()}")  # check-out
        return res
    return _inner


@trace
def do(env, expr):
    if isinstance(expr, int) or isinstance(expr, bool) or isinstance(expr, float):
        return expr
    if isinstance(expr, str) and not expr in OPS:
        return expr
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    # func = do_...

    func = OPS[expr[0]]
    # run do_... function
    return func(env, expr[1:])  # ex. return do_abs(env, expr[1:])


OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}  # OPS = {"abs": do_abs, "add": do_add, "set": do_set, "get": do_get, "seq": do_seq}


def main():
    # make sure to start with clean environment
    try:
        os.remove(sys.argv[3])
    except:
        pass

    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as reader:
            program = json.load(reader)
        assert isinstance(program, list)
        env = [{}]
        result = do(env, program)
        print(f"=> {result}")
    elif len(sys.argv) == 4:
        assert sys.argv[2] == "--trace", f"Invalid argument, expected --trace got {sys.argv[2]}"
        with open(sys.argv[3], "a") as f:
            f.write("id,function_name,event,timestamp")
        with open(sys.argv[1], "r") as reader:
            program = json.load(reader)
        assert isinstance(program, list)
        env = [{}]
        result = do(env, program)
        print(f"=> {result}")
    else:
        raise AssertionError("Invalid number of arguments")


if __name__ == "__main__":
    main()
