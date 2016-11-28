{% sql 'test_query', note='Fake query for unit tests' %}
SELECT
  {{ name|guards.string }} as name,
  {{ age|guards.integer }} as age,
  {{ activated|guards.bool }} as activated
{% endsql %}