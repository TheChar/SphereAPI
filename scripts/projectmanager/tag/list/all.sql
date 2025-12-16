SELECT T.TagID,
    T.Title,
    T.Implements::jsonb,
    T.IsPublic,
    C.Name AS OwnerName,
    T.Owner,
    COUNT(DISTINCT ProjectTagID) AS NumImplementations
FROM Tags T
LEFT JOIN Contributors C ON T.Owner = C.ContributorID
LEFT JOIN ProjectTag PT ON T.TagID = PT.TagID
WHERE (C.ContributorID = %(ContributorID)s OR (C.ContributorID != %(ContributorID)s AND T.IsPublic = TRUE))
    AND (
        %(SearchBy)s IS NULL
        OR T.Title ILIKE '%%' || %(SearchBy)s || '%%'
        OR C.Name ILIKE '%%' || %(SearchBy)s || '%%'
    )
GROUP BY T.TagID, T.Title, T.Implements::jsonb, T.IsPublic, OwnerName, T.Owner
ORDER BY {ORDER_BY}
LIMIT 30
OFFSET (30 * (%(Page)s - 1));