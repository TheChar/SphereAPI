DO $$
BEGIN
UPDATE ProjectContributor
SET IsRemoved = FALSE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RestoredContributorID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version);
VALUES (NOW(), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(RestoredContributorID)s;
    ),
    'Rejoined the project',
    (SELECT Version FROM Projects WHERE ProjectID = %(ProejctID)s)
);
END $$;