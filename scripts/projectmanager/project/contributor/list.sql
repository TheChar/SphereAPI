SELECT C.ContributorID,
    C.Name,
    jsonb_agg(DISTINCT O.OrganizationID) AS OrgIDs
    jsonb_agg(DISTINCT O.Name) AS OrgNames
    (
        SELECT 1
        FROM TimeEntries
        WHERE ProjectContributorID = (THE REFERENCED PC.PROJECTCONTRIBUTORID)
            AND 
    ) AS JoinDate
FROM Contributors C
LEFT JOIN ProjectContributor PC ON PC.ContributorID = C.ContributorID
LEFT JOIN ContributorOrganization CO ON CO.ContributorID = C.ContributorID
LEFT JOIN Organizations O ON O.OrganizationID = CO.OrganizationID
WHERE PC.ProjectID = $(ProjectID)s;