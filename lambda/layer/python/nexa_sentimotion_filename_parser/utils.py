import re


def get_digits_only(mixed_string):
    """
    :param mixed_string: some string that may contain digits and characters
    :return: only digits
    """
    ret = re.sub("\\D", "", mixed_string)
    return int(ret)


def name2list(file_name):
    return file_name.split("_")


def main():
    ret = get_digits_only("ver1")
    print(ret)
    print(type(ret))


if __name__ == "__main__":
    main()
