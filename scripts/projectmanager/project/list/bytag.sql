SELECT P.ProjectID,
    P.Title
FROM Projects P
LEFT JOIN ProjectTag PT ON P.ProjectID = PT.ProjectID
LEFT JOIN Tags T ON T.TagID = PT.TagID
LEFT JOIN ProjectContributor PC ON PC.ProjectID = P.ProjectID
WHERE T.Title = %(TagTitle)s AND T.Owner = %(ContributorID)s AND PC.IsRemoved = FALSE;