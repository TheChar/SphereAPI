SELECT P.ProjectID,
    P.Title,
FROM Projects P
LEFT JOIN ProjectContributor PC ON PC.ProjectID = P.ProjectID
WHERE PC.ContributorID = %(ContributorID)s AND PC.IsOwner = TRUE AND PC.IsRemoved = FALSE;