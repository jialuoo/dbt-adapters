#
# Models
#
_MODELS__INCREMENTAL_SYNC_REMOVE_ONLY = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='sync_all_columns'

    )
}}

WITH source_data AS (SELECT * FROM {{ ref('model_a') }} )

{% set string_type = dbt.type_string() %}

{% if is_incremental() %}

SELECT id,
       cast(field1 as {{string_type}}) as field1

FROM source_data WHERE id NOT IN (SELECT id from {{ this }} )

{% else %}

select id,
       cast(field1 as {{string_type}}) as field1,
       cast(field2 as {{string_type}}) as field2

from source_data where id <= 3

{% endif %}
"""

_MODELS__INCREMENTAL_IGNORE = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='ignore'
    )
}}

WITH source_data AS (SELECT * FROM {{ ref('model_a') }} )

{% if is_incremental() %}

SELECT id, field1, field2, field3, field4 FROM source_data WHERE id NOT IN (SELECT id from {{ this }} )

{% else %}

SELECT id, field1, field2 FROM source_data LIMIT 3

{% endif %}
"""

_MODELS__INCREMENTAL_SYNC_REMOVE_ONLY_TARGET = """
{{
    config(materialized='table')
}}

with source_data as (

    select * from {{ ref('model_a') }}

)

{% set string_type = dbt.type_string() %}

select id
       ,cast(field1 as {{string_type}}) as field1

from source_data
order by id
"""

_MODELS__INCREMENTAL_IGNORE_TARGET = """
{{
    config(materialized='table')
}}

with source_data as (

    select * from {{ ref('model_a') }}

)

select id
       ,field1
       ,field2

from source_data
"""

_MODELS__INCREMENTAL_FAIL = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='fail'
    )
}}

WITH source_data AS (SELECT * FROM {{ ref('model_a') }} )

{% if is_incremental()  %}

SELECT id, field1, field2 FROM source_data

{% else %}

SELECT id, field1, field3 FROm source_data

{% endif %}
"""

_MODELS__INCREMENTAL_SYNC_ALL_COLUMNS = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='sync_all_columns'

    )
}}

WITH source_data AS (SELECT * FROM {{ ref('model_a') }} )

{% set string_type = dbt.type_string() %}

{% if is_incremental() %}

SELECT id,
       cast(field1 as {{string_type}}) as field1,
       cast(field3 as {{string_type}}) as field3, -- to validate new fields
       cast(field4 as {{string_type}}) AS field4 -- to validate new fields

FROM source_data WHERE id NOT IN (SELECT id from {{ this }} )

{% else %}

select id,
       cast(field1 as {{string_type}}) as field1,
       cast(field2 as {{string_type}}) as field2

from source_data where id <= 3

{% endif %}
"""

_MODELS__INCREMENTAL_APPEND_NEW_COLUMNS_REMOVE_ONE = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='append_new_columns'
    )
}}

{% set string_type = dbt.type_string() %}

WITH source_data AS (SELECT * FROM {{ ref('model_a') }} )

{% if is_incremental()  %}

SELECT id,
       cast(field1 as {{string_type}}) as field1,
       cast(field3 as {{string_type}}) as field3,
       cast(field4 as {{string_type}}) as field4
FROM source_data WHERE id NOT IN (SELECT id from {{ this }} )

{% else %}

SELECT id,
       cast(field1 as {{string_type}}) as field1,
       cast(field2 as {{string_type}}) as field2
FROM source_data where id <= 3

{% endif %}
"""

_MODELS__A = """
{{
    config(materialized='table')
}}

with source_data as (

    select 1 as id, 'aaa' as field1, 'bbb' as field2, 111 as field3, 'TTT' as field4
    union all select 2 as id, 'ccc' as field1, 'ddd' as field2, 222 as field3, 'UUU' as field4
    union all select 3 as id, 'eee' as field1, 'fff' as field2, 333 as field3, 'VVV' as field4
    union all select 4 as id, 'ggg' as field1, 'hhh' as field2, 444 as field3, 'WWW' as field4
    union all select 5 as id, 'iii' as field1, 'jjj' as field2, 555 as field3, 'XXX' as field4
    union all select 6 as id, 'kkk' as field1, 'lll' as field2, 666 as field3, 'YYY' as field4

)

select id
       ,field1
       ,field2
       ,field3
       ,field4

