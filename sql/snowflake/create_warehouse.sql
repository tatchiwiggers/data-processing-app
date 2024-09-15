CREATE OR REPLACE WAREHOUSE ecommerce_wh
WITH WAREHOUSE_SIZE = 'XSMALL' -- Specify size, e.g., XSMALL, SMALL, MEDIUM, etc.
AUTO_SUSPEND = 300             -- Suspend warehouse after 300 seconds of inactivity
AUTO_RESUME = TRUE;            -- Automatically resume the warehouse when a query is executed
