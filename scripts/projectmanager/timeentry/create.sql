DO $$
BEGIN

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version)
VALUES (NOW(),
    (SELECT ProjectContributorID
    FROM ProjectContributor
    WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;
    ),
    %(Description)s,
    COALESCE(%(Version)s, (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s))
);
END $$;