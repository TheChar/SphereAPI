SELECT P.ProjectID,
    P.Title,
    DS.Stage,
    P.Version,
    P.Description,
    CONCAT_WS('#', T.Title) as Tags,
    CONCAT_WS(', ', C.Name) as Contributors,
    jsonb_agg(C.ContributorID) AS ContributorIDs
FROM Project P
LEFT JOIN DevelopmentStages DS ON DS.DevelopmentStageID = P.DevelopmentStageID,
LEFT JOIN ProjectTag PT ON P.ProjectID = PT.ProjectID,
LEFT JOIN Tags T ON T.TagID = PT.TagID,
LEFT JOIN ProjectContributor PC ON PC.ProjectID = P.ProjectID,
LEFT JOIN Contributors C ON PC.ContributorID = C.ContributorID
WHERE P.ProjectID = %(ProjectID)s;