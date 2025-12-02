SELECT T.TagID,
    T.Title,
    T.Implements,
    T.IsPublic,
    T.Owner,
    C.Name AS OwnerName
FROM Tags T
LEFT JOIN Contributors C ON T.Owner = C.ContributorID
WHERE Owner = %(OwnerID)s AND IsPublic = TRUE;