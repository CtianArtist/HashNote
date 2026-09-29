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

    def __str__(self) -> str:
        """Print all buckets - helpful for debugging"""
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out
 
    def _next_prime(self, capacity: int) -> int:
        """Find the next prime number >= capacity"""
        if capacity % 2 == 0:
            capacity += 1
 
        while not self._is_prime(capacity):
            capacity += 2
 
        return capacity
 
    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """Check if a number is prime"""
        if capacity == 2 or capacity == 3:
            return True
 
        if capacity == 1 or capacity % 2 == 0:
            return False
 
        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2
 
        return True
 
    def get_size(self) -> int:
        """Return the number of entries in the map"""
        return self._size
 
    def get_capacity(self) -> int:
        """Return the number of buckets"""
        return self._capacity
 
    # ===== METHODS YOU NEED TO IMPLEMENT ===== #
 
    def put(self, key: str, value: object) -> None:
        """
        Add or update a key-value pair.
 
        IMPLEMENT:
        1. IF table_load() >= 1.0:
              Call resize_table(capacity * 2)
 
        2. Calculate: hash_index = _hash_function(key) % capacity
 
        3. Get the chain: chain = _buckets.get_at_index(hash_index)
 
        4. IF chain is empty (chain.length() == 0):
              chain.insert(key, value)
              Increment _size
              Return
 
        5. ELSE (chain has items):
              Loop through chain:
                 IF you find a node with matching key:
                    chain.remove(key)
                    chain.insert(key, value)
                    Return (DON'T increment size)
 
              // Key not found in chain
              chain.insert(key, value)
              Increment _size
        """
        pass
 
    def get(self, key: str):
        """
        Retrieve value for a key.
 
        IMPLEMENT:
        1. Calculate: hash_index = _hash_function(key) % capacity
 
        2. Get the chain: chain = _buckets.get_at_index(hash_index)
 
        3. IF chain is empty:
              Return None
 
        4. Loop through chain:
              IF node.key == key:
                 Return node.value
 
        5. Return None (key not found)
        """
        pass
 
    def remove(self, key: str) -> None:
        """
        Delete a key-value pair.
 
        IMPLEMENT:
        1. Loop through all buckets (0 to capacity):
              Get chain = _buckets.get_at_index(i)
 
              IF chain is NOT empty:
                 Loop through chain:
                    IF node.key == key:
                       chain.remove(key)
                       Decrement _size
                       Return
 
        2. (If we get here, key wasn't found - do nothing)
        """
        pass
 
    def contains_key(self, key: str) -> bool:
        """
        Check if key exists in the map.
 
        IMPLEMENT:
        1. Loop through all buckets (0 to capacity):
              Get chain = _buckets.get_at_index(i)
 
              IF chain is NOT empty:
                 Loop through chain:
                    IF node.key == key:
                       Return True
 
        2. Return False (key not found anywhere)
        """
        pass
 
    def empty_buckets(self) -> int:
        """
        Count how many buckets are empty.
 
        IMPLEMENT:
        1. Set count = 0
 
        2. Loop through all buckets (0 to capacity):
              IF _buckets.get_at_index(i).length() == 0:
                 Increment count
 
        3. Return count
        """
        pass
 
    def table_load(self) -> float:
        """
        Calculate load factor = size / capacity.
 
        IMPLEMENT:
        1. Calculate and return: _size / _capacity
           (This is just one line!)
        """
        pass
 
    def clear(self) -> None:
        """
        Remove all entries but keep the same capacity.
 
        IMPLEMENT:
        1. Set _buckets = DynamicArray() (fresh array)
 
        2. Set _size = 0
 
        3. Loop from 0 to capacity:
              Append empty LinkedList() to _buckets
        """
        pass
 
    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the table to new_capacity and rehash all entries.
 
        IMPLEMENT:
        1. IF new_capacity < 1:
              Return (do nothing)
 
        2. IF new_capacity is NOT prime:
              Set new_capacity = _next_prime(new_capacity)
 
        3. Create new_table = HashMap(new_capacity, _hash_function)
 
        4. Edge case: IF new_capacity == 2:
              Set new_table._capacity = 2 (bypass next_prime quirk)
 
        5. Loop through old buckets (0 to old capacity):
              Get chain = _buckets.get_at_index(i)
 
              IF chain is NOT empty:
                 Loop through chain:
                    Call new_table.put(node.key, node.value)
                    (This rehashes everything!)
 
        6. Copy over new values:
              _buckets = new_table._buckets
              _size = new_table._size
              _capacity = new_table._capacity
        """
        pass
 
    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray containing all (key, value) tuples.
 
        IMPLEMENT:
        1. Create result = DynamicArray()
 
        2. Loop through all buckets (0 to capacity):
              Get chain = _buckets.get_at_index(i)
 
              IF chain is NOT empty:
                 Loop through chain:
                    Append tuple (node.key, node.value) to result
 
        3. Return result
        """
        pass
 
 
def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Find the most frequently occurring value(s) in an array.
 
    Returns tuple: (DynamicArray of mode values, frequency count)
 
    IMPLEMENT:
    1. Create frequency_map = HashMap()
 
    2. Loop through da (0 to da.length()):
          Get value = da.get_at_index(i)
 
          IF NOT frequency_map.contains_key(value):
             frequency_map.put(value, 1)
          ELSE:
             old_count = frequency_map.get(value)
             frequency_map.put(value, old_count + 1)
 
    3. Find highest frequency:
          Set highest = 0
          Get all_pairs = frequency_map.get_keys_and_values()
 
          Loop through all_pairs:
             Get (value, count) = all_pairs.get_at_index(i)
             IF count > highest:
                Set highest = count
 
    4. Collect all values with highest frequency:
          Create mode_array = DynamicArray()
 
          Loop through all_pairs:
             Get (value, count) = all_pairs.get_at_index(i)
             IF count == highest:
                Append value to mode_array
 
    5. Return (mode_array, highest)
    """
    pass
 

        #underscores are set to help indicate that these attributes are intended for internal use within the class and should not be accessed directly from outside the class.
  