DO $$
DECLARE proj_id INT;
    proj_con_id INT;
BEGIN
--Create project
INSERT INTO Projects (Title, Description, Version)
VALUES (%(Title)s, %(Description)s, %(Version)s)
RETURNING ProjectID INTO proj_id;
--Bind owner to project
INSERT INTO ProjectContributor (ProjectID, ContributorID, IsRemoved, IsOwner)
VALUES (proj_id, %(ContributorID)s, FALSE, TRUE)
RETURNING ProjectContributorID INTO proj_con_id;
--Insert creation record in time entries
INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ), 
    proj_con_id, 
    CONCAT('Created ', %(Title)s), 
    TRUE, 
    %(Version)s);
INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ), 
    proj_con_id, 
    'Joined Project', 
    TRUE, 
    %(Version)s);
END $$;