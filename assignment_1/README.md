#### This testing program checks if the functions in file_manager.py are correctly implemented. Basic and edge cases are being tested to ensure the correctness of file_manager.py.
# ASSIGNMENT 1 - FILE MANAGER TESTING
Software Construction HS23, University of Zurich, Supervision Prof. Dr. Bacchelli

Authors:
* Ece Zeynep Asirim
* Mara Miruna Bucur
* Smail Alijagic
***

# Table of Contents
### **[1. Usage](#usage)**
* [1.1 General Usage](#generalusage)
* [1.2 Valid Call Examples](#validcalls)
* [1.3 Invalid Call Examples](#invalidcalls)

### **[2. Imports](#imports)**
* [2.1 os](#os)
* [2.2 time](#time)
* [2.3 sys](#system)
* [2.4 stat](#stat)
* [2.5 file_manager](#filemanager)

### **[3. Helper Functions](#helperfunctions)**
* [3.1 introspection()](#introspection)
* [3.2 setup()](#setup)
* [3.3 teardown()](#teardown)
* [3.4 track_time()](#tracktime)
* [3.5 main function](#mainfunction)

### **[4. Test Functions](#testfunctions)**
* [4.1 General Structure of Test Functions](#generalstructureoftestfunctions)
* [4.2 Reading Files](#readingfiles)
  * [4.2.1 test_read_from_non_empty_file()](#test421)
  * [4.2.2 test_read_from_empty_file()](#test422)
  * [4.2.3 test_read_from_non_existing_file()](#test423)
  * [4.2.4 test_read_from_special_character_file()](#test424)
* [4.3 Creating Files](#creatingfile)
  * [4.3.1 test_create_empty_file()](#test431)
  * [4.3.2 test_create_non_empty_file()](#test432)
  * [4.3.3 test_create_file_with_non_alpha_characters()](#test433)
  * [4.3.4 test_create_file_without_file_type()](#test434)
  * [4.3.5 test_create_file_with_invalid_name_type()](#test435)
  * [4.3.6 test_create_file_with_bool_type_file_name()](#test436)
  * [4.3.7 test_create_file_with_bool_type_content()](#test437)
  * [4.3.8 test_create_file_with_max_file_name_length()](#test438)
  * [4.3.9 test_create_file_with_name_over_maximum_length()](#test439)
  * [4.3.10 test_create_file_in_nonexistent_directory()](#test4310)
* [4.4 Writing to Files](#writingtofiles)
  * [4.4.1 test_write_in_empty_file()](#test441)
  * [4.4.2 test_write_to_special_character_file()](#test442)
  * [4.4.3 test_write_in_readonly_file()](#test443)
  * [4.4.4 test_write_boolean_type_values()](#test444)
  * [4.4.5 test_write_into_non_empty_file()](#test445)
* [4.5 Deleting Files](#deletingfiles)
  * [4.5.1 test_delete_existing_file()](#test451)
  * [4.5.2 test_delete_non_existing_file()](#test452)
  * [4.5.3 test_delete_file_with_wrong_directory()](#test453)
  * [4.5.4 test_delete_directory_instead_of_file()](#test454)
  * [4.5.5 test_delete_readonly_file()](#test455)


<div id="usage"/>

# 1. Usage
---
<div id="generalusage"/>

### 1.1 General Usage
* This call runs all tests:
```
python run_tests.py
```
* This call runs only tests that contain the substring pattern in their name:
```
python run_tests.py --select pattern
```
* It is also possible to enter more than one pattern:
```
pyton run_tests.py --select pattern_required pattern_optional
```
* In case of error replace python with python3 (this is a common error on macOS):
```
python3 run_tests.py 
# or
python3 run_tests.py --select pattern
# or
python3 run_tests.py --select pattern_required pattern_optional
```


<div id="validcalls"/>

### 1.2 Valid Call Examples
* The following examples show some valid calls:
```
python run_tests.py
python run_tests.py --select read
python run_tests.py --select create write delete
python run_tests.py --select del wr
```

<div id="invalidcalls"/>

### 1.3 Invalid Call Examples
* The following examples show some invalid calls:
```
python run_tests.py --select # missing pattern
python run_tests.py --slect  # missing pattern and typo in slect
python run_tests.py --  # missing select and pattern or remove --
```

<div id="importedlibraries"/>

# 2. Imported Libraries
---
<div id="os"/>

### 2.1 os
* **os** is used to handle directory related cases, such as **os.path.exists()**.
<div id="time"/>

### 2.2 time
* **time** is used to check the running times for our testing functions.

<div id="system"/>

### 2.3 sys
* **sys** is imported to handle command line arguments.

<div id="stat"/>

### 2.4 stat
* **stat** is imported to handle readonly modes.

<div id="filemanager"/>

### 2.5 file_manager
* **file_manager** is imported to test the functions in file_manager.

<div id="helperfunctions"/>

# 3. Helper Functions
---


<div id="introspection"/>

### 3.1 introspection()
* **introspection(test_name=""")** creates the necessary environment for the test. 
Automatically discovers and runs tests based on the provided naming patterns.

Usage
**introspection(test_name="")** searches in globals() for all functions that start with **"test_"** and contain the substring pattern in their name. If true **introspection(test_name="")** runs this test and iterates further through **globals()** until all test were executed.
result = introspection("example_test_pattern")
print(result)

Parameter:
It takes one optional argument (**test_name**), which is one pattern or a list of patterns.

Return:
After each test a short string (with pass/fail/error and run time in seconds) is printed in the prompt. At the end the function returns a dictionary with the statistics about how many tests passed, failed or caused an error.

Key Features:
All the matching tests are executed and after the execution of every test, it prints an string indicating the outcome of that test (pass, fail or error) as well as the execution time. Once all tests were executed, it displays in the console a statistic summary, indicating the number of passed test, failed tests and test in which it encountered errors.

<div id="setup"/>

### 3.2 setup()
* **setup(file_name, file_content="")** Prepares the testing environment by creating necessary resources, such as files.
It takes one required (**file_name**) and one optional (**file_content**, per default: **""**) argument. It creates a **.txt** file with the content **file_content** and the name **file_name**. The function returns **file_name**.


<div id="teardown"/>

### 3.3 teardown()
* **teardown(file_name)** Cleans up the testing environment by restoring it to its pre-test state by removing test files.
Takes one required argument (**file_name**). The function deletes that file from the directory. It does not have any return value (per default: **None**).


<div id="tracktime"/>

### 3.4 track_time()
* **track_time()** does not take any argument and returns how much time (in nano-seconded) has passed. It is used to track how much time each test took.

Purpose: Tracks the system processing time in nanoseconds.
Returns: The current performance counter value.

<div id="mainfunction"/>

### 3.5 main function
* run_tests.py does not have a classical main() function, rather the script waits for user input via command line arguments and validates if the input was correctly entered. In case of a wrong call an assert is raised informing the user that the call was false. This procedure ensures to only run the testing functions, when they are correctly called.


<div id="testfunctions"/>

# 4. Test Functions
---
<div id="generalstructureoftestfunctions"/>

### 4.1 General Structure of Test Functions
* Generally every test consists of a similar structure with 3 phases:
- Setup Phase:
Involves preparing the environment for the test by creating a file with the specified content for testing.
- Testing Phase:
This is where the actual test takes place. The function or method under test is called, and its behavior is observed.
Try-excep blocks are used to handle exceptions that might arise during the test. This ensures that even if one test fails due to an exception, the subsequent tests can continue. There are specific except blocks for different types of exceptions, allowing for fine-grained control over how each type of exception is handled. Assert statements are used to check if the behavior is as expected. If the condition in the assert statement is False, an AssertionError is raised, indicating that the test has failed.
- Teardown Phase:
Regardless of the test outcome, teardown function is executed in the finally block to ensures that the environment is cleaned up after the testing phase (delete files, revert write permission etc.)


Below example represents the general structure of a test function.
```
test_example():
    # setting up the environment
    file = setup("example.txt")
    
    # testing phase
    try:
        assert file_manager.some_func(file) == True
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RunTimeError
    finally:
        # finally always restores environment to pre-state
        teardown(file)
```

Below example represents the importance of "finally: teardown":
Lets assume teardown was executed inside the try block instead of the finally block. In the scenario that the file_manager function being tested were to be modified in a way that assert would fail (returns True), the environment could not be restored. To ensure that the environment is  always restored, teardown is executed inside finally block.
```
test_create_file_with_content():
    file_name = "example.txt"
    file_content = "hello world")
    try:
        assert file_manager.create_file(file_name, file_content) == False 
         #if assert returns True, teardown would never be reached
        teardown(file_name)
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RunTimeError
    finally:
        teardown(file_name)  
        # without finally, example.txt would not be removed from the environment
```



<div id="readingfiles"/>

### 4.2 Reading Files
This part of testing focuses on ensuring the function read_file in file_manager.py works seamlessly. We are covering a wide range of tests from reading regular files or empty files to more complex scenarios like special character filenames or non-existent files. Therefore, we ensure that regardless of the file's state, the system's response is always error-free. All these test provide a consistent outcome, passing regardless of the operating system.

<div id="test421"/>

* **4.2.1 test_read_from_non_empty_file()**    
   _Description:_ Tests the ability of file_manager.read_file function to correctly read the content from a non-empty file.
   - A file named "non_empty_file.txt" is created with the content "hello world" using the setup function.
   - An assert statement checks if the content read from the file matches the expected content ("hello world").
      - If the assert statement fails (the content read from the file doesn't match the expected content), an AssertionError is raised. This is caught, the file is deleted, and assert False is executed to indicate the test's failure.
      - If any other exception occurs during the test a RuntimeError is raised to indicate an unexpected error during the test.
   - The teardown function is called to delete the file and clean up the environment, regardless of whether the test passes or fails. 
   _Input:_ A file named "non_empty_file.txt" with a known content ("hello world").  
   _Expected Outcome:_ The function should be able to read the content from a non-empty file and return the content that was written to the file.


<div id="test422"/>

* **4.2.2 test_read_from_empty_file()**  
   _Description:_ Tests the ability of file_manager.read_file function to read from an empty file.
   - A new empty file named "empty_file.txt" is created using the setup function. 
   - An assert statement checks if the returned content from the file is an empty string. 
      - If the function returns anything other than an empty string, the test will fail.
      - If any other unexpected behavior or error occurs during the test, a RuntimeError will be raised.
   - Regardless of the test outcome, teardown function is executed in the finally block to ensures that the file created during setup phase is deleted, restoring the environment to its original state.  
   _Input:_ An empty file.  
   _Expected Outcome:_ The function should handle empty files correctly and return an empty string as sexpected.


<div id="test423"/>

* **4.2.3 test_read_from_non_existing_file()**  
   _Description:_ Tests the ability of file_manager.read_file function to handle an attempt to read a file that does not exist. 
   - Setup phase is intentionally omitted due to the nature of the test.
   - The assertion checks if the function returns None, indicating it correctly identified the file's absence.
      - If the function returns anything other than None, the assertion will fail and AssertionError is raised, indicating the function did not behave as expected.
      - If any other unexpected behavior or error occurs during the test, a RuntimeError will be raised.
   - This test doesn't require a teardown phase, since no resources were set up initially, hence there's nothing to clean up or revert.  
   _Input:_ A non-existent file named "non_existing_file.txt".  
   _Expected Outcome:_ The function should recognize the file's absence and return None, indicating the file doesn't exist. 


<div id="test424"/>

* **4.2.4 test_read_from_special_character_file()**  
   _Description:_ Tests the ability of file_manager.read_file function to handle file names containing special characters. In some systems, files with non-alphanumeric characters can create issues, so it's crucial to manage them.
   - A file with a name containing special characters ("sp€ci@l_ch@r.txt") is created with a specific content ("content of file") to verify later if the reading function fetches the correct content.
   -  An assertion checks if the content returned from the function matches the known content of the file.
      - If the content does not match, or if the function behaves unexpectedly, an AssertionError is triggered with a message.
      - If any other unexpected behavior or error occurs during the test, a RuntimeError will be raised.
   - The finally block ensures that, irrespective of the test outcome, the file created during the setup phase is deleted, restoring the test environment to its original state.  
   _Input:_ A file named "sp€ci@l_ch@r.txt" containing the text "content of file".  
   _Expected Outcome:_ The function should successfully read the content from the file with a special character name and return the exact content.


<div id="creatingfiles"/>

### 4.3 Creating Files
Ensures that files can be created successfully, with checks for edge cases such as creating files with non-string names, files without file types, etc.
For these tests, the setup phase involves only instantiating the file rather than creating the physical file using the setup function. The reason for this is that the test's main objective is to evaluate the file_manager.create_file function's capability to create a file with specific content. By deferring the actual file creation to the testing phase, we ensure that the file_manager.create_file function is fully evaluated, including its ability to instantiate a new file and populate it with content.


<div id="test431"/>

* **4.3.1 test_create_empty_file()**  
   _Description:_ Tests the ability of file_manager.create_file function to create a file with no content. Given that file creation is a fundamental operation, it's crucial to ensure the function is capable of performing this even if the file is empty.
   - A new empty file named "empty_file.txt" is defined.
   - An assertion verifies the existence of the file in the system using the os.path.exists method.
      	- If the assertion finds that the file hasn't been created or if the function behaves differently than anticipated, an AssertionError is triggered.
     	 - If any other unexpected behavior or error occurs during the test, a RuntimeError will be raised.
   - The finally block ensures that the created file is deleted, restoring the testing environment back to its original state regardless of the test outcome.  
   _Input:_ A file named "empty_file.txt" with no content.  
   _Expected Outcome:_ The function should accurately create an empty file and the file's presence should be verifiable post-creation.


<div id="test432"/>

* **4.3.2 test_create_non_empty_file()**  
   _Description:_ Tests the ability of file_manager.create_file function to create a file with the specified content. This test function extends "test_create_empty_file" as the ability to create and simultaneously input content into a file requires additional precision.
   - A new file named "non_empty_file.txt" is defined.
   - An assertion verifies the presence of the file in the system using the os.path.exists method.
      - If the file isn't detectable after its creation or if the system behaves unexpectedly, an AssertionError is raised.
      - If any other unexpected behavior or error occurs during the test, a RuntimeError will be raised.
   - The finally block ensures that the created file is deleted, restoring the testing environment back to its original state regardless of the test outcome.  
   _Input:_ A file named "non_empty_file.txt" containing the text "hello world".  
   _Expected Outcome:_ The function should effectively generate a non-empty file with the specified name and content. 


<div id="test433"/>

* **4.3.3 test_create_file_with_non_alpha_characters()**  
   _Description:_ Tests the ability of file_manager.create_file function to create a file with non-alphabetic characters in its name. Certain systems and file management operations might struggle with names that deviate from the standard alphanumeric format. Therefore, ensuring that our system can handle such cases is essential.
   - A new file named "+|.,-_.txt" is defined. 
   - An assertion is utilized to validate the existence of the new file using the os.path.exists method.
      - If the file isn't detectable after its creation or if the system behaves unexpectedly, an AssertionError is raised.
      - If any other unexpected behavior or error occurs during the test, a RuntimeError will be raised.
   - The finally block ensures that the created file is deleted, restoring the testing environment back to its original state regardless of the test outcome.  
   _Input:_ A file named with non-alphabetic characters “+|.,-_.txt”  
   _Expected Outcome:_ The function should create a file with the specified non-alphanumeric name. Once the file is created, its presence should be verifiable.


<div id="test434"/>

* **4.3.4 test_create_file_without_file_type()**  
   _Description:_ Tests the ability of file_manager.create_file function to create a file without specifying a file extension (e.g., .txt, .pdf). Many systems allow the creation of files without extensions, and it's important to ensure that the function handles this properly.
   - A new file, named "file_type_missing", without an extension is defined. 
   - An assertion verifies the file's existence in the system using the os.path.exists method.
      - If after creation, the file is undetectable or if the system behaves unexpectedly, an AssertionError is raised.
      - Other unexpected issues or exceptions are caught by the second except block, prompting a RuntimeError.
   - The finally block guarantees that regardless of the test outcome, any created file is eliminated, resetting the testing environment to its pristine state.  
   _Input:_ A file named "file_type_missing" without a specified file extension and no content.  
   _Expected Outcome:_ should proficiently create a file without an explicit file type and the created file's presence should be confirmable in the system.


<div id="test435"/>

* **4.3.5 test_create_file_with_invalid_name_type()**  
   _Description:_ Tests the response of file_manager.create_file function when provided with a file name of an invalid type,such as an integer. A well designed file management system should recognize and handle inputs of invalid types, hence this test is important.
   - There is no setup phase for this test because the main goal is to evaluate the file creation function's response to an invalid file name type.
   - The function is invoked to create a file name with integer (123).
   - An assertion checks if the function returns False, indicating that it properly identified and handled the invalid input type.
      - If the function doesn't return False, or if it accepts the invalid name type, an AssertionError is raised.
      - Any other unexpected issues or exceptions are caught by the second except block, resulting in a RuntimeError.
   - No finally block or teardown phase is needed.  
   _Input:_ Invalid data type for the file name.  
   _Expected Outcome:_ The function should handle the error and return False.


<div id="test436"/>

* **4.3.6 test_create_file_with_bool_type_file_name()**

  _Description:_ Tests the `file_manager.create_file` function's response to a boolean type file name (e.g., `True`, `False`, or `None`). The goal is to verify that the function correctly identifies this invalid input type and returns `False` as expected. It first calls the `file_manager.create_file` function with a boolean file name (e.g., `None`). Then, it use an assertion to check if the function returns `False`, indicating successful recognition and handling of the boolean file name type as invalid.
   - If the function does not return `False`, an AssertionError is raised.
   - Any unexpected issues or exceptions are caught by the second `except` block, leading to a RuntimeError.

  _Input:_ Boolean data type (e.g., `None`) used as the file name.

  _Expected Outcome:_ The function should correctly identify the error and return `False`, demonstrating its proper handling of boolean type file names.

   
   
   <div id="test437"/>
* **4.3.7 test_create_file_with_bool_type_content()**

  _Description:_ Evaluates the behavior of the `file_manager.create_file` function when boolean type content is provided for file creation. This    test verifies the function's ability to correctly identify and handle boolean values (e.g., `True`, `False`, or `None`) as file content. I follows the next steps:
  - Define a file name (e.g., "correct_name.txt").
  - Call the `file_manager.create_file` function with the specified file name and boolean type content (e.g., `None`).
  - Verify that the function returns `False` as expected, indicating successful recognition and handling of boolean type content as an error.
  - If the function does not return `False`, proceed to teardown the file (if it was created) and raise an AssertionError.
  - Catch any other unexpected issues or exceptions using the second `except` block, resulting in a RuntimeError.
 - If the test case completes successfully, ensure the file (if created) is torn down to maintain a clean test environment.

  _Input:_ Boolean type content (e.g., `None`) provided for file creation.

  _Expected Outcome:_ The function should correctly identify the error and return `False`, demonstrating its proper handling of boolean type content during file creation.


<div id="test438"/>

* **4.3.8 test_create_file_with_max_file_name_length()**

  _Description:_ Evaluates the `file_manager.create_file` function's ability to create a file with the maximum allowed file name length. This test assesses whether the function can handle and process file names that are as long as the maximum length supported by most systems.This test involves the following steps:

  - The test attempts to create a file with the longest possible file name (255 characters) by defining a file name consisting of "a" repeated 255 times.
  - An assertion checks if the function returns `True`, indicating the successful creation of the file with the maximum allowed file name length.
  - If the function does not return `True`, an AssertionError is raised.
  - Any other unexpected issues or exceptions are caught by the second `except` block, resulting in a RuntimeError.
  - Finally, a teardown operation is performed to clean up the created file (if it was created).

  _Input:_ None (the function attempts to create a file with the longest possible file name).

  _Expected Outcome:_ The function should successfully create the file with the maximum allowed file name length (255 characters) and return `True`, demonstrating its capability to handle maximum file name lengths.


<div id="test439"/>

* **4.3.9 test_create_file_with_name_over_maximum_length()**

  _Description:_ Evaluates the `file_manager.create_file` function's response when attempting to create a file with a file name that exceeds the maximum allowed length. This test assesses whether the function correctly handles scenarios where the file name length exceeds the system-defined maximum limit. It calls the `file_manager.create_file` function with a file name longer than the maximum allowed length (e.g., 258 characters) and verifies that the function returns `False` as expected, indicating the proper handling of excessive file name lengths. 
  - The test attempts to create a file with a file name that exceeds the maximum allowed length by defining a file name consisting of "a" repeated 258 times.
  - An assertion checks if the function returns `False`, as expected, signifying its correct handling of file names that exceed the maximum length.
    - If the function does not return `False`, an AssertionError is raised.
    - Any other unexpected issues or exceptions are caught by the second `except` block, leading to a RuntimeError.

  _Input:_ None (the function attempts to create a file with a name longer than the maximum allowed length).

  _Expected Outcome:_ The function should correctly identify the error, handle the attempt to create a file with a name exceeding the maximum allowed length, and return `False`.



<div id="test4310"/>

* **4.3.10 test_create_file_in_nonexistent_directory()**

  _Description:_ Evaluates the response of the `file_manager.create_file` function when attempting to create a file in a directory that does not exist. This test assesses how the function handles scenarios where the specified directory for file creation is nonexistent. It calls the `file_manager.create_file` function with a file path pointing to a non-existing directory (e.g., "nonexistent_directory/test_file.txt") and verifies that the function returns `False` as expected, indicating the proper handling of non-existent directories.
  - The test attempts to create a file with a file path pointing to a directory that does not exist (e.g., "nonexistent_directory/test_file.txt").
  - An assertion checks if the function returns `False`, as expected, signifying its correct response to the attempt to create a file in a nonexistent directory.
   - If the function does not return `False`, an AssertionError is raised.
   - Any other unexpected issues or exceptions are caught by the second `except` block, leading to a RuntimeError.

  _Input:_ A file path ("nonexistent_directory/test_file.txt") pointing to a non-existing directory.
  _Expected Outcome:_ The `file_manager.create_file` function should correctly identify the error, handle the attempt to create a file in a nonexistent directory, and return `False`.


<div id="writingtofiles"/>

### 4.4 Writing to Files
In this part, we validate the writing_file method implemented in file_manager.py. The set of tests in here confirm that data is written correctly, even in challenging situations like writing to files with special characters or readonly permissions. 


<div id="test441"/>

* **4.4.1 test_write_in_empty_file()**

  _Description:_ Tests the `file_manager.write_file` function's ability to write content to an empty file. The test sets up an empty file, writes the content "hello world" to it, and then checks if the content was correctly written into the file by opening and reading its content. If the written content matches the expected "hello world," the test passes. Otherwise, an AssertionError is raised. Teardown is performed to clean up the file.	

  _Input:_ An empty file with the content "hello world" to be written.

  _Expected Outcome:_ An empty file with the content "hello world" to be written.
  **Note:** It is worth mentioning that our test suite incorporates a check for writing to non-existent files. In our context, this particular test would succeed on a Windows system but fail on MacOS. This discrepancy arises from the inherent differences in how the two operating systems manage this scenario: Windows does not permit writing to a non-existent file, whereas MacOS will seamlessly create the file and allow the write operation.


<div id="test442"/>

* **4.4.2 test_write_to_special_character_file()**


  _Description:_ TChecks whether the `file_manager.write_file` function can handle special characters in file names and return the correct content. The test sets up a file with a special character in its name (e.g., "sp€ci@l_ch@r.txt") and writes the content "content of file" to it. The test asserts that the function returns True, indicating successful writing to a file with special characters in its name. Teardown is performed to clean up the file.

  _Input:_ A file with a special character in its name and the content "content of file" to be written.

  _Expected Outcome:_ The `file_manager.write_file` function should successfully write the content to the file and return `True`.

<div id="test443"/>

* **4.4.3 test_write_in_readonly_file()**

   _Description:_ Tests the `file_manager.write_file`function when writing to a read-only file. The test sets up a file and removes write permissions from it (turns on read-only mode). It then attempts to write "hello world" to the read-only file and asserts that the function returns `False`. Teardown is performed to restore write permissions and clean up the file.

   _Input:_ A read-only file with the content "hello world" to be written.
   
   _Expected Outcome:_ The `file_manager.write_file` function should recognize the read-only status of the file and return `False`.


<div id="test444"/>

* **4.4.4 test_write_boolean_type_values()**


   _Description:_ Tests the `file_manager.write_file` function's response when attempting to write boolean values (e.g., True) to a file. The test sets up a file and attempts to write `True` to it. It asserts that the function returns `False` as expected. Teardown is performed to clean up the file.

   _Input:_ A file with the content `True` to be written.
   
   _Expected Outcome:_ The `file_manager.write_file` function should correctly handle boolean values and return `False`.


<div id="test445"/>

* **4.4.5 test_write_into_non_empty_file()**

   _Description:_ This test checks the `file_manager.write_file` function's response when attempting to write to an existing non-empty file. The file is first created using `setup()`. To test if the new file content was correctly written, the file is opened and then it is being checked if the file content is equal to the one that was written. Teardown is performed to clean up the file.

   _Input:_ A non-empty existing file name ("non_empty.txt") with the content "hello world". The new file content is "Software Construction is cool!".
   
   _Expected Outcome:_ The `file_manager.write_file` function should correctly handle the attempt to overwrite the content of an existing non-empty file and return `True`.

<div id="deletingfiles"/>

### 4.5 Deleting Files
This set of test ensures the safe and correct deletion of files using the delete_file function in file_manager.py. The tests in this section ensure that files can be deleted successfully and without unintended side effects. They are generally valid and check that the file can be deleted irrespective of the state, name, or permissions of the file. One exception worth mentioning is that only in Windows the test for deleting read-only files will pass because in other operation systems, the levels of permissions are superior and harder to break. \


<div id="test451"/>

* **4.5.1 test_delete_existing_file()**

   _Description:_ Tests the `file_manager.delete_file` function's ability to delete an existing file. The test sets up an existing file, deletes it using the `file_manager.delete_file` function, and checks if the file no longer exists by verifying its path. If the file is successfully deleted, the test passes. Otherwise, an `AssertionError` is raised.
   
   _Input:_ An existing file to be deleted.
   
   _Expected Outcome:_ The `file_manager.delete_file` function should successfully delete the existing file, and the test should pass if the file no longer exists.

<div id="test452"/>

* **4.5.2 test_delete_non_existing_file()**

   _Description:_ Tests the `file_manager.delete_file` function's behavior when attempting to delete a non-existing file. The test does not require setup, as the goal is to check the function's response to a non-existing file. It attempts to delete a non-existing file ("never_existed_file.txt") and asserts that the function returns `False`. Teardown is not needed as no file was created.

   _Input:_ A non-existing file ("never_existed_file.txt") to be deleted.
   
   _Expected Outcome:_ The `file_manager.delete_file` function should correctly handle the attempt to delete a non-existing file and return `False`.

<div id="test453"/>

* **4.5.3 test_delete_file_with_wrong_directory**

   _Description:_ Tests the `file_manager.delete_file` function's response when attempting to delete a file in a directory that does not exist. The test aims to check how the function handles scenarios where the specified file path points to a non-existing directory (e.g., "nonexistent_directory/test_file.txt"). It attempts to delete the file at the specified path and asserts that the function returns`False`, as expected. If the function does not return `False`, an AssertionError is raised, and any other unexpected issues or exceptions are caught by the second except block, leading to a `RuntimeError`.

   _Input:_ A file path ("nonexistent_directory/test_file.txt") pointing to a non-existing directory.
   
   _Expected Outcome:_ The `file_manager.delete_file` function should correctly handle the attempt to delete a file in a non-existing directory and return `False`.

<div id="test454"/>

* **4.5.4 test_delete_directory_instead_of_file()**

   _Description:_ Tests the `file_manager.delete_file` function when attempting to delete a directory instead of a file, where the file name is not indicated. The test sets up a directory ("test_directory"), attempts to delete it using the `file_manager.delete_file` function, and asserts that the function returns `False`, as it should not be possible to delete a directory using this function. Teardown is performed to remove the initially created directory.

   _Input:_  A directory to be deleted using the `file_manager.delete_file` function.
   
   _Expected Outcome:_ The `file_manager.delete_file` function should recognize that a directory is being passed as input and return `False`, demonstrating that it should not delete directories using this function.

<div id="test455"/>

* **4.5.5 test_delete_readonly_file()**

   _Description:_ Tests the `file_manager.delete_file` function when attempting to delete a read-only file. The test sets up a read-only file, attempts to delete it using the `file_manager.delete_file`delete_file function, and asserts that the function returns `False`. Teardown is performed to restore write permissions and clean up the file.

   _Input:_ A read-only file to be deleted.
   
   _Expected Outcome:_ The `file_manager.delete_file` function should recognize the read-only status of the file and return `False`.

   **Note:** This test should fail for macOS but pass for Windows because the difference in the level of permissions (Windows' permissions are weaker)
