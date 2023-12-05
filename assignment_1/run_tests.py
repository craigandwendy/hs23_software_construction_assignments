import file_manager
import os
import time
import sys
import stat


def introspection(test_name=""):
    # check if the test_name type is correct (important when only receiving one or multiple patterns)
    assert isinstance(test_name, str) or isinstance(test_name, list), f"Received invalid type"
    # track all called tests in one dictionary
    results = {"pass": 0, "fail": 0, "error": 0}

    # find and execute tests automatically
    if isinstance(test_name, str):
        # if only one pattern was given make a list out of it, to reduce duplicate code when search in globals() for test
        test_name = [test_name]

    if isinstance(test_name, list):
        called_test = []
        for t_name in test_name:  # iterating through all patters
            for (name, test) in globals().items():  # iterating through all globals()
                # check name requirements and make sure that the test was not called previously
                if name.startswith("test_") and t_name in name and name not in called_test:
                    called_test.append(name)
                    t0 = track_time()  # starting time tracker
                    try:
                        test()
                        t1 = track_time()  # ending time tracker
                        results["pass"] += 1
                        print(f"test: {name}  Passed,  finished in {t1 - t0} s.")
                    except AssertionError:
                        t1 = track_time()  # ending time tracker
                        results["fail"] += 1
                        print(f"test: {name}  Failed,  finished in {t1 - t0} s.")
                    except Exception:
                        t1 = track_time()  # ending time tracker
                        results["error"] += 1
                        print(f"test: {name}  Error occurred,  finished in {t1 - t0} s.")
        return results


def track_time():
    # tracking system processing time in nanoseconds
    return time.perf_counter()


def setup(file_name, content=""):
    # setting up the necessary resources for the testing environment, e.g. creating files etc.
    try:
        # Open the file with write ('w') permission.
        # If the file doesn't exist, it will be created.
        with open(file_name, "w") as file:
            # Write the specified content to the file.
            file.write(content)
        # Return the file name indicating that setup was successful.
        return file_name
    except Exception as e:
        # Log any exception that occurs during file operation.
        print(f"Error during setup: {e}")
        # Return None to indicate that setup failed.
        return None


def teardown(file_name):
    # restoring the setup-environment to pre-state
    try:
        # Remove the specified file.
        os.remove(file_name)
        # Return True when teardown was successful
        return True
    except FileNotFoundError:
        # Error message if the file is not found
        print(f"File {file_name} not found during teardown.")
        # Return False when teardown failed
        return False
    except PermissionError:
        # Log an error message if there is a permission error
        print(f"Permission error during deleting {file_name}.")
        # Return False to indicate that teardown failed.
        return False
    except Exception as e:
        # Log any other exception that occurs during file operation
        print(f"Error during teardown: {e}")
        # Return False to indicate that teardown failed
        return False


def test_read_from_non_empty_file():
    # Test if the read_file function can read from a file with content correctly
    # setup
    file_content = "hello world"
    file = setup("non_empty_file.txt", file_content)

    # testing
    try:
        # assert that the content read from the file matches the expected content
        assert file_manager.read_file(file) == file_content
    # handle AssertionError or any other unexpected exceptions that arise
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_read_from_empty_file():
    # Test if the read_file function can read from an empty file correctly

    # setup
    file = setup("empty_file.txt", "")
    # testing
    try:
        # assert that the content read from the empty file is indeed an empty string
        assert file_manager.read_file(file) == "", "Failed: Reading from an empty file should return an empty string"
    # handle AssertionError or any other unexpected exceptions that arise
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_read_from_non_existing_file():
    # Test if the read_file function can handle non-existing files appropriately

    # setup not needed because file does not exist
    # testing
    try:
        # expect the function to return None, indicating the file does not exist
        assert file_manager.read_file("non_existing_file.txt") is None
    # handle AssertionError or any other unexpected exceptions that arise
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    # teardown not needed since no resource was created


