DO $$
BEGIN

UPDATE ContributorOrganization
SET IsOwner = TRUE
WHERE ContributorID = %(NewOwnerContID)s AND OrganizationID = %(OrganizationID)s;

UPDATE ContributorOrganization
SET IsOwner = FALSE
WHERE ContributorID = %(ContributorID)s AND OrganizationID = %(OrganizationID)s;
END $$;