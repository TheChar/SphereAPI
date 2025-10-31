DO $$
DECLARE
new_cont_id INT;
BEGIN
INSERT INTO ProjectContributor (ProjectID, ContributorID, IsOwner, IsRemoved)
VALUES (%(ProjectID)s, %(NewContributorID)s, FALSE, FALSE)
RETURNING ProjectContributorID INTO new_cont_id;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version)
VALUES (NOW(), new_cont_id, 'Joined Project', (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s));
END $$;