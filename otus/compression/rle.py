def rle(text):
    """
    Улучшенный метод сжатия RLE
    """
    encoded_string = ""
    i = 0
    while (i <= len(text)-1):
        count = 1
        ch = text[i]
        j = i
        while (j < len(text)-1):
            if (text[j] == text[j + 1]):
                count = count + 1
                j = j + 1
            else:
                break

        if not encoded_string:
            encoded_string = encoded_string + str(count) + ch
            i = j + 1
            continue

        if encoded_string[-2] == '1' or not encoded_string[-2].isnumeric():
            if count == 1:
                encoded_string += ch
            else:
                encoded_string += str(count) + ch
        else:
            encoded_string += str(count) + ch
        i = j + 1
    return encoded_string