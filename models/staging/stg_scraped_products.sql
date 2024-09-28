WITH raw_data AS (
    SELECT
        product_link,
        product_image,
        product_title,
        -- Remove currency symbol and convert prices to numeric values
        REPLACE(REPLACE(previous_price, 'R$', ''), ',', '.')::NUMERIC AS previous_price,
        REPLACE(REPLACE(current_price, 'R$', ''), ',', '.')::NUMERIC AS current_price,
        
        -- Calculate discount as a decimal
        CASE 
            WHEN discount = '' THEN 0.0
            ELSE ROUND(CAST(REGEXP_REPLACE(discount, '[^0-9]', '') AS FLOAT) / 100, 2)
        END AS discount,
        
        -- Extract the number of installments
        COALESCE(
            CASE 
                WHEN installments = '' THEN 1
                ELSE CAST(SPLIT_PART(SPLIT_PART(installments, 'x', 1), 'em', 2) AS INTEGER)
            END, 
            1
        ) AS num_installments,
        
        -- Calculate the installment value
        ROUND(
            CASE 
                WHEN COALESCE(
                    CASE 
                        WHEN SPLIT_PART(installments, 'x', 2) = '' THEN 0.0
                        ELSE CAST(
                            REPLACE(REPLACE(SPLIT_PART(SPLIT_PART(installments, 'x', 2), 'sem juros', 1), 'R$', ''), ',', '.')
                        AS NUMERIC(18, 10))
                    END, 
                    0.0
                ) = 0.0 AND num_installments = 1 THEN current_price
                ELSE COALESCE(
                    CASE 
                        WHEN SPLIT_PART(installments, 'x', 2) = '' THEN 0.0
                        ELSE CAST(
                            REPLACE(REPLACE(SPLIT_PART(SPLIT_PART(installments, 'x', 2), 'sem juros', 1), 'R$', ''), ',', '.')
                        AS NUMERIC(18, 10))
                    END, 
                    0.0
                )
            END, 
            2
        ) AS installment_value,
        
        -- Handle missing or null seller information
        COALESCE(NULLIF(seller, ''), 'não informado') AS seller,
        
        -- Add timestamps for tracking inserts and updates
        CURRENT_TIMESTAMP AS inserted_at,
        CURRENT_TIMESTAMP AS updated_at

    FROM {{ ref('raw_scraped_data_source') }} -- Reference the raw source table/view
)

SELECT
    product_link,
    product_image,
    product_title,
    previous_price,
    current_price,
    discount,
    num_installments,
    installment_value,
    seller,
    inserted_at,
    updated_at
FROM raw_data
