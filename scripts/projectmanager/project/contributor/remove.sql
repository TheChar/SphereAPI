DO $$
BEGIN
UPDATE ProjectContributor
SET IsRemoved = TRUE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RemovedContributorID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES ((
    SELECT NOW() AT TIME ZONE 'UTC'
    ), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RemovedContributorID)s
    ),
    'Left the project',
    TRUE,
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);
END $$;