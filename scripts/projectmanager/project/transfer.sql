DO $$
BEGIN
UPDATE ProjectContributor
SET IsOwner = TRUE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(NewOwnerID)s;

UPDATE ProjectContributor
SET IsOwner = FALSE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

INSERT INTO TimeEntries(StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ),
    (SELECT ProjectContributorID
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s   
    ),
    'Stepped down from ownership',
    TRUE,
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);

INSERT INTO TimeEntries(StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ),
    (SELECT ProjectContributorID
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(NewOwnerID)s
    ),
    'Assumed ownership',
    TRUE,
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);
END $$;