SELECT TE.TimeEntryID,
    TE.StartTime,
    TE.EndTime,
    (TE.EndTime - TE.StartTime) AS ElapsedTime,
    TE.Description,
    TE.Version,
    C.ContributorID,
    C.Name
FROM TimeEntries TE
LEFT JOIN ProjectContributor PC ON PC.ProjectContributorID = TE.ProjectContributorID,
LEFT JOIN Contributors C ON C.ContributorID = PC.ContributorID,
WHERE PC.ProjectID = %(ProjectID)s;