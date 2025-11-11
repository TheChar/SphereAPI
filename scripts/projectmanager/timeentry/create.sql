DO $$
BEGIN

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (NOW(),
    (SELECT ProjectContributorID
    FROM ProjectContributor
    WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s
    ),
    %(Description)s,
    FALSE,
    COALESCE(%(Version)s, (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s))
);
END $$;