DO $$
DECLARE is_owner BOOLEAN;
BEGIN

SELECT IsOwner
INTO is_owner
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

--Cannot restore if not owner
IF NOT is_owner
THEN
RAISE EXCEPTION 'User cannot restore a removed contributor without being the project owner';
END IF;

UPDATE ProjectContributor
SET IsRemoved = FALSE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RemovedContributorID)s;
RETURN 'Success';
END $$;