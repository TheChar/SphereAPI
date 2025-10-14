DO $$
BEGIN

SELECT TE.StartTime,
    TE.EndTime,
    C.Name,
    TE.Description,
    TE.Version
FROM TimeEntries TE
LEFT JOIN ProjectContributor PC ON PC.ProjectContributorID = TE.ProjectContributorID
LEFT JOIN Contributors C ON PC.ContributorID = C.ContributorID
WHERE PC.ContributorID = %(ContributorID)s
ORDER BY StartTime DESC;

END $$;