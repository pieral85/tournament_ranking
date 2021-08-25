
def filter_records(records):
    """ Filter a list of records, based on their `id_internal` property
    (only accept one record per `id_internal` and excludes falsy ones).

    note: The model of the records needs to implement the method `id_internal`

    :return: dict_values of filtered records (can be considered as a list)
    """
    return {rec.id_internal: rec for rec in records if rec.id_internal}.values()
