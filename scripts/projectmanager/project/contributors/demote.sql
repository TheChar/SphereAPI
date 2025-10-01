UPDATE ProjectContributor
SET (IsOwner = FALSE)
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;