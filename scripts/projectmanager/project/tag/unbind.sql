DO $$
BEGIN

DELETE FROM ProjectTag
WHERE ProjectID = %(ProjectID)s AND TagID = %(TagID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version);
VALUES (NOW(), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;
    ),
    'Removed the tag ' || (SELECT Title FROM Tags WHERE TagID = %(TagID)s),
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);

RETURN 'Success';
END $$;
