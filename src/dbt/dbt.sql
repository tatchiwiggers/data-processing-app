-- models/staging/stg_scraped_products.sql
WITH raw_scraped_products AS (
    SELECT
        product_id,
        product_link,
        product_image,
        product_title,
        NULLIF(previous_price, '')::NUMERIC AS previous_price,
        NULLIF(REGEXP_REPLACE(current_price, '[^0-9.]', ''), '')::NUMERIC AS current_price,
        discount,
        installments,
        seller
    FROM {{ ref('raw_scraped_products') }}
)

SELECT
    product_id,
    product_link,
    product_image,
    product_title,
    COALESCE(previous_price, 0) AS previous_price,
    current_price,
    discount,
    installments,
    seller
FROM raw_scraped_products
