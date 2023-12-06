# ASSIGNMENT 2 - Interpreter and Reporting
Software Construction HS23, University of Zurich, Supervision Prof. Dr. Bacchelli

Authors:
* Ece Zeynep Asirim
* Mara Miruna Bucur
* Smail Alijagic
***

# Table of Contents

### **[1. Introduction](#introduction)**

### **[2. Usage](#usage)**
* [2.1 General Usage](#generalusage)
* [2.2 Valid Call Examples](#validcalls)
* [2.3 Invalid Call Examples](#invalidcalls)
* [2.4 First Program](#firstprogram)

### **[3. Imports](#imports)**
* [3.1 Interpreter](#importinterpreter)
* [3.2 Reporting](#importreporting)

### **[4. Task 1: Implementation of New Functionalities](#implementation)**
#### **[4.1. Mathematical Operators and Logic Comparison](#math&logic)**
* [4.1.1 Mathematical Operators()](#math)
* [4.1.2 Logic Comparison()](#logic)

#### **[4.2. Iterating](#iterating)**
* [4.2.1 While Loop()](#while)
* [4.2.2 For Loop()](#for)

#### **[4.3. Variables and Data Types](#var&data)**
* [4.3.1 Setting Variables](#set)
* [4.3.2 Getting Variables](#get)
* [4.3.3 Printing Variables](#print)
* [4.3.3 Numeric, Boolean and String](#nbs)
* [4.3.4 Fixed Size Array](#arr)
* [4.3.5 Dictionary](#dict)

#### **[4.4. Functions](#func)**
* [4.4.1 Defining Functions](#deffunc)
* [4.4.2 Calling Functions](#callfunc)

### **[5. Task 2: Object System](#objsys)**

#### **[5.1 Implementation](#impl)**
  * [5.1.1 Class Definition and Object Instantiation](#classdef&objinst)
  * [5.1.2 Single Inheritance](#singleinher)
  * [5.1.1.3 Polymorphism](#polymorph)

#### **[5.2 Defining Classes](#defineclass)**
  * [5.2.1 Defining Shape Class](#setclass)
  * [5.2.2 Defining Square Class](#square)
  * [5.2.3 Defining Circle Class](#circle)
  * [5.2.4 Creating and Calling Objects with Class Methods](#callobj)

### **[6. Task 3: Tracing](#trace)**
#### **[6.1 Logging](#log)**
  * [6.1.1 Implementing the Decorator](#funtrace)
  * [6.1.2 Calling the Tracer](#tracer)

#### **[6.2 Reporting](#report)**
  * [6.2.1 Building the Reporter](#createreport)
  * [6.2.1 Calling the Reporter](#reportoruse)


<div id="introduction"/>

# 1. Introduction

---

The goal of this assignment is to expand the Little German Language (LGL) introduced in class and in order to support more basic operations (Task 1), classes (Task 2) and tracing (Task 3).  

<div id="usage"/>

# 2 Usage

---

<div id="generalusage"/>

### 2.1 General Usage
* In order to use the interpreter and the self written code. It is possible to run the code only, to trace the ran code or even to create a report of the ran code.

<div id="validcalls"/>

### 2.2 Valid Call Examples
* This commandline argument will run the commands given in example.gsc
```
python lgl_interpreter.py example.gsc
```
* This commandline argument runs the code in example.gsc and traces the functions that were defined and called inside example.gsc in example.log
```
python lgl_interpreter.py example.gsc --trace example.log
```
* Once the previous line was executed, it is possible to get a nice report of example.log
```
python reporting.py example.log
```

<div id="invalidcalls"/>

### 2.3 Invalid Call Examples
* Here are some invalid command line call examples
```
python lgl_interpreter.py  # missing example.gsc
python lgl_interpreter.py --trace  # missing example.gsc
python lgl_interpreter.py example.gsc --follow  # only --trace is valid
python lgl_interpreter.py example.gsc --trace  # missing example.log 
python reporting.py  # missing example.log
python reporting.py example.gsc  # should be example.log instead of example.gsc
```

* In case of error replace python with python3 (this is a common error on macOS):
```
python3 lgl_interpreter.py example.gsc 
# or
python3 lgl_interpreter.py example.gsc --trace example.log
# or
python3 reporting.py example.log
```

<div id="firstprogram"/>

### 2.4 First Program
* This should only show a first small program. While reading this document, it should become clearer what this little program does.
```
["seq",
    ["set", "dict1", ["dictionary"]],
    ["set", "my_int", 5],
    ["set", "i", 3],
    ["while", ["smaller", ["get", "i"], ["get", "my_int"]],
        ["set", "i", ["addition", ["get", "i"], 1]]
    ],
    ["set", "my_arr", ["array", 3]],
    ["set_array_index", "my_arr", 0, "hello"],
    ["set_array_index", "my_arr", 1, "world"],
    ["set_array_index", "my_arr", 2, "!"],
    ["set_key_value", "dict1", "a", 55],
    ["set_key_value", "dict1", "b", ["get", "my_arr"]],
    ["set_key_value", "dict1", "c", ["multiplication", ["get", "my_int"], 5]],
    ["print", [["get", "dict1"]]]
]
```

<div id="imports"/>

# 3. Imports

---

<div id="importinterpreter"/>

### 3.1 Interpreter
* **datetime** https://docs.python.org/3/library/datetime.html
* **json** https://docs.python.org/3/library/json.html
* **os** https://docs.python.org/3/library/os.html
* **random** https://docs.python.org/3/library/random.html
* **sys** https://docs.python.org/3/library/sys.html

<div id="importreporting"/>

### 3.2 Reporting
* **csv** https://docs.python.org/3/library/csv.html
* **datetime** https://docs.python.org/3/library/datetime.html
* **sys** https://docs.python.org/3/library/sys.html
* **tabulate** https://pypi.org/project/tabulate/ this is not from the Python standard library and has therefore to be installed.

<div id="implementation"/>

## 4. Task 1: Implementation of New Functionalities

---

<div id="math&logic"/>

### 4.1 Mathematical Operators and Logic Comparison

<div id="math"/>

#### 4.1.1 Mathematical Operators
| function name           | Mathematical Operation |
|-------------------------|------------------------|
| ```do_addition```       | +                      |
| ```do_abs```            | absolute               |
| ```do_subtraction```    | -                      |
| ```do_multiplication``` | *                      |
| ```do_division```       | /                      |
| ```do_power```          | **                     |
* The mathematical operators return the result rounded up to 2 values after comma, e.g. 1/8 = 0.13
```
# lgl syntax (takes the function name without do_)
["addition", 1, 2]
["multiplication", 4, 5]
```

<div id="logic"/>

#### 4.1.2 Logic Comparison
| function name         | Python Syntax |
|-----------------------|---------------|
| ```do_equal```        | ```==```      |
| ```do_largerequal```  | ```>=```      |
| ```do_smallerequal``` | ```<=```      |
| ```do_larger```       | ```>```       |
| ```do_smaller```      | ```<```       |
| ```do_notequal```     | ```!=```      |
| ```do_is```           | ```is```      |
| ```do_is_not```       | ```is not```  |
| ```do_in```           | ```in```      |
| ```do_not_in```       | ```not in```  |
| ```do_and```          | ```and```     |
| ```do_or```           | ```or```      |
| ```do_not```          | ```not```     |

```
# lgl syntax (takes the function name without do_)
["equal", 1, 1]
["in", 3, ["get", "my_arr"]]
```

<div id="iterating"/>

### 4.2 Iterating

<div id="while"/>

#### 4.2.1 While Loop
* The function ```do_while(env, args)``` takes two arguments. The first argument is a comparison, the second argument is the command.
```
# lgl syntax
["while",
    ["smaller", ["get", "a"], ["get", "b"]],
    ["addition", ["get", "a"], 1]
]

# Python syntax
while a < b:
    a += 1
```

<div id="for"/>

#### 4.2.2 For Loop
* The funcion ```do_repeat(env, args)``` takes two arguments. The first argument is a strictly positive integer, the second argument is the command.
```
# lgl syntax
["repeat", 3,
    ["addition", ["get", "a"], 1]
]

# Python syntax
for i in range(3):
    a += 1
```

<div id="var&data"/>

### 4.3 Variables and Data Types

<div id="set"/>

#### 4.3.1 Setting Variables
* Generally setting variables is done using the word ```set```. It is possible to set different data types.
```
["set", variable_name, value]  # used for numeric, boolean and string
["set", variable_name, [data_type]]  # used for array, dictionary and class
```

<div id="get"/>

#### 4.3.2 Getting Variables
* Using the word ```get``` the value of any variable will be returned.
```
["set", "a", 5]  # define a
["get", "a"]  # returns 5

["set", "my_dict", ["dictionary"]]  # defining my_dict
["get", "my_dict"]  # return {}
```

<div id="nbs"/>

#### 4.3.3 Numeric, Boolean and String
* Integer, float, Boolean and string data type variables can be set easily, without taking any extra arguments.
```
# setting integer
["set", "a", 5]  # python syntax: a = 5


# setting float
["set", "b", 5.5]  # python syntax: b = 5.5


# setting boolean
["set", "c", True]  # python syntax: c = True


# setting string
["set", "d", "Hello World!"]  # python syntax: d = "Hello World!"
```

<div id="arr"/>

#### 4.3.4 Fixed Size Array
* The interpreter can only handle fixed size arrays. Setting fixed size array takes some additional arguments.
```
# setting fixed size array
["set", "e", ["array", 3]]  # creates an empty array with length 3 -> [None, None, None]
```
* It is possible to set values at any valid index inside the array.
```
# change the value of array e at index -1 and 0
["set_array_index", "e", -1, "!"]  # e = [None, None, "!"]
["set_array_index", "e", 0, "Hello,"]  # e = ["Hello,", None, "!"]


# setting the value at an invalid index will raise an Assertion
["set_array_index", "e", 3, "???"]  # raises assert: Index out of range
```
* It is possible to get the value at any valid index of an array.
```
# getting the value at index -2 and 0
["get_array_index", "e", 0]  # returns "Hello,"
["get_array_index", "e", -2]  # returns None


# getting the value of an invalid index will raise an Assertion
["get_array_index", "e", 20]  # raises assert: Index out of range
```

<div id="dict"/>

#### 4.3.5 Dictionary
* The interpreter can only set empty dictionaries.
```
# setting an empty dictionary
["set", "f", ["dictionary"]]  # creates an empty dictionary -> {}
```
* It is possible to set keys and values. Dictionaries can take any datatype (only those that are supported by the interpreter) as value. As key it can take variables.
```
# setting a key and a value
["set_key_value", "f", "my_key", "my_val"]  # f = {"my_key": "my_val"}


# setting the variable d (chapter 6.3) as key and variable e (chapter 6.4) as value
["set_key_value", "f", ["get", "d"], ["get", "e"]]  # f = {"my_key": "my_val", d:e} -> {"my_key": "my_value", "Hello World!": ["Hello,", None, "!"]}
```
* Another important function is merging dictionaries. Using the ```|``` operator two dictionaries are being merged into a new one (https://www.geeksforgeeks.org/python-merging-two-dictionaries/).
```
["seq",
    ["set", "dict1", ["dictionary"]],
    ["set", "dict2", ["dictionary"]],
    ["set", "my_arr", ["array", 3]],
    ["set_array_index", "my_arr", 0, "hello"],
    ["set_array_index", "my_arr", 1, "world"],
    ["set_array_index", "my_arr", 2, "!"],  # ["hello", "world", "!"]
    ["set_key_value", "dict1", "a", 55],
    ["set_key_value", "dict1", "b", "hello"],
    ["set_key_value", "dict2", "c", ["get", "my_arr"]],
    ["set_key_value", "dict2", "d", 123],
    ["set", "merged_dict", ["merge_dictionary", ["get", "dict1"], ["get", "dict2"]]],
    ["get", "merged_dict"]  # returns {"a": "55", "b": "hello", "c": ["hello", "world", "!"], "d": 123}
]
```
<div id="func"/>

### 4.4 Functions

<div id="deffunc"/>

#### 4.4.1 Defining Functions
* It is possible to define functions. Functions consist of parameters and a body. A function is defined using the word ```function```.
```
# general form
["function", parameter, body]
```
* In order to be able to store the function and to call it a later point it is important to bind the function to a variable. This means we have to set a variable that will take a function as value.
```
["set", "get_cubes", ["function", ["a"], ["seq", ["power", ["get", "a"], 3]]]]
```
<div id="callfunc"/>

#### 4.4.2 Calling Functions
* Previously defined functions can be called. In order to store the return value we can just bind it to a variable.
```
["set", "res", ["call", "get_cubes", ["get", "a"]]]
```

<div id="task1design&use"/>

###  4.5 Design Decisions and Use

<div id="task1design"/>

#### 4.5.1 Design Decisions
- Each function mentioned above is designed to interpret and execute a specific type of operation. All functions are designed in a similar manner. They take two parameters:
  - _env_: the environment maintaining the state of variables.
  - _args_: a list of operands.

- Assertions are included to ensure:
  - Correct number of arguments for each function (e.g., `assert len(args) == 2`).
  - Variables are instances of the correct type (e.g., `

assert isinstance(name, str); assert isinstance(expr, list)`).

- The _do_ function is used as a dispatcher that handles different types of expressions by calling the appropriate function for every operation.

- The _env_ variable (evironment) represents a stack-like structure as a list of dictionaries, with each dictionary representing a scope. When a new block is entered, a new dictionary is added to the list, and when the block is exited, the dictionary is removed.

- The _env_set_ function assigns values to keys in the most recent scope, while _env_get_ retrieves values from the first dictionary in _env_ where the key is found, respecting scoping rules. This obeys the scoping rules where variables in inner scopes shadow those in outer scopes.
    * For instance, when a variable is accessed, the env is searched from the most recent scope (the end of the list) back to the outermost scope (the start of the list). The first occurrence of the variable name found in this search is used. This is the "shadowing" effect, where an inner scope's variable "shadows" (overrides) a variable with the same name in an outer scope.

<div id="task1use"/>

#### 4.5.2 Use
**Usage:** `python lgl_language.py example_operations.gsc`  
This file contains a series of operations processed by the interpreter:
- _seq_ facilitates sequential execution of multiple instructions.
- _set_ declares and initializes variables (e.g., `["set", "variable_name", "value_or_expression"]`).
- _print_ operation is used to output values to the console.  
- _array_ creates an array and _set_array_index_ sets values at specific indices, allowing to work with list data structures.  
- _dictionary_ and _set_key_value_ are used to creates dictionaries and sets key-value pairs. _merge_dictionary can be used to merge existing dictionaries.  

<div id="objsys"/>

# 5. Task 2: An Object System

---

<div id="impl"/>

### 5.1 Implementation  
The _lgl_interpreter.py_ script supports class definition, object instantiation, single inheritance, and polymorphism.

<div id="classdef&objinst"/>

#### 5.1.1 Class Definition and Object Instantiation  
_do_class_ function creates a new class definition. The function creates a dictionary "value" with 2 keys:  
   *  "__type_": set to "class", indicating this dictionary represents type class.  
   *  "__parent_": Stores the parent class name, if there is any. If there is no parent class, this will be set to None.

_do_instance_ instantiates an object, fetching the class definition and calling _do_call_ for the constructor. The function takes two arguments:
   *  Class name from which the object is to be instantiated.
   * Arguments to be passed to the class's constructor (the "_new" method).  
The function fetches the class definition from the environment using the function _env_get_, then creates a list of arguments for the constructor (including the special "_new" method), and then uses _do_call_ to invoke the constructor.


- _do_call_ handles function calls by their designated name. In the context of object instantiation, it evaluates the arguments and retrieves the function definition from the environment. If the function is a method of a class, the first argument is expected to be "self", referring to the instance itself.

<div id="singleinher"/>

#### 5.1.2 Single Inheritance  
Single inheritance is implemented using dictionaries to represent class definitions, including a reference to a parent class.  
As mentioned in class definition, the dictionary created by the _do_class_ function holds "_type" key to indicate it's a class and "_parent" key containing the name of the parent class from which this class should inherit from.  If a class is not derived from any other class, this "_parent" key is set to None (in the gsc file).  
When a method is called on an instance of a class, the interpreter first looks in the class's own dictionary. If the method is not found there, the interpreter will use the "_parent" key to check the parent class's dictionary for the method. This check is recursive: if the parent class also inherits from another class, the search continues up the inheritance chain until the method is found or no more parent classes are available.  

_check_up_ is a recursive helper function that verifies correct inheritance.  
If a class name is provided (not "None"), it verifies if a method is part of the class or its parents, supporting single inheritance. It traverses up the inheritance chain using the "_parent" references in class dictionaries. First, it looks up the method name in the current class's dictionary, and if not found, it recursively checks the parent class by looking up the "_parent" key in the class dictionary.

<div id="polymorph"/>

#### 5.1.3 Polymorphism  
Polymorphism is implemented through the concepts of method overriding and dynamic dispatch. Method overriding is a specific case of polymorphism that our interpreter supports, where a class can provide its own implementations of methods. Dynamic dispatch is the mechanism that enables this at runtime, deciding which method to call based on the object's type. This allows objects to be treated polymorphically where  different types of objects may respond to the same method call in their own implementation. Specific examples are given in the section "Task 2.2. Use".

When a method is called on an object, the _do_call_ function will look up the method name in the object's class. If the method is not found in the current class and the class inherits from another class ("_parent" is not "None"), the check_up function will be used to look up the method in the parent class, allowing for method overriding.

As explain below in more detail, both Circle and Square classes inherit from Shape and make use of the shape_density method, which is only defined in the Shape class. The shape_density method uses dynamic dispatch to call the area method of the object it's calculating the density for. This is an example of polymorphism, where shape_density expects any subclass of Shape to have an area method and doesn't need to know the specific class of the object. So when we calculate the density of sq and ci using shape_density, the script assumes that both have an area method since they are subclasses of Shape and the shape_density method can be applied to them polymorphically.
//notes to explain polymorphism
    * When we instantiate a Circle and then call ["call", "fun.circle_area", ["get", "ci"]], the interpreter would dynamically dispatch the call to the Circle's area method.  
    * Similarly, for the Square instance, ["call", "fun.square_area", ["get", "sq"]] would result in the execution of the Square's area method.  

<div id="polymorph"/>

<div id="defineclass"/>

### 5.2 Defining Classes  
**Use:** `python lgl_interpreter.py example_class.gsc`  

<div id="setclass"/>

#### 5.2.1 Define a Shape Class  
- Constructor `shape_new(name)` creates an instance with name and class properties.
```
["function", ["name"],
    ["seq",
        ["set", "inst_dict", ["dictionary"]],
        ["set_key_value", "inst_dict", "name", ["get", "name"]],
        ["set_key_value", "inst_dict", "_class", "Shape"],
        ["get", "inst_dict"]
    ]
]
```   
The constructor function _shape_new_ is defined to take a name argument. It creates an instance dictionary _inst_dict_, sets the name and _class keys (which are like instance variables) via _set_key_value_ method, and returns the instance dictionary.

- Method `shape_density(self, weight)` calculates density using the object's area method, demonstrating polymorphism.
``` 
["function", ["self", "weight"],
    ["seq",
        ["set", "myclass", ["get_key_value", ["get","self"], "_class"]],
        ["set", "area_get", ["get_key_value", ["get","myclass"], "area"]],
        ["division",["get","weight"], ["call", ["get","area_get"],["get","self"]]]
    ]
]
```
The _shape_density_ method is defined to take _self_ (the object instance) and _weight_. It retrieves the class name of the object _self_ from the dictionary and stores it as _myclass_. Then, the _area_ method is retrieved from that class (which is key in the class's dictionary). Finally, the density is calculated by dividing the weight of the object by the result of calling its area method. 

This method assumes that any object that it is called on will have an area method, which is a characteristic of polymorphism. The shape_density method can work with any object that has an area method, allowing different shapes to calculate density in a uniform manner, regardless of the specific type of shape.
The method does not need to know in advance whether self is a Circle, Square, or any other shape derived from Shape, just that it can respond to the area call, even though the specific implementation of area might differ between classes. Depending on whether self is a Circle or a Square, the correct area method is called (dynamic dispatch). This behavior is what allows for polymorphism, where the shape_density function can operate on any object that fits the expected interface.

<div id="square"/>

#### 5.2.2 Define a Square Class  
- Inherits from Shape
```
["set", "Square",
    ["class", "Shape",
        // rest of the code...
```  
Inheritance is declared by setting "Shape" as the parent class when defining Square. 

- Constructor `square_new(name, side)` merges Shape properties with Square-specific properties.
```
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
]
```
The _square_new_ function creates a new Shape instance and merges it with a dictionary for the Square instance, which includes the side property and overrides the _class to "Square". Dictionaries _my_shape_ (Shape instance) and _my_square_ (Square instance) are merged via _merge_dictionary_ method to create a full Square instance that inherits the properties of class Shape, 

- Method `square_area(self)` calculates the area of a square.
```
["set", "fun.square_area",
    ["function", ["self"],
        ["seq",
            ["set", "s", ["get_key_value", ["get", "self"], "side"]],
            ["multiplication", ["get", "s"], ["get", "s"]]
        ]
    ]
]
```
The _square_area_ method calculates the area of a square using the side property from the Square instance. _self_ is the Square instance on which the area method is called. "s" is the side length of the square, retrieved from the instance. The area is calculated as the square of side length.

The Square class is defined with a clear parent-child relationships using "class" operation to establish inheritance from Shape as the base class. Superclass properties are merged with subclass-specific attributes, ensuring a coherent inheritance structure.
The constructor of Squarefirst creates an instance of the parent Shape class. This is to ensures instances of Square to also have the properties and methods of the superclass Shape.
After creating a base Shape instance, the constructors merge additional subclass-specific properties into this instance. This approach allows subclass instances to extend the properties of the superclass instances, maintaining the relationship of inheritance.

Polymorphism is achieved by expecting all subclasses to adhere to a shared method contract. For example in the above section, the shape_density method assumes that the instance will have an area method regardless of its class. The shape_density method dynamically retrieves and calls the area method on the instance at runtime. This allows objects of "Square" to respond differently to the same method call (area), which is the essence of polymorphism (dynamic dispatch).

<div id="circle"/>

#### 5.2.3 Define a Circle Class  
- Inherits from Shape.
```
["set", "Circle",
    ["class", "Shape",
        // rest of the code...
```
Similar to Square, Circle is defined with Shape as its parent class, indicating inheritance.

- Constructor `circle_new(name, radius)` merges Shape properties with Circle-specific properties.
```
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
]
```
The constructor for Circle follows the same pattern as Square, creating a Shape instance and merging via _merge_dictionary_it with Circle-specific properties, such as radius.
First, a base instance of the Shape class is created to ensure the Circle inherits any Shape properties and methods which is stored in a temporary variable my_shape. Then, a separate dictionary is created to hold  properties specific to Circle such as radius. These two dictionaries are merged later, allowing Circle to override or extend the inherited properties of Shape. 
- Method `circle_area(self)` calculates the area of a circle.
```
["set", "fun.circle_area",
    ["function", ["self"],
        ["seq",
            ["set", "pi", 3.141592653],
            ["multiplication", ["get", "pi"], ["power", ["get_key_value", ["get", "self"], "radius"], 2]]
        ]
    ]
]
```
The circle_area method calculates the area of a circle using the radius property of the Circle instance and the variable pi.
Variable pi is set to the value and the circle area is calculated as pi times radius squared.  

Design decisions mentioned above for Square regarding inheritance and polymorphism are also followed for the Circle class.  
#### 5.2.4 Create New Objects and Return Sum  
A new Square object with side=3 and name=‘sq’ is created as follows:  
```
["set", "sq", ["instance", "Square", ["sq", 3]]]
```  

A new Circle object with radius=2 and name=‘ci’ is created as follows:  
```
["set", "ci", ["instance", "Circle", ["ci", 2]]]
```

The sum of the densities of the new objects sq and ci (with weight = 5) are calculated as follows:
```
["set", "weight", 5],
["set", "res",
    ["addition",
        ["call", "fun.shape_density", ["get", "sq"], ["get", "weight"]],
        ["call", "fun.shape_density", ["get", "ci"], ["get", "weight"]]
    ]
],
["get", "res"]
```  
The "res" variable is set to the sum of the densities and is calculated by calling the  `shape_density` function with each object. Finally, the result res is retrieved.

<div id="callobj"/>

### 5.3 Creating and Calling Object with Class Methods
- The script implements inheritance by allowing classes to specify a parent class. Constructors are special functions that create a new instance of the class. For Square and Circle, the constructors call the parent Shape constructor to ensure the object is properly initialized with Shape properties before adding their specific properties.  

- Methods are stored as functions in the class definitions and are looked up dynamically at runtime when they're called with an instance. The dynamic lookup supports the polymorphic behavior of methods like area, which is defined differently for Square and Circle.  

- The script assumes a shared interface for objects derived from Shape, specifically that they will have an area method. This allows the shape_density method to be used polymorphically on any Shape subclass.  

- Instances are dictionaries that can hold properties and a reference to their class, which allows for dynamic property access and method invocation.  

- The script uses dictionary merging as a means to combine the properties of a parent class with those of a subclass when instantiating an object. 

<div id="trace"/>

# 6. Task 3: Tracing
The _lgl_interpreter.py_ script is enhanced with the `--trace trace_file.log` argument to support function tracing using a decorator. This argument triggers logging of the start and end times of each function into the file _trace_file.log_.

---

<div id="log"/>

## 6.1. Logging

<div id="funtrace"/>

### 6.1.1 Implementing the Decorator  
The `@trace` decorator is designed to wrap the `do` function, the central executor of our interpreter. Specifically, the `trace` function takes another function as an argument and returns a new function that wraps the original with additional logging behavior. The relevant code is shown below:
```python
def trace(func):
    def _inner(*args, **kwargs):
        # Generate a unique ID for the function call
        my_id = next(num for num in iter(lambda: random.randint(100000, 999999), None) if num not in global_id)
        global_id.append(my_id)
        
        # Get the name of the function being called
        ele = list_iterator(args[1])
        
        # Log the start of the function call
        if ele:
            file_logging(f"{my_id},{ele},start,{datetime.now()}")
        
        # Execute the function
        res = func(*args, **kwargs)
        
        # Log the end of the function call
        if ele:
            file_logging(f"{my_id},{ele},stop,{datetime.now()}")
        
        return res
    return _inner

# Apply the trace decorator to the do function
@trace
def do(env, expr):  
    # rest of the code...
```  
The process includes:
1. Logging the start of the `do` function execution, including ID, function name, event, and timestamp.
2. Executing the `do` function with its arguments and storing the result.
3. Logging the end of the function execution.
4. Returning the result of the function call.

Within the decorator, a unique ID is generated for each function call, crucial for distinguishing separate invocations of the same function, especially in recursive calls.

<div id="tracer"/>

### 6.1.2 Calling the Tracer
Usage: `python lgl_interpreter.py example_trace.gsc --trace trace_file.log`, or `python lgl_interpreter.py example_class.gsc --trace trace_file.log` (or with any other .gsc file).  
```python
if len(sys.argv) == 4:
    assert sys.argv[2] == "--trace", f"Invalid argument, expected --trace got {sys.argv[2]}"
    # Open the log file and write headers for CSV format
    with open(sys.argv[3], "a") as f:
        f.write("id,function_name,event,timestamp\n")
```
In the `main` function, the script checks for the `--trace` argument and initializes the log file if present. Each function call decorated with `@trace` logs into this file. The result is printed to the console after processing the .gsc file.

<div id="report"/>

## 6.2 Reporting

<div id="createreport"/>

#### 6.2.1 Building the Reporter
The _reporting.py_ script reads a log file generated by tracing and displays the data in a tabulated format using the Python library _tabulate_.

The process involves:
1. Opening and reading the trace log file.
2. Initializing dictionaries to track runtime and call counts for each function.
3. Iterating through log entries, grouping events based on function calls, and calculating total function runtimes.
4. Presenting the collected data in a table with columns: "Function Name", "Num. of Calls", "Total Time (ms)", and "Average Time (ms)", which is then printed to the console.


<div id="reportoruse"/>

#### 6.2.2 Calling the Reporter
Usage: `python reporting.py trace_file.log`  
* Report for a trace_file.log containing logs from example_trace.gsc:  
```
| Function Name   | Num. of Calls | Total Time (ms) | Average Time (ms) |
|-----------------|---------------|-----------------|-------------------|
| get_area        |             1 |           0.324 |              0.32 |
| get_cubes       |             1 |           0.271 |              0.27 |
```
* Report for a trace_file.log containing logs from example_class.gsc:  
```
| Function Name     | Num. of Calls | Total Time (ms) | Average Time (ms) |
|-------------------|---------------|-----------------|-------------------|
| fun.shape_density |             2 |           0.097 |              0.05 |
| area_get          |             2 |           0.261 |              0.13 |
```

---
