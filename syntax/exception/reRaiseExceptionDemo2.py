def checkScore(score):
    if score < 0 or score > 100:
        raise Exception("Invalid Score " + str(score))


def checkPlayer(name, score):
    try:

        checkScore(score)

    except Exception as e:

        print("Something invalid with player: ", name, ' >> ', str(e))

        # throw new exception.
        raise Exception("Something invalid with player: " + name + " >> " + str(e))


        # ------------------------------------------


checkPlayer("Tran", 101)