DO $$
DECLARE org_id INT;
BEGIN
--Create the organization
INSERT INTO Organizations (Title)
VALUES (%(OrgTitle)s)
RETURNING OrganizationID INTO org_id;
--Assign the creator as the owner
INSERT INTO ContributorOrganization (ContributorID, OrganizationID, IsOwner)
VALUES (%(ContributorID)s, org_id, TRUE)
RETURNING "Success";
END $$;