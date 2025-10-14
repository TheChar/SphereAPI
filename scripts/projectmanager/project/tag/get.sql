DO $$
DECLARE is_cont BOOLEAN,
    is_implemented BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO is_cont
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s AND IsRemoved = FALSE;

SELECT COUNT(ProjectTagID) > 0
INTO is_implemented
FROM ProjectTag
WHERE ProjectID = %(ProjectID)s AND TagID = %(TagID)s;

IF NOT is_cont
THEN
RAISE EXCEPTION 'User cannot get implementation of a tag on a project they do not contribute to';
END IF;

IF NOT is_implemented
THEN
RAISE EXCEPTION 'Project does not implement the given tag';
END IF;

SELECT Implementations
FROM ProjectTag
WHERE ProjectID = %(ProjectID)s AND TagID = %(TagID)s;

END $$;