def checkScore(score):
    if score < 0 or score > 100:
        raise Exception("Invalid Score " + str(score))


def checkPlayer(name, score):
    try:

        checkScore(score)

    except Exception as e:

        print("Something invalid with player: ", name, ' >> ', str(e))

        # re throw exception.
        raise


        # ------------------------------------------


checkPlayer("Tran", 101)