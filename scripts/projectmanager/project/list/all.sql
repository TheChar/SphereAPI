SELECT P.ProjectID,
    P.Title,
    P.Version,
    P.Description,
    (
        SELECT TE.StartTime
        FROM TimeEntries TE
        LEFT JOIN ProjectContributor PC2 ON TE.ProjectContributorID = PC2.ProjectContributorID
        WHERE TE.SystemGenerated = TRUE
            AND TE.Description LIKE 'Created %%'
            AND PC2.ProjectID = P.ProjectID
        LIMIT 1
    ) AS StartDate,
    (
        SELECT TE.StartTime
        FROM TimeEntries TE
        LEFT JOIN ProjectContributor PC2 ON TE.ProjectContributorID = PC2.ProjectContributorID
        WHERE PC2.ProjectID = P.ProjectID
        ORDER BY TE.StartTime DESC
        LIMIT 1
    ) AS RecentDate,
    EXISTS (
        SELECT 1
        FROM TimeEntries TE
        LEFT JOIN ProjectContributor PC2 ON PC2.ProjectContributorID = TE.ProjectContributorID
        WHERE TE.SystemGenerated = FALSE
            AND TE.EndTime IS NULL
            AND PC2.ProjectID = P.ProjectID
            AND PC2.ContributorID = %(ContributorID)s
    ) AS HasActiveTimer,
    (
        SELECT TE.TimeEntryID
        FROM TimeEntries TE
        LEFT JOIN ProjectContributor PC2 ON PC2.ProjectContributorID = TE.ProjectContributorID
        WHERE TE.SystemGenerated = FALSE
            AND TE.EndTime IS NULL
            AND PC2.ProjectID = P.ProjectID
            AND PC2.ContributorID = %(ContributorID)s
        LIMIT 1
    ) AS ActiveTimeEntryID
FROM Projects P
LEFT JOIN ProjectContributor PC ON PC.ProjectID = P.ProjectID
WHERE PC.ContributorID = %(ContributorID)s AND PC.IsRemoved = FALSE;