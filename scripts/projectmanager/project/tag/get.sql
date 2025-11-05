SELECT TagID,
    ProjectID,
    Implementations
FROM ProjectTag
WHERE ProjectID = %(ProjectID)s AND TagID = %(TagID)s;