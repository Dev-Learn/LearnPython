from syntax.exception import ageexception
from syntax.exception.ageexception import AgeException

print("Start Recruiting ...")

age = 51

print("Check your Age ", age)

try:

    ageexception.checkAge(age)

    print("You pass!")


except AgeException as e:

    print("You are not pass!")
    print("type(e): ", type(e))
    print("Cause message: ", str(e))
    print("Invalid age: ", e.age)