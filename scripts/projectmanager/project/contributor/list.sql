SELECT C.ContributorID,
    C.Name,
    jsonb_agg(DISTINCT O.OrganizationID) AS OrgIDs,
    jsonb_agg(DISTINCT O.Title) AS OrgTitles,
    MIN(TE2.StartTime) AS JoinDate,
    COUNT(DISTINCT TE1.TimeEntryID) AS NumTimeEntries,
    PC.IsRemoved,
    PC.IsOwner
FROM Contributors C
LEFT JOIN ProjectContributor PC ON PC.ContributorID = C.ContributorID
LEFT JOIN ContributorOrganization CO ON CO.ContributorID = C.ContributorID
LEFT JOIN Organizations O ON O.OrganizationID = CO.OrganizationID
LEFT JOIN TimeEntries TE1 ON TE1.ProjectContributorID = PC.ProjectContributorID
    AND TE1.SystemGenerated = FALSE
LEFT JOIN TimeEntries TE2 ON TE2.ProjectContributorID = PC.ProjectContributorID
    AND TE2.SystemGenerated = TRUE
    AND TE2.Description = 'Joined Project'
WHERE PC.ProjectID = %(ProjectID)s
GROUP BY C.ContributorID, C.Name, PC.IsRemoved, PC.IsOwner;