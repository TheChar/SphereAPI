SELECT TE.TimeEntryID,
    TE.StartTime,
    TE.EndTime,
    TE.ProjectContributorID,
    C.ContributorID AS ContributorID,
    C.Name AS ContributorName,
    TE.Description,
    TE.SystemGenerated,
    TE.Version
FROM TimeEntries TE
LEFT JOIN ProjectContributor PC ON PC.ProjectContributorID = TE.ProjectContributorID
LEFT JOIN Contributors C ON C.ContributorID = PC.ContributorID
WHERE TE.TimeEntryID = %(TimeEntryID)s