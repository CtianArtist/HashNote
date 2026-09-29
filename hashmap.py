class HashMap:
    def __init__(self, capacity=11, function: callable = hash_function_1):
        """
        Initialize the hashmap with a given capacity.
        Default capacity is 11, cannot be set to anything negative. Must be a prime number.
        """

        # Ensure that the capacity is a prime number
        self._buckets = DynamicArray()
        self._capacity = capacity
        if self.capacity < 0:
            raise ValueError("Capacity cannot be negative.")
        self._capacity = self._next_prime(capacity)
        for bucket in range(self._capacity):
            self._buckets.append(LinkedList())

        #ssigns additional attributes to the hashmap
        self._hash_function = function
        self._size = 0

        #underscores are set to help indicate that these attributes are intended for internal use within the class and should not be accessed directly from outside the class.
  