-- models/staging/stg_scraped_products.sql

WITH raw_scraped_products AS (
    SELECT
        product_id,
        product_link,
        product_image,
        product_title,
        COALESCE(previous_price, 0) AS previous_price,
        current_price,

        -- Clean the discount field by removing any non-numeric text like ' OFF', 'no PIX', and '%'
        CASE 
            WHEN discount = '' THEN 0.0
            ELSE CAST(REGEXP_REPLACE(discount, '[^0-9]', '') AS FLOAT) / 100
        END AS discount,

        -- Handle installments by filling nulls with 1 and extracting the number of installments
        COALESCE(
            CASE 
                WHEN installments = '' THEN 1
                ELSE CAST(SPLIT_PART(installments, 'x', 1) AS INTEGER)
            END,
            1
        ) AS num_installments,

        -- Extract the installment value, handle empty strings, remove 'R$', and cast to decimal
        COALESCE(
            CASE 
                WHEN SPLIT_PART(installments, 'x', 2) = '' THEN 0.0
                ELSE CAST(
                    REPLACE(REPLACE(SPLIT_PART(SPLIT_PART(installments, 'x', 2), 'sem juros', 1), 'R$', ''), ',', '.') 
                AS DECIMAL)
            END, 
            0.0
        ) AS installment_value,

        seller
    FROM {{ ref('raw_scraped_products') }}
)

SELECT
    product_id,
    product_link,
    product_image,
    product_title,
    previous_price,
    current_price,
    discount,
    num_installments,
    installment_value,
    seller
FROM raw_scraped_products
