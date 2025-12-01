SELECT T.TagID,
    T.Title,
    PT.Implementations,
    T.Owner,
    T.IsPublic
FROM ProjectTag PT
LEFT JOIN Tags T ON PT.TagID = T.TagID
WHERE PT.ProjectID = %(ProjectID)s;