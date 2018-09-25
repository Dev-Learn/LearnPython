# Python 3.x:
# Ngoại lệ giới tính.
class GenderException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

        # Ngoại lệ ngôn ngữ.


class LanguageException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class PersonException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# Hàm này có thể ném ra GenderException.
def checkGender(gender):
    if gender != 'Female':
        raise GenderException("Accept female only")


# Hàm này có thể ném ra LanguageException.
def checkLanguage(language):
    if language != 'English':
        raise LanguageException("Accept english language only")


def checkPerson(name, gender, language):
    try:
        # Có thể ném ra GenderException.
        checkGender(gender)
        # Có thể ném ra LanguageException.
        checkLanguage(language)
    except Exception as e:
        # Bắt exception và ném ra ngoại lệ khác.
        # Ngoại lệ mới có thông tin __cause__ = e.
        raise PersonException(name + " does not pass") from e


# --------------------------------------------------------
try:

    checkPerson("Nguyen", "Female", "Vietnamese")

except PersonException as e:

    print("Error message: ", str(e))

    # GenderException hoặc LanguageException
    cause = e.__cause__

    print('e.__cause__: ', repr(cause))

    print("type(cause): ", type(cause))

    print(" ------------------ ")

    if type(cause) is GenderException:

        print("Gender exception: ", cause)

    elif type(cause) is LanguageException:

        print("Language exception: ", cause)