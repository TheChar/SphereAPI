CREATE TABLE Organizations (
    OrganizationID SERIAL PRIMARY KEY,
    Title VARCHAR(100)
);

CREATE TABLE Contributors (
    ContributorID SERIAL PRIMARY KEY,
    Name VARCHAR(50)
);

CREATE TABLE ContributorOrganization (
    ContributorOrganizationID SERIAL PRIMARY KEY,
    ContributorID INT,
    OrganizationID INT,
    IsOwner BOOLEAN,
    CONSTRAINT fk_contributor_contributororganization
        FOREIGN KEY (ContributorID)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT fk_organization_contributororganization
        FOREIGN KEY (OrganizationID)
        REFERENCES Organizations (OrganizationID),
    CONSTRAINT unique_contributor_organization
        UNIQUE (ContributorID, OrganizationID)
);

CREATE TABLE Projects (
    ProjectID SERIAL PRIMARY KEY,
    Title VARCHAR(100),
    Version VARCHAR(30),
    Description VARCHAR(300)
);

CREATE TABLE ProjectContributor (
    ProjectContributorID SERIAL PRIMARY KEY,
    ProjectID INT,
    ContributorID INT,
    IsOwner BOOLEAN,
    IsRemoved BOOLEAN,
    CONSTRAINT fk_project_projectcontributor
        FOREIGN KEY (ProjectID)
        REFERENCES Projects (ProjectID),
    CONSTRAINT fk_contributor_projectcontributor
        FOREIGN KEY (ContributorID)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT unique_project_contributor
        UNIQUE (ContributorID, ProjectID)
);

CREATE TABLE TimeEntries (
    TimeEntryID SERIAL PRIMARY KEY,
    StartTime DATE,
    EndTime DATE,
    ProjectContributorID INT,
    Description VARCHAR(300),
    Version VARCHAR(30),
    CONSTRAINT fk_timeentry_projectcontributor
        FOREIGN KEY (ProjectContributorID)
        REFERENCES ProjectContributor (ProjectContributorID)
);

CREATE TABLE Tags (
    TagID SERIAL PRIMARY KEY,
    Implements JSON,
    Owner INT,
    CONSTRAINT fk_tags_contributors
        FOREIGN KEY (Owner)
        REFERENCES Contributors (ContributorID)
);

CREATE TABLE ProjectTag (
    ProjectTagID SERIAL PRIMARY KEY,
    ProjectID INT,
    TagID INT,
    Implementations JSON,
    CONSTRAINT fk_projects_projecttag
        FOREIGN KEY (ProjectID)
        REFERENCES Projects (ProjectID),
    CONSTRAINT fk_tags_projecttag
        FOREIGN KEY (TagID)
        REFERENCES Tags (TagID),
    CONSTRAINT unique_project_tag
        UNIQUE (ProjectID, TagID)
);