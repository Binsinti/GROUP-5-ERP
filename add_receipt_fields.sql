-- SQL commands to add the missing fields to the payment table
ALTER TABLE erpdb_payment ADD COLUMN receipt_generated BOOLEAN DEFAULT FALSE;
ALTER TABLE erpdb_payment ADD COLUMN receipt_number VARCHAR(20) NULL;

-- If you're using SQLite, use this syntax instead:
-- ALTER TABLE erpdb_payment ADD COLUMN receipt_generated BOOLEAN DEFAULT 0;
-- ALTER TABLE erpdb_payment ADD COLUMN receipt_number TEXT NULL;
