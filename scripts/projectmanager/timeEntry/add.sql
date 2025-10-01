INSERT INTO TimeEntries (StartTime, EndTime, ProjectContributorID, Description, Version)
VALUES (
    %(StartTime)s,
    %(EndTime)s,
    SELECT ProjectContributorID
    FROM ProjectContributor
    WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s,
    %(Description)s,
    %(Version)s
)
RETURNING (EndTime - StartTime) AS ElapsedTime;