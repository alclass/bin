class UniqueTupleSet:
  def __init__(self):
    # Stores the actual unique tuples
    self.tuples_set = set()
    # Stores all first elements to check for uniqueness
    self.first_elements = set()
    # Stores all second elements to check for uniqueness
    self.second_elements = set()

  def add(self, new_tuple):
    """
    Adds a new tuple if both of its elements are unique across the
    entire collection and the tuple itself is new.
    """
    if not isinstance(new_tuple, tuple) or len(new_tuple) != 2:
      raise ValueError("Input must be a 2-element tuple")

    field1, field2 = new_tuple

    # Check for uniqueness constraints
    if new_tuple in self.tuples_set:
      print(f"Tuple {new_tuple} already exists in the collection. Ignoring.")
      return False
    if field1 in self.first_elements:
      print(f"First element '{field1}' is already in the collection's first fields. Ignoring.")
      return False
    if field2 in self.second_elements:
      print(f"Second element '{field2}' is already in the collection's second fields. Ignoring.")
      return False

    # If all checks pass, add to all tracking sets
    self.tuples_set.add(new_tuple)
    self.first_elements.add(field1)
    self.second_elements.add(field2)
    print(f"Added tuple {new_tuple}.")
    return True

  def get_collection(self):
    """Returns the collection of unique tuples."""
    return self.tuples_set

  def __len__(self):
    return len(self.tuples_set)

  def __contains__(self, item):
    return item in self.tuples_set


# Example Usage:
my_unique_set = UniqueTupleSet()

# Valid additions
my_unique_set.add(('A', 1))
my_unique_set.add(('B', 2))
my_unique_set.add(('C', 3))

# Invalid additions due to field repetition
my_unique_set.add(('A', 4))  # 'A' is repeated
my_unique_set.add(('D', 2))  # '2' is repeated

# Invalid addition due to full tuple repetition
my_unique_set.add(('B', 2))  # ('B', 2) is repeated

print("\nFinal unique tuple set:", my_unique_set.get_collection())
