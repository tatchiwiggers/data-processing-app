-- Create table for product data from web scraping
CREATE OR REPLACE TABLE ecommerce_db.scraped_products (
    product_id INT AUTOINCREMENT, -- Unique product identifier
    product_link STRING NOT NULL, -- URL of the product
    product_image STRING,         -- URL of the product image
    product_title STRING,         -- Title of the product
    previous_price DECIMAL(10, 2),-- Previous price of the product
    current_price DECIMAL(10, 2), -- Current price of the product
    discount STRING,              -- Discount information
    installments STRING,          -- Installments information
    seller STRING,                -- Seller information
    PRIMARY KEY (product_id)
);
