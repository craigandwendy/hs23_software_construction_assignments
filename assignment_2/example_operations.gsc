["seq",
    ["set", "a", 5],
    ["set", "b", 9],
    ["set", "c", 10],
    ["set", "d", ["division", ["get", "a"], ["get", "b"]]],
    ["set", "e", ["multiplication", ["get", "c"], ["get", "d"]]],
    ["set", "f", ["power", ["get", "a"], 2]],
    ["print", ["f = ", ["get", "f"]]],
    ["set", "my_arr", ["array", 3]],
    ["set_array_index", "my_arr", 0, ["get", "d"]],
    ["set_array_index", "my_arr", 1, ["get", "e"]],
    ["set_array_index", "my_arr", 2, ["get", "f"]],
    ["print", [["get", "my_arr"]]],
    ["set", "i", 0],
    ["while", ["smaller", ["get", "i"], 3], ["seq",
        ["print", ["value at index ", ["get", "i"], " = ", ["get_array_index", "my_arr", ["get", "i"]]]],
        ["set", "i", ["addition", ["get", "i"], 1]]
        ]
    ],
    ["set", "my_dict1", ["dictionary"]],
    ["set", "my_dict2", ["dictionary"]],
    ["set_key_value", "my_dict1", "a", ["get", "my_arr"]],
    ["set_key_value", "my_dict1", "b", ["get", "f"]],
    ["set_key_value", "my_dict1", "c", 21],
    ["set_key_value", "my_dict2", "a", ["subtraction", ["get", "d"], 5]],
    ["set_key_value", "my_dict2", "b", 33],
    ["set_key_value", "my_dict2", "d", "I love Software Construction"],
    ["print", [["get", "my_dict1"], "\n", ["get", "my_dict2"]]],
    ["print", ["value at key d = ", ["get_key_value", "my_dict2", "d"]]],
    ["set", "merged_dict", ["merge_dictionary", ["get", "my_dict1"], ["get", "my_dict2"]]],
    ["print", ["merged dictionary = ", ["get", "merged_dict"]]]






]