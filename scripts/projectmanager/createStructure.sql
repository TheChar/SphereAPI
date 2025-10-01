CREATE TABLE DevelopmentStages (
    DevelopmentStageID SERIAL PRIMARY KEY,
    Stage VARCHAR(20)
);

CREATE TABLE Projects (
    ProjectID SERIAL PRIMARY KEY,
    Title VARCHAR(50),
    DevelopmentStageID INT,
    Version VARCHAR(10),
    Description VARCHAR(300),
    CONSTRAINT fk_project_developmentstage
        FOREIGN KEY (DevelopmentStageID)
        REFERENCES DevelopmentStages (DevelopmentStageID)
);

CREATE TABLE Organizations (
    OrganizationID SERIAL PRIMARY KEY,
    Title VARCHAR(100),
    Location VARCHAR(100)
);

CREATE TABLE Contributors (
    ContributorID SERIAL PRIMARY KEY,
    Name VARCHAR(50),
    Location VARCHAR(50),
    CONSTRAINT ck_Name_alpha
        CHECK (Name NOT LIKE '%[^A-Z]%')
);

CREATE TABLE ContributorOrganization (
    ContributorOrganizationID SERIAL PRIMARY KEY,
    ContributorID INT,
    OrganizationID INT,
    CONSTRAINT fk_contributor_contributororganzation
        FOREIGN KEY (ContributorID)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT fk_organization_contributororganization
        FOREIGN KEY (OrganizationID)
        REFERENCES Organizations (OrganizationID)
);

CREATE TABLE ProjectContributor (
    ProjectContributorID SERIAL PRIMARY KEY,
    ProjectID INT,
    ContributorID INT,
    IsOwner BOOLEAN,
    IsRemoved BOOLEAN,
    CONSTRAINT fk_projects_projectcontributor
        FOREIGN KEY (ProjectID)
        REFERENCES Projects (ProjectID),
    CONSTRAINT fk_contributors_projectcontributor
        FOREIGN KEY (ContributorID)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT unique_projectid_contributorid
        UNIQUE (ProjectID, ContributorID)
);

CREATE TABLE Tags (
    TagID SERIAL PRIMARY KEY,
    Title VARCHAR(20),
    Implements JSON,
    Owner: Int
    CONSTRAINT ck_title_alphanumeric
        CHECK (Title NOT LIKE '%[^A-Z0-9]%'),
    CONSTRAINT fk_owner_contributor
        FOREIGN KEY (Owner)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT unique_title_owner
        UNIQUE (Title, Owner)
);

CREATE TABLE ProjectTag (
    ProjectTagID SERIAL PRIMARY KEY,
    ProjectID INT,
    TagID INT,
    IsPublic BOOLEAN,
    CONSTRAINT fk_projects_projecttag
        FOREIGN KEY (ProjectID)
        REFERENCES Projects (ProjectID),
    CONSTRAINT fk_tags_projecttag
        FOREIGN KEY (TagID)
        REFERENCES Tags (TagID)
);

CREATE TABLE WebComponents (
    WebComponentID SERIAL PRIMARY KEY,
    Title VARCHAR(50),
    Parameters JSON
);

CREATE TABLE ProjectWebComponent (
    ProjectWebComponentID SERIAL PRIMARY KEY,
    ProjectID INT,
    WebComponentID INT,
    ListOrder INT,
    CONSTRAINT fk_projects_projectwebcomponent
        FOREIGN KEY (ProjectID)
        REFERENCES Projects (ProjectID),
    CONSTRAINT fk_webcomponents_projectwebcomponent
        FOREIGN KEY (WebComponentID)
        REFERENCES WebComponents (WebComponentID)
);

CREATE TABLE TimeEntries (
    TimeEntryID SERIAL PRIMARY KEY,
    StartTime DATE,
    EndTime DATE,
    ProjectContributorID INT,
    Description VARCHAR(300),
    Version VARCHAR(30),
    CONSTRAINT fk_projectcontributor_timeentries
        FOREIGN KEY (ProjectContributorID)
        REFERENCES ProjectContributor (ProjectContributorID)
);