from source_data
"""

_MODELS__INCREMENTAL_APPEND_NEW_COLUMNS_TARGET = """
{{
    config(materialized='table')
}}

{% set string_type = dbt.type_string() %}

with source_data as (

    select * from {{ ref('model_a') }}

)

select id
       ,cast(field1 as {{string_type}}) as field1
       ,cast(field2 as {{string_type}}) as field2
       ,cast(CASE WHEN id <= 3 THEN NULL ELSE field3 END as {{string_type}}) AS field3
       ,cast(CASE WHEN id <= 3 THEN NULL ELSE field4 END as {{string_type}}) AS field4

from source_data
"""

_MODELS__INCREMENTAL_APPEND_NEW_COLUMNS = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='append_new_columns'
    )
}}

{% set string_type = dbt.type_string() %}

WITH source_data AS (SELECT * FROM {{ ref('model_a') }} )

{% if is_incremental()  %}

SELECT id,
       cast(field1 as {{string_type}}) as field1,
       cast(field2 as {{string_type}}) as field2,
       cast(field3 as {{string_type}}) as field3,
       cast(field4 as {{string_type}}) as field4
FROM source_data WHERE id NOT IN (SELECT id from {{ this }} )

{% else %}

SELECT id,
       cast(field1 as {{string_type}}) as field1,
       cast(field2 as {{string_type}}) as field2
FROM source_data where id <= 3

{% endif %}
"""

_MODELS__INCREMENTAL_SYNC_ALL_COLUMNS_TARGET = """
{{
    config(materialized='table')
}}

with source_data as (

    select * from {{ ref('model_a') }}

)

{% set string_type = dbt.type_string() %}

select id
       ,cast(field1 as {{string_type}}) as field1
       --,field2
       ,cast(case when id <= 3 then null else field3 end as {{string_type}}) as field3
       ,cast(case when id <= 3 then null else field4 end as {{string_type}}) as field4

from source_data
order by id
"""

_MODELS__INCREMENTAL_APPEND_NEW_COLUMNS_REMOVE_ONE_TARGET = """
{{
    config(materialized='table')
}}

{% set string_type = dbt.type_string() %}

with source_data as (

    select * from {{ ref('model_a') }}

)

select id,
       cast(field1 as {{string_type}}) as field1,
       cast(CASE WHEN id >  3 THEN NULL ELSE field2 END as {{string_type}}) AS field2,
       cast(CASE WHEN id <= 3 THEN NULL ELSE field3 END as {{string_type}}) AS field3,
       cast(CASE WHEN id <= 3 THEN NULL ELSE field4 END as {{string_type}}) AS field4

from source_data
"""

# Special Character Column Tests - Test column quoting functionality
_MODELS__A_SPECIAL_CHARS = """
{{
    config(materialized='table')
}}

with source_data as (

    select 1 as id, 'aaa' as {{ adapter.quote("field with space") }}, 'bbb' as {{ adapter.quote("select") }}, 111 as {{ adapter.quote("field-with-dash") }}, 'TTT' as {{ adapter.quote("field.with.dots") }}
    union all select 2 as id, 'ccc' as {{ adapter.quote("field with space") }}, 'ddd' as {{ adapter.quote("select") }}, 222 as {{ adapter.quote("field-with-dash") }}, 'UUU' as {{ adapter.quote("field.with.dots") }}
    union all select 3 as id, 'eee' as {{ adapter.quote("field with space") }}, 'fff' as {{ adapter.quote("select") }}, 333 as {{ adapter.quote("field-with-dash") }}, 'VVV' as {{ adapter.quote("field.with.dots") }}
    union all select 4 as id, 'ggg' as {{ adapter.quote("field with space") }}, 'hhh' as {{ adapter.quote("select") }}, 444 as {{ adapter.quote("field-with-dash") }}, 'WWW' as {{ adapter.quote("field.with.dots") }}
    union all select 5 as id, 'iii' as {{ adapter.quote("field with space") }}, 'jjj' as {{ adapter.quote("select") }}, 555 as {{ adapter.quote("field-with-dash") }}, 'XXX' as {{ adapter.quote("field.with.dots") }}
    union all select 6 as id, 'kkk' as {{ adapter.quote("field with space") }}, 'lll' as {{ adapter.quote("select") }}, 666 as {{ adapter.quote("field-with-dash") }}, 'YYY' as {{ adapter.quote("field.with.dots") }}

)

select id
       ,{{ adapter.quote("field with space") }}
       ,{{ adapter.quote("select") }}
       ,{{ adapter.quote("field-with-dash") }}
       ,{{ adapter.quote("field.with.dots") }}

from source_data
"""

