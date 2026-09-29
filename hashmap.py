from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity=11, function: callable = hash_function_1):
        """
        Initialize the hashmap with a given capacity.
        Default capacity is 11, cannot be set to anything negative. Must be a prime number.
        """

        # Ensure that the capacity is a prime number to reduce collisions and improve distribution
        self._buckets = DynamicArray()
        self._capacity = capacity
        if self._capacity < 0:
            raise ValueError("Capacity cannot be negative.")
        self._capacity = self._next_prime(capacity)
        for bucket in range(self._capacity):
            self._buckets.append(LinkedList())

        # assigns additional attributes to the hashmap - the hash function and initial size tracking
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """Print all buckets which is mainly just for debugging"""
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out


    # Check if number is prime, primarily to ensure as little collisions as possible
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

    def put(self, key: str, value: object) -> None:
        """
        Add or update a key-value pair in the hash map.
        """

        # Resizing the table if the load factor is greater than or equal to 1.0, to ensure that
        # the table has enough capacity to accommodate new entries and maintain efficient performance.
        # This prevents collision chains from becoming too long and keeps average lookup time at O(1).
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # ensures the hash index is calculated correctly based on the current capacity, by using
        # modulo operator to wrap around the index if it exceeds the capacity of the hashmap
        hash_index = self._hash_function(key) % self._capacity
        chain = self._buckets.get_at_index(hash_index)

        # calling the chain to get the linked list at this bucket for collision handling
        if chain.length() == 0:
            # if the bucket is empty, we can directly insert the key-value pair without searching
            chain.insert(key, value)
            self._size += 1
            return

        # for each node in the chain, if the key already exists, remove it and insert the new value.
        # If the key does not exist, insert the new key-value pair at the end of the chain.
        # This handles collisions by storing multiple entries in the same bucket as a linked list.
        else:
            for node in chain:
                if node.key == key:
                    # key found - update its value without incrementing size since it already existed
                    chain.remove(key)
                    chain.insert(key, value)
                    return
            # key was not found in the chain, so insert it as a new entry and increment the size
            chain.insert(key, value)
            self._size += 1

    def get(self, key: str):
        """
        Return the value associated with the given key.
        """

        # ensures the hash index is calculated correctly based on the current capacity, by using
        # modulo operator to wrap around the index if it exceeds the capacity of the hashmap
        hash_index = self._hash_function(key) % self._capacity
        # makes the chain linked to the corresponding bucket calculated at the hash index
        chain = self._buckets.get_at_index(hash_index)
        # asks if the chain length is 0, if it's 0 it returns none because the key cannot exist in an empty bucket
        if chain.length() == 0:
            return None
        # but if the chain length is not 0, it loops through the chain to find the node with the matching key
        # and returns its value. If no matching key is found, it returns None because the key does not exist in this hashmap.
        else:
            for node in chain:
                if node.key == key:
                    return node.value

        return None


    def remove(self, key: str) -> None:
        """
        Delete a key-value pair.
        """

        # sets the chain to the corresponding bucket depending on the hash index that was calculated,
        # using the same hash function and modulo to ensure we check the correct bucket
        hash_index = self._hash_function(key) % self._capacity
        chain = self._buckets.get_at_index(hash_index)
        # ensures the hash index is calculated correctly based on the current capacity, by using modulo
        # operator to wrap around the index if it exceeds the capacity of the hashmap
        if chain.length() == 0:
            # bucket is empty, so the key cannot exist here, return early without doing anything
            return
        # if the chain length is not 0, it loops through the chain to find the node with the matching key
        # and removes it from the chain. If no matching key is found, it does nothing and returns.
        else:
            for node in chain:
                if node.key == key:
                    # found the key - remove it from the chain and decrement size to reflect the removal
                    chain.remove(key)
                    self._size -= 1
                    return

    def contains_key(self, key: str) -> bool:
        """
        Check if key exists in the map by searching all buckets and their chains.
        """
        # we must check all buckets in the table since we don't know which bucket contains the key without hashing it
        for i in range(self._capacity):
            # get the chain (linked list) at each bucket index
            chain = self._buckets.get_at_index(i)
            # if the chain is not empty, search through it for the matching key
            if chain.length() > 0:
                for node in chain:
                    if node.key == key:
                        # key found in this bucket's chain, return True immediately
                        return True
        # if we've checked all buckets and chains without finding the key, it doesn't exist in the map
        return False

    def empty_buckets(self) -> int:
        """
        Count how many buckets are empty. This helps us analyze the distribution of our hash function.
        """
        count = 0
        # loop through each bucket in the hash table to count how many have no entries
        for i in range(self._capacity):
            # get the chain at this bucket index
            chain = self._buckets.get_at_index(i)
            # if the chain length is 0, this bucket is empty and contributes to our count
            if chain.length() == 0:
                count += 1
            # otherwise continue to check the next bucket
            else:
                continue
        return count

    def table_load(self) -> float:
        """
        Calculate load factor = size / capacity. This tells us the average number of items per bucket.
        """
        # the load factor helps us determine when to resize. When it reaches 1.0, we resize to maintain O(1) performance
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Remove all entries but keep the same capacity so we don't waste the allocated space.
        """
        # create a fresh DynamicArray for buckets to clear all stored data
        self._buckets = DynamicArray()
        # reset the size to 0 since we're removing all entries from the map
        self._size = 0
        # reinitialize all buckets with empty linked lists, preserving the original capacity
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the table to new_capacity and rehash all entries into the new table structure.
        """
        # Check if new_capacity is less than 1. If it is then do nothing since we need at least one bucket
        if new_capacity < 1:
            return

        # A check for a new capacity with a prime number size to ensure good distribution and reduce collisions
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # First, create a new Hashmap with the new capacity and same hash function for consistency
        new_table = HashMap(new_capacity, self._hash_function)

        # this is to prevent next_prime from going to 3, when it should stay at 2 (since 2 is prime)
        if new_capacity == 2:
            new_table._capacity = 2

        # loop through all existing buckets in the old table and rehash all entries
        for i in range(self._capacity):
            # get the chain at this bucket in the old table
            chain = self._buckets.get_at_index(i)
            # if the chain is not empty, we need to rehash all its entries into the new table
            if chain.length() > 0:
                # iterate through each node in the chain to retrieve its key-value pair
                for node in chain:
                    # use the new table's put method to rehash each entry - this recalculates
                    # hash indices based on the new capacity, ensuring proper distribution
                    new_table.put(node.key, node.value)

        # Reassigning new values to self to make the old table be replaced with the new resized table
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table._capacity

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        The order of the keys in the dynamic array does not matter.
        """
        # create a new DynamicArray to store all the key-value pairs as tuples
        da = DynamicArray()

        # loop through all buckets in the hash table
        for i in range(self._capacity):
            # get the chain (linked list) at this bucket index
            chain = self._buckets.get_at_index(i)
            # if the chain is not empty, there are entries to collect from this bucket
            if chain.length() > 0:
                # iterate through each node in the chain to get its key-value pair
                for node in chain:
                    # append a tuple of (key, value) to our result array
                    da.append((node.key, node.value))

        return da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    A standalone function outside of the HashMap class that receives a dynamic array (not guaranteed to be sorted).
    Returns a tuple containing, in this order, a dynamic array comprising the mode (most occurring) value/s of the
    array, and an integer that represents the highest frequency (how many times they appear).

    If more than one value has the highest frequency, all values at that frequency is included in the array
    being returned (order does not matter). If there is only one mode, the dynamic array will only contain that
    value.

    The input array must contain at least one element, and that all values stored in the array will be strings.

    Implemented in O(N) time complexity. A separate chaining hash map is recommended.
    """
    # if you'd like to use a hash map, use this instance of your Separate Chaining HashMap
    map = HashMap()
    # first pass: count the frequency of each value in the input array by iterating through all elements
    for i in range(da.length()):
        # get the current value from the input array
        value = da.get_at_index(i)
        # check if this value has been seen before using the hash map
        if not map.contains_key(value):
            # if not seen before, initialize its count to 1
            map.put(value, 1)
        else:
            # if already seen, increment its count to track how many times it appears
            current_count = map.get(value)
            map.put(value, current_count + 1)

    # second pass: find the highest frequency value among all entries in the frequency map
    frequency = 0
    # get all key-value pairs from the frequency map where key is the value and value is the count
    arr = map.get_keys_and_values()
    # iterate through all frequency pairs to find the maximum count
    for i in range(arr.length()):
        # unpack the pair to get the value and its frequency
        value, count = arr.get_at_index(i)
        # track the highest frequency we've seen so far
        if frequency < count:
            frequency = count

    # third pass: collect all values that have the highest frequency into the result array
    mode_arr = DynamicArray()
    # iterate through all frequency pairs again to find all values with the maximum frequency
    for i in range(arr.length()):
        # unpack the pair to get the value and its frequency
        value, count = arr.get_at_index(i)
        # if this value's frequency matches the maximum frequency, it's a mode value
        if count == frequency:
            # add this mode value to our result array
            mode_arr.append(value)

    # return a tuple containing a dynamic array of the most frequent values and the frequency
    return mode_arr, frequency
 

        #underscores are set to help indicate that these attributes are intended for internal use within the class and should not be accessed directly from outside the class.
  