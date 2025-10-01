INSERT INTO TimeEntries (StartTime, EndTime, ProjectContributorID, Description, Version)
VALUES (
    %(StartTime)s,
    %(EndTime)s,
    INSERT INTO ProjectContributor (ProjectID, ContributorID, IsOwner, IsRemoved)
    VALUES (
        INSERT INTO Projects (Title, DevelopmentStage, Version, Description)
        VALUES (
            %(Title)s, 
            SELECT DevelopmentStageID FROM DevelopmentStages WHERE Stage = %(DevStage)s,
            %(Version)s,
            %(Description)s
        )
        RETURNING ProjectID;
        %(ContributorID)s,
        TRUE,
        FALSE
    )
    RETURNING ProjectContributorID,
    "Created %(Title)s project",
    %(Version)s
)
RETURNING Description;


