SELECT T.Title,
    T.Implements,
    T.IsPublic,
    C.Name,
    C.ContributorID,
    COUNT(DISTINCT PT.ProjectTagID) AS NumImplementations
FROM Tags T
LEFT JOIN Contributors C ON C.ContributorID = T.Owner
LEFT JOIN ProjectTag PT ON PT.TagID = T.TagID
WHERE T.TagID = %(TagID)s;