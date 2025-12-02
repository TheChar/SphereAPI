DO $$
DECLARE
new_cont_id INT;
BEGIN
INSERT INTO ProjectContributor (ProjectID, ContributorID, IsOwner, IsRemoved)
VALUES (%(ProjectID)s, %(NewContributorID)s, FALSE, FALSE)
RETURNING ProjectContributorID INTO new_cont_id;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ), 
    new_cont_id, 
    'Joined Project', 
    TRUE, 
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s));
END $$;