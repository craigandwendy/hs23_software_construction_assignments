["seq",
    ["set", "Shape",
        ["class", "None",
            ["seq",
                ["set", "shape_new",
                    ["function", ["name"],
                        ["seq",
                            ["set", "inst_dict", ["dictionary"]],
                            ["set_key_value", "inst_dict", "name", ["get", "name"]],
                            ["set_key_value", "inst_dict", "_class", "Shape"],
                            ["get", "inst_dict"]
                        ]
                    ]
                ],
                ["set", "fun.shape_density",
                    ["function", ["self", "weight"],
                        ["seq",
                            ["set", "myclass", ["get_key_value", ["get","self"], "_class"]],
                            ["set", "area_get", ["get_key_value", ["get","myclass"], "area"]],
                            ["division",["get","weight"], ["call", ["get","area_get"],["get","self"]]]
                        ]
                    ]
                ]
            ]
        ]
    ],

    ["set", "Circle",
        ["class", "Shape",
            ["seq",
                ["set", "circle_new",
                    ["function", ["name", "radius"],
                        ["seq",
                            ["set", "my_shpe", ["instance", "Shape", [["get", "name"]]]],
                            ["set", "my_crcle", ["dictionary"]],
                            ["set_key_value", "my_crcle", "radius", ["get", "radius"]],
                            ["set_key_value", "my_crcle", "_class", "Circle"],
                            ["set", "merged_dict", ["merge_dictionary", ["get", "my_shpe"], ["get", "my_crcle"]]],
                            ["get", "merged_dict"]
                        ]
                    ]
                ],
                ["set", "fun.circle_area",
                    ["function", ["self"],
                        ["seq",
                            ["set", "pi", 3.141592653],
                            ["multiplication", ["get", "pi"], ["power", ["get_key_value", ["get", "self"], "radius"], 2]]
                        ]
                    ]
                ]
            ]
        ]
    ],
    ["set", "Square",
        ["class", "Shape",
            ["seq",
                ["set", "square_new",
                    ["function", ["name", "side"],
                        ["seq",
                            ["set", "my_shape", ["instance", "Shape", [["get", "name"]]]],
                            ["set", "my_square", ["dictionary"]],
                            ["set_key_value", "my_square", "side", ["get", "side"]],
                            ["set_key_value", "my_square", "_class", "Square"],
                            ["set", "merged_dict", ["merge_dictionary", ["get", "my_shape"], ["get", "my_square"]]],
                            ["get", "merged_dict"]
                        ]
                    ]
                ],
                ["set", "fun.square_area",
                    ["function", ["self"],
                        ["seq",
                            ["set", "s", ["get_key_value", ["get", "self"], "side"]],
                            ["multiplication", ["get", "s"], ["get", "s"]]
                        ]
                    ]
                ]
            ]
        ]
    ],
    ["set", "ci", ["instance", "Circle", ["ci", 2]]],
    ["set", "sq", ["instance", "Square", ["sq", 3]]],

    ["set", "weight", 5],
    ["set", "res",
        ["addition",
            ["call", "fun.shape_density", "sq", ["get", "weight"]],
            ["call", "fun.shape_density", "ci", ["get", "weight"]]
        ]
    ],
    ["get", "res"]

]