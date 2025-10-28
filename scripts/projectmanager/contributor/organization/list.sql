SELECT 
    O.OrganizationID,
    O.Title,
    OwnerCO.ContributorID AS OwnerID,
    OwnerCont.Name AS OwnerName,
    UserCO.IsJoined AS AcceptedInvite
FROM Organizations O
JOIN ContributorOrganization UserCO 
    ON UserCO.OrganizationID = O.OrganizationID
    AND UserCO.ContributorID = %(ContributorID)s
JOIN ContributorOrganization OwnerCO
    ON OwnerCO.OrganizationID = O.OrganizationID
    AND OwnerCO.IsOwner = TRUE
JOIN Contributors OwnerCont
    ON OwnerCont.ContributorID = OwnerCO.ContributorID