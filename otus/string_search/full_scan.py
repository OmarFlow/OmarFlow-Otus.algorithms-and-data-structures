def search_full_scan(text: str, mask: str) -> int:
    """
    Реверсивный посик подстроки c не большой оптимизацией
    """
    t = 0
    while t <= len(text) - len(mask):
        if text[t + len(mask) - 1] != mask[-1]:
            t += len(mask) - 1
            continue
        m = 0
        while m < len(mask) and text[t + m] == mask[m]:
            m += 1
        if m < 0:
            return t
        t += 1
    return -1


def search_reverse_scan(text: str, mask: str) -> int:
    """
    Реверсивный посик подстроки
    """
    t = 0
    while t <= len(text) - len(mask):
        m = len(mask) - 1
        while m >= 0 and text[t + m] == mask[m]:
            m -= 1
        if m < 0:
            return t
        t += 1
    return -1