_MODELS__INCREMENTAL_APPEND_NEW_SPECIAL_CHARS = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='append_new_columns'
    )
}}

{% set string_type = dbt.type_string() %}

WITH source_data AS (SELECT * FROM {{ ref('model_a_special_chars') }} )

{% if is_incremental()  %}

SELECT id,
       cast({{ adapter.quote("field with space") }} as {{string_type}}) as {{ adapter.quote("field with space") }},
       cast({{ adapter.quote("select") }} as {{string_type}}) as {{ adapter.quote("select") }},
       cast({{ adapter.quote("field-with-dash") }} as {{string_type}}) as {{ adapter.quote("field-with-dash") }},
       cast({{ adapter.quote("field.with.dots") }} as {{string_type}}) as {{ adapter.quote("field.with.dots") }}
FROM source_data WHERE id NOT IN (SELECT id from {{ this }} )

{% else %}

SELECT id,
       cast({{ adapter.quote("field with space") }} as {{string_type}}) as {{ adapter.quote("field with space") }},
       cast({{ adapter.quote("select") }} as {{string_type}}) as {{ adapter.quote("select") }}
FROM source_data where id <= 3

{% endif %}
"""

_MODELS__INCREMENTAL_APPEND_NEW_SPECIAL_CHARS_TARGET = """
{{
    config(materialized='table')
}}

{% set string_type = dbt.type_string() %}

with source_data as (

    select * from {{ ref('model_a_special_chars') }}

)

select id
       ,cast({{ adapter.quote("field with space") }} as {{string_type}}) as {{ adapter.quote("field with space") }}
       ,cast({{ adapter.quote("select") }} as {{string_type}}) as {{ adapter.quote("select") }}
       ,cast(CASE WHEN id <= 3 THEN NULL ELSE {{ adapter.quote("field-with-dash") }} END as {{string_type}}) AS {{ adapter.quote("field-with-dash") }}
       ,cast(CASE WHEN id <= 3 THEN NULL ELSE {{ adapter.quote("field.with.dots") }} END as {{string_type}}) AS {{ adapter.quote("field.with.dots") }}

from source_data
"""

_MODELS__INCREMENTAL_SYNC_ALL_SPECIAL_CHARS = """
{{
    config(
        materialized='incremental',
        unique_key='id',
        on_schema_change='sync_all_columns'
    )
}}

{% set string_type = dbt.type_string() %}

WITH source_data AS (SELECT * FROM {{ ref('model_a_special_chars') }} )

{% if is_incremental() %}

SELECT id,
       cast({{ adapter.quote("field with space") }} as {{string_type}}) as {{ adapter.quote("field with space") }},
       cast({{ adapter.quote("field-with-dash") }} as {{string_type}}) as {{ adapter.quote("field-with-dash") }},
       cast({{ adapter.quote("field.with.dots") }} as {{string_type}}) as {{ adapter.quote("field.with.dots") }}

FROM source_data WHERE id NOT IN (SELECT id from {{ this }} )

{% else %}

select id,
       cast({{ adapter.quote("field with space") }} as {{string_type}}) as {{ adapter.quote("field with space") }},
       cast({{ adapter.quote("select") }} as {{string_type}}) as {{ adapter.quote("select") }}

from source_data where id <= 3

{% endif %}
"""

_MODELS__INCREMENTAL_SYNC_ALL_SPECIAL_CHARS_TARGET = """
{{
    config(materialized='table')
}}

with source_data as (

    select * from {{ ref('model_a_special_chars') }}

)

{% set string_type = dbt.type_string() %}

select id
       ,cast({{ adapter.quote("field with space") }} as {{string_type}}) as {{ adapter.quote("field with space") }}
       --,{{ adapter.quote("select") }} (removed in sync)
       ,cast(case when id <= 3 then null else {{ adapter.quote("field-with-dash") }} end as {{string_type}}) as {{ adapter.quote("field-with-dash") }}
       ,cast(case when id <= 3 then null else {{ adapter.quote("field.with.dots") }} end as {{string_type}}) as {{ adapter.quote("field.with.dots") }}

from source_data
order by id
"""
