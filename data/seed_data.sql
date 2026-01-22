CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL
);

INSERT OR IGNORE INTO tickets (id, title, status, priority, created_at) VALUES
('TICK-001', 'Login page 404 error', 'OPEN', 'HIGH', '2023-10-26T10:00:00Z'),
('TICK-002', 'Update user profile API latency', 'IN_PROGRESS', 'MEDIUM', '2023-10-25T14:30:00Z'),
('TICK-003', 'Add dark mode support', 'CLOSED', 'LOW', '2023-10-20T09:15:00Z'),
('TICK-004', 'Payment gateway timeout', 'OPEN', 'CRITICAL', '2023-10-27T08:45:00Z'),
('TICK-005', 'Typo in landing page', 'CLOSED', 'LOW', '2023-10-22T11:20:00Z');
