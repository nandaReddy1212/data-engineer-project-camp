{#
    Macro to generate vendor_name column using Jinja dictionary.

    This approach works seamlessly across BigQuery, DuckDB, Snowflake, etc.
    by generating a CASE statement at compile time.

    Usage: {{ get_vendor_data('vendor_id') }}
    Returns: SQL CASE expression that maps vendor_id to vendor_name
#}

{% macro get_vendor_data(vendor_id_column) %}
    CASE {{ vendor_id_column }}
        WHEN 1 THEN 'Creative Mobile Technologies, LLC.'
        WHEN 2 THEN 'VeriFone Inc.'
        WHEN 4 THEN 'Unknown Vendor'
    END
{% endmacro %}