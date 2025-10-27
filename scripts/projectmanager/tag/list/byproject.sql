DO $$
BEGIN

SELECT T.Title,
    PT.Implementations
FROM ProjectTag PT
LEFT JOIN Tags T ON PT.TagID = T.TagID
WHERE PT.ProjectID = %(ProjectID)s;

END $$;