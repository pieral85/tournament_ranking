def get_ranks(records, sort_by=None):
  """ TODO
  `records`: list of either `Player` or `Club` instances.
  `sort_by`: field name of an instance for which the sort is done. If `None` (by default),
    default sort is applied (by points)

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

  if sort_by:
    try:
      ranks.sort(key=lambda el: getattr(el[2], sort_by))
    except AttributeError:
      pass

  return ranks
