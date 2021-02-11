def get_ranks(records):
  """ TODO
  `records` must be a list of either `Player` or `Club` instances.

  :return: list of triplet, sorted by points (descending). Each element is as follow:
   - rank (starts at 1; can equal to previous rank in case of points equality)
   - points for current object
   - record (Player or Club instance)
  """
  ranks = [[None, record.points, record] for record in records]
  ranks.sort(key=lambda el: el[1], reverse=True)  # sort records by points (descending)
  for i, element in enumerate(ranks):
    previous_element = ranks[i-1]
    # if score of current element equals score of previous one: rank must be equal as well
    if i > 0 and element[1] == previous_element[1]:
      element[0] = previous_element[0]
    else:
      element[0] = i + 1
  return ranks
