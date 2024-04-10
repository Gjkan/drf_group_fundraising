# drf_project
Project for group fundraising.

Steps for set up project.

0. Clone in some_folder repository by command 'git clone https://github.com/Gjkan/drf_group_fundraising.git'
1. Create file .env.dev in some_folder/django/group_fundraising/docker/env. 
2. Write down project variables in .env.dev using template from file some_folder/django/group_fundraising/docker/env/.env.template.
3. Open cmd and go to some_folder/django/group_fundraising.
4.  Build image. Write in cmd command 'docker compose -f docker-compose.dev.yml build'. Press enter.
5. Write in cmd command 'docker compose -f docker-compose.dev.yml up' being in the same folder as in step 4. Press enter.
6. Automatically creates 2000 payments, collects and users.
7. Automatically creates 1 superuser with datas, provided in .env.dev.
6. URL 'localhost/api/v1' in browser open group_fundraising api overview.

URLs

1. 'localhost/api/v1' - group_fundraising api overview.
2. 'localhost/api/v1/swagger' - swagger documentation.
3. 'localhost/api/v1/redoc' - redoc documentation.
4. 'localhost/admin' - admin panel.

Management command.

1. 'python manage.py seed' for filling databases with mock data.
2. 'python manage.py initadmin' for creating superuser.

IMPORTANT

All users have email address, provided in .env.dev. So all email will send to that email and tester will see it.