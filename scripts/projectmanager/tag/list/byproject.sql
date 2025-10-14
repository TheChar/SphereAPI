DO $$
DECLARE is_cont BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO is_cont
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

IF NOT is_cont
THEN
RAISE EXCEPTION 'User cannot get tags from a project they do not contribute to';
END IF;

SELECT T.Title,
    PT.Implementations
FROM ProjectTag PT
LEFT JOIN Tags T ON PT.TagID = T.TagID
WHERE PT.ProjectID = %(ProjectID)s;

END $$;