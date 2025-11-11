DO $$
BEGIN

--Update projects only if the field is given
UPDATE Projects
SET
    Title = COALESCE(%(Title)s, Title),
    Description = COALESCE(%(Description)s, Description),
    Version = COALESCE(%(Version)s, Version)
WHERE ProjectID = %(ProjectID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    NOW(),
    (
        SELECT ProjectContributorID
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s
    ),
    'Updated Project Details',
    TRUE,
    (
        SELECT Version
        FROM Projects
        WHERE ProjectID = %(ProjectID)s
    )
);
END $$;