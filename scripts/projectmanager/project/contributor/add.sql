DO $$
DECLARE is_contributor BOOLEAN,
new_cont_id BOOLEAN;
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
VALUES (%(ProjectID)s, %(NewContributorID)s, FALSE, FALSE)
RETURNING ProjectContributorID INTO new_cont_id;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version)
VALUES (NOW(), new_cont_id, 'Joined Project', (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s));

RETURN 'Success';
END $$;