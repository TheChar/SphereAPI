INSERT INTO ProjectContributor (ProjectID, ContributorID, IsOwner, IsRemoved)
VALUES (%(ProjectID)s, %(ContributorID)s, %(IsOwner)s, FALSE)
RETURNING ProjectID, ContributorID;