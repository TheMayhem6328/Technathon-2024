from retrieve_words import wordlist
from re import search


def validate_wifi_password(password: str) -> bool:
    # Length check

    if len(password) < 12:
        return False

    # Consequent check

    for position in range(len(password) + 1):
        # Get `n`th character of `password` and two more after it
        check: str = password[position : position + 3]

        # Get `n`th character
        check_head: str = check[0]

        # Generate string of three consequent characters
        # Starting from chr(n)
        consequent: str = "".join(
            [chr(i) for i in range(ord(check_head), ord(check_head) + 3)]
        )

        # Check whether the three characters we selected from `password`
        # match the string of consequent characters
        #
        # Yes, this might invalidate sequences like `@ab`,
        # which are not consequent alphabets, but
        # that's expected since if it's a computer
        # generated password which generate passwords
        # the same way I generate this consequent string,
        # it could be susceptible to attacks which try out
        # strings generated in the same manner.
        #
        # This is why I'm not looking for solely
        # alphanumeric sequences, but any sequence
        # of consequent characters
        if check == consequent:
            return False

    # Charset check

    # Initialize variables
    flag: int = 0
    found_uppercase: bool = False
    found_lowercase: bool = False
    found_digit: bool = False
    found_special: bool = False

    # Alter flag according to whatever is found
    #
    # Flag is basically how many character sets
    # were found in the password
    for char in password:
        if char.isupper():
            if not found_uppercase:
                found_uppercase = True
                flag += 1
        elif char.islower():
            if not found_lowercase:
                found_lowercase = True
                flag += 1
        elif char.isnumeric():
            if not found_digit:
                found_digit = True
                flag += 1
        else:
            if not found_special:
                found_lowercase = True
                flag += 1
    if flag < 3:
        return False

    # Dictionary check

    common = wordlist().common(password)
    if not common:
        return False

    # If all checks pass, return True
    return True
