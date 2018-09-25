def toInteger(text):
    try:

        print("-- Begin parse text: ", text)

        # Một ngoại lệ có thể bị ném ra tại đây (ValueError).
        value = int(text)

        return value

    except ValueError as e:

        # Trường hợp 'text' không là một số.
        # Khối 'except' sẽ được thực thi.
        print("ValueError message: ", str(e))
        print("type(e): ", type(e))

        # Trả về 0 nếu xuất hiện lỗi ValueError.
        return 0


    finally:

        print("-- End parse text: " + text)


text = "001234A2"

value = toInteger(text)

print("Value= ", value)