SELECT T.Title,
    T.Implements,
    C.Name,
    C.ContributorID
    COUNT(DISTINCT ProjectTagID) AS NumImplementations
FROM Tags T
LEFT JOIN Contributors C ON T.Owner = C.ContributorID
LEFT JOIN ProjectTag PT ON T.TagID = PT.TagID
WHERE IsPublic = TRUE
LIMIT 30
OFFSET (30 * (%(Page)s - 1))
ORDER BY T.Title DESC;