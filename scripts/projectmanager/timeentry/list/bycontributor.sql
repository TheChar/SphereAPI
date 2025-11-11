SELECT TE.TimeEntryID,
    TE.StartTime,
    TE.EndTime,
    P.Title AS ProjectTitle,
    TE.Description,
    TE.SystemGenerated,
    TE.Version
FROM TimeEntries TE
LEFT JOIN ProjectContributor PC ON PC.ProjectContributorID = TE.ProjectContributorID
LEFT JOIN Projects P ON PC.ProjectID = P.ProjectID
WHERE PC.ContributorID = %(ContributorID)s
ORDER BY TE.StartTime DESC;