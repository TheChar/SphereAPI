UPDATE ProjectContributor
SET (IsOwner = TRUE)
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;