def test_read_from_special_character_file():
    # Test if the read_file function can read files with names containing special characters

    # setup
    file_name = "sp€ci@l_ch@r.txt"
    file_content = "content of file"
    file = setup(file_name, file_content)
    # testing
    try:
        # assert that the content read matches the known content
        assert file_manager.read_file(file) == file_content, "Failed reading from a file with special characters in file name"
    # raise AssertionError if the function doesn't return the expected content
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_create_empty_file():
    # Test if create_file function can accurately create an empty file

    # setup
    file = "empty_file.txt"
    # testing
    try:
        # invoke create_file function to create file
        file_manager.create_file(file)
        # verify the existence of the created file
        assert os.path.exists(file)
    # raise AssertionError if the created file's path isn't found
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_create_non_empty_file():
    # Test create_file function's ability to create a non-empty file

    # setup
    file = "non_empty_file.txt"
    # testing
    try:
        # invoke create_file function to create file
        file_manager.create_file(file, "hello world")
        # verify the existence of the created file
        assert os.path.exists(file)
    # raise AssertionError if the created file's path isn't found
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_create_file_with_non_alpha_characters():
    # Test create_file function's ability to create a file named with exclusively non-alphanumeric characters

    # setup
    file = "+ç.txt"
    # testing
    try:
        # invoke create_file function to create file
        file_manager.create_file(file)
        # verify the existence of the created file
        assert os.path.exists(file)
    # raise AssertionError if the created file's path isn't found
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_create_file_without_file_type():
    # Test create_file function's ability to generate a file without specifying an explicit file extension

    # setup
    file = "file_type_missing"
    # testing
    try:
        # invoke create_file function to create file
        file_manager.create_file(file, "")
        assert os.path.exists(file)
    # raise AssertionError if the created file's path isn't found
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_create_file_with_invalid_name_type():
    # Test create_file function's ability to recognize and handle a file name of an invalid type (e.g. integer)

    # setup not needed, we want to test if the function will raise the Exception
    # testing
    try:
        # invoke create_file function to create file with an integer as the file name
        assert file_manager.create_file(123) == False
        # raise AssertionError if the function does not return False for the invalid input type
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions or if the function tries to process the invalid input
    except Exception:
        raise RuntimeError
    # teardown not needed, because file was never created


def test_create_file_with_bool_type_file_name():
    # Test create_file function's ability to identify and respond to a file name of an invalid type: False/True/None

    # setup not needed
    # testing
    try:
        # attempt creating a file with file name None and check if it returns False
        assert file_manager.create_file(None) == False
    # raise AssertionError if the function does not return False
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    # teardown not needed


def test_create_file_with_bool_type_content():
    # Test create_file function's ability to identify and respond to a file with bool type content: False/True/None

    # setup
    file_name = "correct_name.txt"
    # testing
    try:
        # Create a file with a valid name but None content and check if the function returns False
        assert file_manager.create_file(file_name, None) == False
    # raise AssertionError if the function does not return False
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file_name)


def test_create_file_with_max_file_name_length():
    # Test create_file function's ability to handle file names of maximum length

    # setup
    file = "a" * 255  # Maximum allowed file name length on most systems
    # testing
    try:
        # invoke create_file function with the maximum-length file name and check if it returns True.
        assert file_manager.create_file(file) == True, "Failed to create file with maximum file name length"
    # raise AssertionError if the function does not return True
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_create_file_with_name_over_maximum_length():
    # Test create_file function's behavior when faced with an excessively long file name

    # setup
    file = "a" * 258  # Maximum allowed file name length on most systems
    # testing
    try:
        # attempt to create the file and verify the function returns False.
        assert file_manager.create_file(file) == False, "Passed: As expected, it failed to create file with maximum file name length"
    # raise AssertionError if the function does not return False
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    # teardown not needed


def test_create_file_in_nonexistent_directory():
    # Test create_file function's response to a file creation attempt inside a non-existent directory

    # setup
    file_path = "nonexistent_directory/test_file.txt"
    # testing
    try:
        # attempt to create the file and verify the function returns False.
        assert file_manager.create_file(file_path) == False, "Failed: File should not be created in a nonexistent directory"
    # raise AssertionError if the function does not return False
    except AssertionError:
        raise AssertionError
    # raise RuntimeError for any other unexpected exceptions
    except Exception:
        raise RuntimeError
    # teardown not needed


def test_write_in_empty_file():
    # Test write_file function's ability to write in an empty file
    # setup
    file = setup("empty_file.txt", "")

    try:
        file_manager.write_file(file, "hello world")
        with open(file, "r") as f:
            # check if the previously written content, was correctly written into the file
            assert "hello world" == f.read()
    except AssertionError:
        assert False
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_write_to_special_character_file():
    # Test if write_file function is able to handle special characters and return the correct content

    # setup
    file = setup("sp€ci@l_ch@r.txt")
    content = "content of file"
    # testing
    try:
        # write the content into the file and verify it returns True.
        file_manager.write_file(file, content), "Failed writing to a file with special characters in file name"
        with open(file, "r") as f:
            # check if the previously written content, was correctly written into the file
            assert content == f.read()
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_write_in_readonly_file():
    # Test write_file function's response to a write request to a read-only file

    # setup
    file = setup("readonly.txt")
    # remove write permissions
    os.chmod(file, stat.S_IREAD)
    # testing
    try:
        # attempt to write to the read-only file and verify the function returns False
        assert file_manager.write_file(file, "hello world") == False, f"Invalid change to read-only file"
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        # reset write permissions so that it can be cleaned up
        os.chmod(file, stat.S_IWRITE)
        # teardown
        teardown(file)


