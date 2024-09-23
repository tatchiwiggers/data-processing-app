-- models/staging/stg_scraped_products.sql

WITH raw_scraped_products AS (
    SELECT
        product_id,
        product_link,
        product_image,
        product_title,
        COALESCE(previous_price, 0) AS previous_price,
        COALESCE(current_price, 0) AS current_price,

        -- Clean the discount field by removing any non-numeric text like ' OFF', 'no PIX', and '%'
        CASE 
            WHEN discount = '' THEN 0.0
            ELSE CAST(REGEXP_REPLACE(discount, '[^0-9]', '') AS FLOAT) / 100
        END AS discount,
        COALESCE(
            CASE 
                WHEN installments = '' THEN 1
                ELSE CAST(SPLIT_PART(SPLIT_PART(installments, 'x', 1), 'em', 2) AS INTEGER)
            END,
            1
        ) AS num_installments,

        -- Extract the installment value, handle empty strings, remove 'R$', and cast to decimal
        -- If num_installments is 1, set installment_value to current_price
        CASE 
            WHEN COALESCE(
                CASE 
                    WHEN SPLIT_PART(installments, 'x', 2) = '' THEN 0.0
                    ELSE CAST(
                        REPLACE(REPLACE(SPLIT_PART(SPLIT_PART(installments, 'x', 2), 'sem juros', 1), 'R$', ''), ',', '.') 
                    AS DECIMAL)
                END, 
                0.0
            ) = 0.0 AND num_installments = 1 THEN current_price
            ELSE COALESCE(
                CASE 
                    WHEN SPLIT_PART(installments, 'x', 2) = '' THEN 0.0
                    ELSE CAST(
                        REPLACE(REPLACE(SPLIT_PART(SPLIT_PART(installments, 'x', 2), 'sem juros', 1), 'R$', ''), ',', '.') 
                    AS DECIMAL)
                END, 
                0.0
            )
        END AS installment_value,

        -- Fill null or empty values in seller with 'não informado'
        COALESCE(NULLIF(seller, ''), 'não informado') AS seller
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