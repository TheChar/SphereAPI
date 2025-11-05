SELECT T.TagID,
    T.Title,
    T.Implements::jsonb,
    C.Name AS OwnerName,
    C.ContributorID AS OwnerID,
    COUNT(DISTINCT ProjectTagID) AS NumImplementations
FROM Tags T
LEFT JOIN Contributors C ON T.Owner = C.ContributorID
LEFT JOIN ProjectTag PT ON T.TagID = PT.TagID
WHERE IsPublic = TRUE
GROUP BY T.TagID, T.Title, T.Implements::jsonb, OwnerName, OwnerID
ORDER BY T.Title DESC
LIMIT 30
OFFSET (30 * (%(Page)s - 1));