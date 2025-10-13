INSERT INTO ContributorOrganization (ContributorID, OrganizationID, IsOwner)
VALUES (
    %(contributorID)s,
    (SELECT OrganizationID FROM Organizations WHERE Title = %(OrgTitle)s),
    FALSE
);