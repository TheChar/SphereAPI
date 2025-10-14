DO $$
DECLARE is_contributor BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO is_contributor
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

IF NOT is_contributor
THEN
RAISE EXCEPTION 'User cannot add a contributor to a project they do not contribute to';
END IF;

INSERT INTO ProjectContributor (ProjectID, ContributorID, IsOwner, IsRemoved)
VALUES (%(ProjectID)s, %(NewContributorID)s, FALSE, FALSE);

RETURN 'Success';
END $$;