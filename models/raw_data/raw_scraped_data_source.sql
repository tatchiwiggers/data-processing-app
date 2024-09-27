WITH 
source AS (
    SELECT 
        * 
    FROM 
        {{ source('raw_data', 'raw_scraped_data_source') }}
),

renamed AS (
    SELECT
        product_link,
        product_image,
        product_title,
        previous_price,
        current_price,
        discount,
        installments,
        seller,
        CURRENT_TIMESTAMP AS inserted_at,
        CURRENT_TIMESTAMP AS updated_at
    FROM 
        source
)

select * from renamed
