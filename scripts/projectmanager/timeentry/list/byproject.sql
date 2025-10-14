DO $$
DECLARE is_cont BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO is_cont
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s AND IsRemoved = FALSE;

IF NOT is_cont
THEN
RAISE EXCEPTION 'User cannot view Time Entries for projects they do not contribute to';
END IF;

SELECT TE.StartTime,
    TE.EndTime,
    C.Name,
    TE.Description,
    TE.Version
FROM TimeEntries TE
LEFT JOIN ProjectContributor PC ON PC.ProjectContributorID = TE.ProjectContributorID
LEFT JOIN Contributors C ON PC.ContributorID = C.ContributorID
WHERE PC.ProjectID = %(ProjectID)s;

END $$;