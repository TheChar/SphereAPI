SELECT TE.TimeEntryID,
    TE.StartTime,
    TE.EndTime,
    (TE.EndTime - TE.StartTime) AS ElapsedTime,
    TE.Description,
    TE.Version,
    P.ProjectID,
    P.Title,
    C.ContributorID,
    C.Name
FROM TimeEntries TE
LEFT JOIN ProjectContributor PC ON TE.ProjectContributorID = PC.ProjectContributorID,
LEFT JOIN Projects P ON PC.ProjectID = P.ProjectID
LEFT JOIN Contributors C ON PC.ContributorID = C.ContributorID
WHERE TE.TimeEntryID = %(TimeEntryID)s;