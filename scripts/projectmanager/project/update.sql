DO $$
BEGIN

--Update projects only if the field is given
UPDATE Projects
SET
    Title = COALESCE(%(Title)s, Title),
    Description = COALESCE(%(Description)s, Description),
    Version = COALESCE(%(Version)s, Version),
    Cost = COALESCE(%(Cost)s, Cost),
    HoursRequired = COALESCE(%(HoursRequired)s, HoursRequired),
    Marketability = COALESCE(%(Marketability)s, Marketability),
    UnitValue = COALESCE(%(UnitValue)s, UnitValue),
    Interest = COALESCE(%(Interest)s, Interest)
WHERE ProjectID = %(ProjectID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, SystemGenerated, Version)
VALUES (
    (
        SELECT NOW() AT TIME ZONE 'UTC'
    ),
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