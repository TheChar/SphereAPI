SELECT T.TagID,
    T.Title,
    T.Implements,
    T.IsPublic,
    T.Owner,
    C.Name AS OwnerName,
    COUNT(DISTINCT PT.ProjectTagID) AS NumImplementations
FROM Tags T
LEFT JOIN Contributors C ON T.Owner = C.ContributorID
LEFT JOIN ProjectTag PT ON PT.TagID = T.TagID
WHERE Owner = %(OwnerID)s AND IsPublic = TRUE
GROUP BY T.TagID, T.Title, T.Implements::jsonb, T.IsPublic, T.Owner, C.Name;