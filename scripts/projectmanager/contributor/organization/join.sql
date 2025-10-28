UPDATE ContributorOrganization
SET IsJoined = TRUE
WHERE ContributorID = %(ContributorID)s AND OrganizationID = %(OrganizationID)s;