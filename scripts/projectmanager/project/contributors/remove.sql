UPDATE ProjectContributor
SET (IsRemoved = TRUE)
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;