def test_write_boolean_type_values():
    # Test write_file function's ability to manage when provided with boolean or None content

    # setup
    file = setup("correct_file.txt")
    # testing
    try:
        # write a boolean value into the file and check if the function returns False
        assert file_manager.write_file(file, True) == False
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        # teardown
        teardown(file)


def test_write_into_non_empty_file():
    # test if content of a non-empty file is correctly overwritten
    # setup
    file = setup("non_empty.txt", "hello world")
    new_file_content = "Software Construction is cool!"
    # testing
    try:
        file_manager.write_file(file, new_file_content)
        with open(file, "r") as f:
            # check if the previously written content, was correctly written into the file
            assert new_file_content == f.read()
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        teardown(file)


def test_delete_existing_file():
    # Test write_file function's ability to delete an existing file

    # setup
    file = setup("existing_file.txt")
    # testing
    try:
        # delete the previously created file
        file_manager.delete_file(file)
        # verify the file has been deleted by checking its path
        assert os.path.exists(file) == False
    except AssertionError:
        teardown(file)
        raise AssertionError
    except Exception:
        teardown(file)
        raise RuntimeError
    # "finally: teardown" not needed as the file was already deleted


def test_delete_non_existing_file():
    # Test write_file function's response when asked to delete a non-existing file

    # setup not needed, as we want to check a non-existing file
    # testing
    try:
        # attempt to delete a non-existing file and check if the function returns False
        assert file_manager.delete_file("never_existed_file.txt") == False
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    # teardown not needed, as no file was created


def test_delete_file_with_wrong_directory():
    # Test write_file function's behavior when asked to delete a file from a non-existent directory

    # setup
    file_path = "nonexistent_directory/test_file.txt"
    # testing
    try:
        # attempt to delete the file and verify that the function returns False
        assert file_manager.delete_file(file_path) == False, "Failed: File in nonexistent directory should not be deleted"
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError


def test_delete_directory_instead_of_file():
    # Test write_file function's behavior when asked to delete a directory instead of a file (file name not indicated)

    # setup
    dir_name = "test_directory"
    os.mkdir(dir_name)
    # testing
    try:
        # attempt to delete the directory using the file deletion function and verify it returns False
        assert file_manager.delete_file(dir_name) == False, "Failed: Directory should not be deleted using delete_file function"
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        # teardown: remove directory
        os.rmdir(dir_name)


def test_delete_readonly_file():
    # Test write_file function's behavior when asked to delete a read-only file
    # this function only works with windows or linux!

    # setup
    file = setup("readonly_delete.txt")
    os.chmod(file, stat.S_IREAD)  # turn on read-only mode
    # testing
    try:
        # attempt to delete the read-only file and verify the function returns False
        assert file_manager.delete_file(file) == False, f"Invalid deleted a read-only file"
    except AssertionError:
        raise AssertionError
    except Exception:
        raise RuntimeError
    finally:
        # reset write permissions so that it can be cleaned up
        os.chmod(file, stat.S_IWRITE)
        # teardown
        teardown(file)


if __name__ == "__main__":
    # taking arguments from the command line
    # call: python3 run_tests.py --select pattern
    # python3 run_tests.py --select -> invalid
    # python3 run_tests.py -> valid runs all tests
    # python3 run_tests.py --select pattern -> valid runs all tests that contain pattern in name
    # python3 run_tests.py --select pattern1 pattern2 -> valid runs all tests that contain pattern1 or pattern2 in name

    # check if length of call is valid
    # python3 run_tests.py -> length = 1
    # python3 run_tests.py --select -> length = 2
    # python3 run_tests.py --select read -> length = 3
    assert len(sys.argv) != 2, f"Usage: python3 run_tests.py or python3 run_tests.py --select pattern"

    if len(sys.argv) == 1:
        # python3 run_tests.py -> run all tests
        print(introspection())
    else:
        # check if call is valid
        # python3 run_tests.py --select pattern -> valid
        # python3 run_tests.py --choose pattern -> invalid
        assert sys.argv[1] == "--select", f"Usage: python3 run_tests.py --select pattern_required pattern_optional"
        print(introspection(sys.argv[2:]))