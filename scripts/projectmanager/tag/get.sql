SELECT T.TagID,
    T.Title,
    T.Implements::jsonb,
    T.IsPublic,
    C.Name AS OwnerName,
    C.ContributorID AS OwnerID,
    COUNT(DISTINCT PT.ProjectTagID) AS NumImplementations
FROM Tags T
LEFT JOIN Contributors C ON C.ContributorID = T.Owner
LEFT JOIN ProjectTag PT ON PT.TagID = T.TagID
WHERE T.TagID = %(TagID)s
GROUP BY T.TagID, T.Title, T.Implements::jsonb, T.IsPublic, OwnerName, OwnerID;