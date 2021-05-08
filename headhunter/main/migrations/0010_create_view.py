from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210503_1940'),
    ]

    sql = """
    CREATE OR REPLACE VIEW vacancy_employer_view AS
      SELECT e.company_name, e.site, v.vacancy_name, v.vacancy_description, v.salary_min, v.salary_max, v.currency,
             v.publish_date, v.is_active
        FROM main_vacancy AS v
        INNER JOIN main_employer AS e ON e.id = v.company_name_id
        ORDER BY v.publish_date DESC
    """

    operations = [
        migrations.RunSQL('DROP VIEW IF EXISTS vacancy_employer_view;'),
        migrations.RunSQL(sql)
    ]
