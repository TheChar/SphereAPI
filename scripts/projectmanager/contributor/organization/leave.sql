DO $$
DECLARE is_owner BOOLEAN;
BEGIN

--Get if contributor is owner
SELECT IsOwner
INTO is_owner
FROM ContributorOrganization
WHERE ContributorID = %(contributorID)s
AND OrganizationID = (SELECT OrganizationID FROM Organizations WHERE Title = %(OrgTitle)s);

--Exception handling
IF is_owner
THEN
RAISE EXCEPTION "User cannot leave an organization they own";
END IF;

--Leave org
DELETE FROM ContributorOrganization
WHERE ContributorID = %(contributorID)s AND OrganizationID = (SELECT OrganizationID FROM Organizations WHERE Title = %(OrgTitle)s);
RETURNING "Success";