DO $$
DECLARE
    app_id INT;
    role_id INT;
    role_count INT;
BEGIN
-- Get the application ID
SELECT ApplicationID INTO app_id
FROM Applications
WHERE Title = %(AppTitle)s;

-- Get the role count for that app
SELECT COUNT(*) INTO role_count
FROM Roles
WHERE ApplicationID = app_id;

IF role_count <= 1 THEN
    RAISE EXCEPTION 'This is the last role for %%. You cannot remove it.', %(AppTitle)s;
END IF;

-- Get the role ID to delete
SELECT RoleID INTO role_id
FROM Roles
WHERE ApplicationID = app_id AND Title = %(RoleTitle)s;

-- Check if any users have this role
IF EXISTS (SELECT 1 FROM UserApplication WHERE RoleID = role_id) THEN
    RAISE EXCEPTION 'A user has this role. It cannot be removed.';
END IF;

-- Delete role-route connections
DELETE FROM RoleRoute WHERE RoleID = role_id;

-- Delete the role itself
DELETE FROM Roles WHERE RoleID = role_id;

-- Delete routes that aren't connected to any role
DELETE FROM Routes
WHERE NOT EXISTS (
    SELECT 1
    FROM RoleRoute
    WHERE Routes.RouteID = RoleRoute.RouteID
);
END $$;
