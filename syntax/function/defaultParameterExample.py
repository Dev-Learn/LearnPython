def showInfo(name, gender="Male", country="US"):
    print("Name: ", name)
    print("Gender: ", gender)
    print("Country: ", country)


# Valid
showInfo("Aladdin", "Male", "India")

print(" ------ ")

# Valid
showInfo("Tom", "Male")

print(" ------ ")

# Valid
showInfo("Jerry")

print(" ------ ")

# Valid
showInfo(name="Tintin", country="France")

print(" ------ ")