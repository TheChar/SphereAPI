DO $$
BEGIN

UPDATE TimeEntries
SET
    StartTime = COALESCE(%(StartTime)s, StartTime),
    EndTime = COALESCE(%(EndTime)s, EndTime),
    Description = COALESCE(%(Description)s, Description),
    Version = COALESCE(%(Version)s, Version)
WHERE TimeEntryID = %(TimeEntryID)s;
END $$;