SELECT T.TagID,
    T.Title,
    T.Implements,
FROM Tags T
WHERE T.Owner = %(OwnerContributorID)s AND T.Title = %(Title);