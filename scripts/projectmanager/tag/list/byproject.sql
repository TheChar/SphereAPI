SELECT T.TagID,
    T.Title,
    T.Implements::jsonb,
    PT.Implementations::jsonb,
    T.Owner,
    T.IsPublic,
    C.Name AS OwnerName
FROM ProjectTag PT
LEFT JOIN Tags T ON PT.TagID = T.TagID
LEFT JOIN Contributors C ON T.Owner = C.ContributorID
WHERE PT.ProjectID = %(ProjectID)s;