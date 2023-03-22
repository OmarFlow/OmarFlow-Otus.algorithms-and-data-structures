def search_bmh(text: str, mask: str) -> int:
    """
    Поиск подстроки, улучшенный, алгоритмом Бойера-Мура-Хорспула
    """
    if text[:len(mask)] == mask:
        return 0

    #создаём карту сдвигов для букв маски
    shift_map_letter = dict()
    for ind, letter in enumerate(reversed(mask[:-1])):
        ind += 1

        #если подобного значения еще нет, сразу присваиваем индекс
        if shift_map_letter.get(letter) is None:
            shift_map_letter[letter] = ind
        # если есть, оставляем существующий индекс
        else:
            continue

    if mask.count(mask[-1]) > 1:
        # ищем индекс последеней буквы маски, если она повторяется
        for ind, value in enumerate(reversed(mask)):
            if value == mask[-1]:
                shift_map_letter[mask[-1]] = ind
    else:
        shift_map_letter[mask[-1]] = len(mask)

    t = 0
    while t <= len(text) - len(mask):
        if t < len(text) - len(mask):
            # если последний символ длины маски в тексте, не равен последнему символу маски, сдвигаемся на 1
            if text[t + len(mask) - 1] != mask[-1]:
                t += 1
            # если совсем нет в маске, прыгаем на длину маски
            elif text[t + len(mask) - 1] not in set(mask):  # not in set(mask):
                t += len(mask) - 1
            # если присутствует в маске, сразу прыгаем на значение из таблицы
            else:
                t += shift_map_letter[text[t + len(mask) - 1]]

        m = 0
        while m < len(mask) and text[t + m] == mask[m]:
            m += 1
        if m == len(mask):
            return t
    return -1


def search_bm(text: str, mask: str) -> int:
    """
    Поиск подстроки, улучшенный, алгоритмом Бойера-Мура(для использования нужно модифицировать алгоритм для работы с подобными шаблонами: "aaa")
    """
    if text[:len(mask)] == mask:
        return 0

    #создаём карту сдвигов для суффиксов
    map_suff = {}
    if len(mask) >= 9:
        suff = mask[(len(mask) + 1) // 2:]
        h = ''
        for i in range(len(suff)-1, -1, -1):
            h = h + suff[i]
            ind = mask[:-(len(suff) - i)][::-1].find(h)
            if ind != -1:
                map_suff[h] = ind + len(suff) - i

    t = 0
    while t <= len(text) - len(mask):
        if t < len(text) - len(mask):
            if len(mask) == 1 and text[t] != mask[0]:
                t += 1
                continue
            elif len(mask) == 1 and text[t] == mask[0]:
                return t

            # если совсем нет в маске, прыгаем на длину маски
            if text[t + len(mask) - 1] not in set(mask):
                t += len(mask) - 1
            # если последний символ длины маски в тексте, не равен последнему символу маски, сдвигаемся на 1
            elif text[t + len(mask) - 1] != mask[-1]:
                t += 1
            # если присутствует в маске, сразу прыгаем на значение из таблицы
            else:
                if len(mask) >= 9:
                    m = len(mask) - 1
                    pattern = ''
                    while m >= 0 and text[t + m] == mask[m]:
                        pattern += text[t + m]
                        m -= 1
                    shift = map_suff.get(pattern, 1)
                    t += shift
        m = len(mask) - 1
        if text[t] == mask[m]:
            return t
        while m >= 0 and text[t + m] == mask[m]:
            m -= 1
        if m < 0:
            return t
    return -1
