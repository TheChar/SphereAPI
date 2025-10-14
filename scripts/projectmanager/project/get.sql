DO $$
DECLARE is_contributor BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO is_contributor
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s AND IsRemoved = FALSE;

IF NOT is_contributor
THEN
RAISE EXCEPTION 'User cannot retrieve information about a project they are not a part of';
END IF;

SELECT P.ProjectID,
    P.Title,
    P.Version,
    P.Description,
    COUNT(DISTINCT TimeEntryID) AS NumTimeEntries,
    (SELECT C.ContributorID
        FROM Contributors C
        LEFT JOIN ProjectContributor PC ON PC.ContributorID = C.ContributorID
        WHERE PC.ProjectID = %(ProjectID)s AND IsOwner = TRUE
    ) AS OwnerID,
    (SELECT C.Name
        FROM Contributors C
        LEFT JOIN ProjectContributor PC ON PC.ContributorID = C.ContributorID
        WHERE PC.ProjectID = %(ProjectID)s AND IsOwner = TRUE
    ) AS OwnerName,
    jsonb_agg(PC.ContributorID) AS ContributorIDs,
    jsonb_agg(C.Name) AS ContributorNames,
    jsonb_agg(T.Title) AS ImportedTags,
    jsonb_agg(T.TagID) AS TagIDs
FROM Projects P
LEFT JOIN ProjectContributor PC ON PC.ProjectID = P.ProjectID
LEFT JOIN TimeEntries TE ON PC.ProjectContributorID = TE.ProjectContributorID
LEFT JOIN Contributors C ON PC.ContributorID = C.ContributorID
LEFT JOIN ProjectTag PT ON PT.ProjectID = P.ProjectID
LEFT JOIN Tags T ON T.TagID = PT.TagID
WHERE ProjectID = %(ProjectID)s;

END $$;