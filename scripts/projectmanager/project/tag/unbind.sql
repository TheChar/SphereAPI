DO $$
BEGIN

DELETE FROM ProjectTag
WHERE ProjectID = %(ProjectID)s AND TagID = %(TagID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s
    ),
    'Removed the tag ' || (SELECT Title FROM Tags WHERE TagID = %(TagID)s),
    TRUE,
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);

END $$;
