DO $$
BEGIN
UPDATE ProjectContributor
SET IsRemoved = FALSE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RestoredContributorID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RestoredContributorID)s
    ),
    'Rejoined the project',
    TRUE,
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);
END $$;