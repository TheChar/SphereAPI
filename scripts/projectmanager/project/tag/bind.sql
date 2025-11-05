DO $$
BEGIN

INSERT INTO ProjectTag (ProjectID, TagID, Implementations)
VALUES (%(ProjectID)s, %(TagID)s, %(Implementations)s);

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version)
VALUES (NOW(), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s
    ),
    'Added the tag ' || (SELECT Title FROM Tags WHERE TagID = %(TagID)s),
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);
END $$;