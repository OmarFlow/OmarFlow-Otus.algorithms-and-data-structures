class QueueKnownProirity:
    def __init__(self, priority):
        self.priority = priority
        self.container_array = [[] for _ in range(priority)]

    def dequeue(self):
        for i in range(len(self.container_array)):
            if self.container_array[i]:
                for j in range(len(self.container_array[i])):
                    res = self.container_array[i][j]
                    del self.container_array[i][j]
                    return res
            continue

    def enqueue(self, priority, item):
        priority_array = self.container_array[priority]
        priority_array.append(item)


class QueueUnknownPriority:
    def __init__(self):
        self.array = []

    def dequeue(self):
        if self.array:
            for i in range(len(self.array)):
                res = self.array[i]
                del self.array[i]
                return res

    def enqueue(self, priority_and_item):
        if not self.array:
            self.array.append(priority_and_item)
            return

        for i in range(len(self.array)):
            prio, value = self.array[i]
            if priority_and_item[0] < prio:
                self.array.insert(i, priority_and_item)
                break
            if i == len(self.array) - 1:
                self.array.append(priority_and_item)

