SELECT P.Title
FROM Projects P
LEFT JOIN ProjectContributor PC ON P.ProjectID = PC.ProjectID,
LEFT JOIN Contributors C ON PC.ContributorID = C.ContributorID
WHERE C.ContributorID = %(ContributorID)s;