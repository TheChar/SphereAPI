DO $$
DECLARE proj_id INT,
    proj_con_id INT;
BEGIN
--Create project
INSERT INTO Projects (Title, Description, Version)
VALUES (%(Title)s, %(Description)s, %(Version)s)
RETURNING ProjectID INTO proj_id;
--Bind owner to project
INSERT INTO ProjectContributor (ProjectID, ContributorID, IsRemoved, IsOwner)
VALUES (proj_id, %(ContributorID)s, FALSE, TRUE);
RETURNING ProjectContributorID INTO proj_con_id;
--Insert creation record in time entries
INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version)
VALUES (NOW(), proj_con_id, 'Created ' || %(Title)s, %(Version)s);
INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version)
VALUES (NOW(), proj_con_id, 'Joined ' || %(Title)s, %(Version)s);

RETURN "Success";
END $$;