DO $$
DECLARE new_is_contributor BOOLEAN,
org_id INT,
caller_is_owner BOOLEAN;
BEGIN

--Get organization id
SELECT OrganizationID
INTO org_id
FROM Organizations
WHERE Title = %(OrgTitle)s;
--Get if new owner is org contributor already
SELECT COUNT(ContributorOrganizationID) > 0
INTO new_is_contributor
FROM ContributorOrganization
WHERE ContributorID = %(NewOwnerContID)s AND OrganizationID = org_id;
--Get if caller is owner
SELECT IsOwner
INTO caller_is_owner
FROM ContributorOrganization
WHERE ContributorID = %(ContributorID)s AND OrganizationID = org_id;

--Exception handling
IF NOT new_is_contributor
THEN
RAISE EXCEPTION 'You cannot transfer ownership to a non-organization member.';
END IF;
IF NOT caller_is_owner
THEN
RAISE EXCEPTION 'You cannot transfer ownership of an organization you do not own!';

UPDATE ContributorOrganization
SET IsOwner = TRUE
WHERE ContributorID = %(NewOwnerContID)s AND OrganizationID = org_id;

UPDATE ContributorOrganization
SET IsOwner = FALSE
WHERE ContributorID = %(ContributorID)s AND OrganizationID = org_id;
RETURN 'Success';
END $$;