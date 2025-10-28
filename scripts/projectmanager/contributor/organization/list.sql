SELECT 
    O.OrganizationID,
    O.Title,
    OwnerCO.ContributorID AS OwnerID
FROM Organizations O
JOIN ContributorOrganization UserCO 
    ON UserCO.OrganizationID = O.OrganizationID
    AND UserCO.ContributorID = %(ContributorID)s
JOIN ContributorOrganization OwnerCO
    ON OwnerCO.OrganizationID = O.OrganizationID
    AND OwnerCO.IsOwner = TRUE;