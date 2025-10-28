DO $$
DECLARE 
    org_id INT;
    is_owner BOOLEAN;
BEGIN
--Get org_id
SELECT OrganizationID
INTO org_id
FROM Organizations
WHERE Title = %(OrgTitle)s;
--Get ownership status
SELECT IsOwner
INTO is_owner
FROM ContributorOrganization
WHERE ContributorID = %(ContributorID)s AND OrganizationID = org_id;
--Exception handling
IF NOT is_owner
THEN
RAISE EXCEPTION 'User cannot dissolve an organization they dont own';
END IF;
--Remove users from org
DELETE FROM ContributorOrganization
WHERE OrganizationID = org_id;
--Delete organization
DELETE FROM Organizations
WHERE OrganizationID = org_id;
END $$;