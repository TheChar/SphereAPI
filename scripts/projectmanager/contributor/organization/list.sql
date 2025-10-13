SELECT O.Title, O.Owner
FROM Organizations O
LEFT JOIN ContributorOrganization CO ON CO.OrganizationID = O.OrganizationID
WHERE CO.ContributorID = %(ContributorID)s;