SELECT P.ProjectID,
    P.Title
FROM Projects P
LEFT JOIN ProjectTag PT ON PT.TagID = T.TagID
WHERE PT.TagID = %(TagID)s;