DO $$
DECLARE is_owner BOOLEAN;
DECLARE is_public BOOLEAN;
BEGIN

SELECT %(ContributorID)s = (SELECT Owner FROM Tags WHERE TagID = %(TagID)s)
INTO is_owner;

SELECT IsPublic
FROM Tags
WHERE TagID = %(TagID)s;

IF NOT is_owner AND NOT is_public
THEN
RAISE EXCEPTION 'User cannot access data about a private tag they do not own';
END IF;

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

END $$;