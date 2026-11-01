class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """First in, first out. Items join at the rear and leave from the front."""
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear:
            self.rear.next = new_node
        else:
            self.front = new_node
        self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None
        removed_node = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return removed_node.data

    def peek(self):
        if self.front is None:
            return None
        return self.front.data

    def clear(self):
        self.front = self.rear = None
        self.size = 0

    def items(self):
        """Return the queue contents from front to rear (for display)."""
        data, current_node = [], self.front
        while current_node:
            data.append(current_node.data)
            current_node = current_node.next
        return data


if __name__ == "__main__":
    q = Queue()
    for value in [10, 20, 30]:
        q.enqueue(value)
    print("Queue:", q.items(), "| dequeue ->", q.dequeue(), "|", q.items())
