DO $$
DECLARE is_owner BOOLEAN;
BEGIN

SELECT IsOwner
INTO is_owner
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

IF NOT is_owner
THEN
RAISE EXCEPTION 'User cannot delete project they do not own';
END IF;

--Delete time entries
DELETE FROM TimeEntries
WHERE ProjectContributorID IN (
    SELECT ProjectContributorID
    FROM ProjectContributor
    WHERE ProjectID = %(ProjectID)s
);

--Unbind Contributors
DELETE FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s;

--Unbind tags
DELETE FROM ProjectTag
WHERE ProjectID = %(ProjectID)s;

--Delete Project
DELETE FROM Projects
WHERE ProjectID = %(ProjectID)s;
RETURN 'Success';

END $$;