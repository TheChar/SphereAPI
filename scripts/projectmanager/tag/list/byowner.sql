SELECT T.TagID,
    T.Title,
    T.Implements::jsonb,
    T.IsPublic,
    T.Owner,
    C.Name AS OwnerName,
    COUNT(DISTINCT PT.ProjectTagID) AS NumImplementations
FROM Tags T
LEFT JOIN Contributors C ON T.Owner = C.ContributorID
LEFT JOIN ProjectTag PT ON PT.TagID = T.TagID
WHERE T.Owner = %(OwnerID)s
    AND (%(ContributorID)s = %(OwnerID)s OR IsPublic = TRUE)
GROUP BY T.TagID, T.Title, T.Implements::jsonb, T.IsPublic, T.Owner, C.Name;