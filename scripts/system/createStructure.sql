CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    HashedPassword VARCHAR(80),
    ExpireMinutes INT
);

CREATE TABLE Roles (
    RoleID SERIAL PRIMARY KEY,
    Operation VARCHAR(10),
    Route VARCHAR(50),
    CONSTRAINT unique_operation_route
        UNIQUE (Operation, Route)
);

CREATE TABLE UserRole (
    UserRoleID SERIAL PRIMARY KEY,
    UserID INT,
    RoleID INT,
    CONSTRAINT fk_users_userrole
        FOREIGN KEY (UserID)
        REFERENCES Users (UserID),
    CONSTRAINT fk_roles_userrole
        FOREIGN KEY (RoleID)
        REFERENCES Roles (RoleID),
    CONSTRAINT unique_userid_roleid
        UNIQUE (UserID, RoleID)
);

-- -- List all tables in the current schema
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname = 'public';