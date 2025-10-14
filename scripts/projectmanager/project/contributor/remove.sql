DO $$
DECLARE is_owner BOOLEAN;
BEGIN

SELECT IsOwner
INTO is_owner
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

--Cannot remove self if owner
IF is_owner AND %(ContributorID)s == %(RemovedContributorID)s
THEN
RAISE EXCEPTION 'User cannot remove self if they are owner. Transfer or delete.';
END IF;
--Cannot remove others if not owner
IF NOT is_owner AND %(ContributorID)s != %(RemovedContributorID)s
THEN
RAISE EXCEPTION 'Only the project owner can remove other contributors from a project';
END IF;

UPDATE ProjectContributor
SET IsRemoved = TRUE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RemovedContributorID)s;
RETURN 'Success';
END $$;