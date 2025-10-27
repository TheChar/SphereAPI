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
    jsonb_agg(DISTINCT PC.ContributorID) AS ContributorIDs,
    jsonb_agg(DISTINCT C.Name) AS ContributorNames,
    jsonb_agg(DISTINCT T.Title) AS ImportedTags,
    jsonb_agg(DISTINCT T.TagID) AS TagIDs
FROM Projects P
LEFT JOIN ProjectContributor PC ON PC.ProjectID = P.ProjectID
LEFT JOIN TimeEntries TE ON PC.ProjectContributorID = TE.ProjectContributorID
LEFT JOIN Contributors C ON PC.ContributorID = C.ContributorID
LEFT JOIN ProjectTag PT ON PT.ProjectID = P.ProjectID
LEFT JOIN Tags T ON T.TagID = PT.TagID
WHERE P.ProjectID = %(ProjectID)s
GROUP BY P.ProjectID;
